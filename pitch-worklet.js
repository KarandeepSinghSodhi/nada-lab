/**
 * Song Lab — Real-time Pitch Detection Processor (AudioWorklet)
 * Uses McLeod Pitch Method / Normalized Square Difference Function (NSDF)
 * running at 100 Hz frame intervals (every 10 ms).
 */

class PitchWorkletProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    // 2048 samples at 44.1/48kHz gives ~45 ms window, suitable down to ~60 Hz (low Mandra Saptak)
    this.bufferSize = 2048;
    this.buffer = new Float32Array(this.bufferSize);
    this.writePos = 0;
    this.hopSamples = 480; // ~10 ms hop at 48kHz
    this.samplesSinceLastHop = 0;
  }

  process(inputs) {
    const input = inputs[0];
    if (!input || !input[0]) return true;

    const channelData = input[0];
    const len = channelData.length;

    for (let i = 0; i < len; i++) {
      this.buffer[this.writePos] = channelData[i];
      this.writePos = (this.writePos + 1) % this.bufferSize;
      this.samplesSinceLastHop++;

      if (this.samplesSinceLastHop >= this.hopSamples) {
        this.samplesSinceLastHop = 0;
        this.detectPitch();
      }
    }

    return true;
  }

  detectPitch() {
    // Linearize ring buffer into contiguous array
    const window = new Float32Array(this.bufferSize);
    const head = this.writePos;
    for (let i = 0; i < this.bufferSize; i++) {
      window[i] = this.buffer[(head + i) % this.bufferSize];
    }

    // 1. RMS Energy Gate
    let sumSq = 0;
    for (let i = 0; i < this.bufferSize; i++) {
      sumSq += window[i] * window[i];
    }
    const rms = Math.sqrt(sumSq / this.bufferSize);
    if (rms < 0.012) {
      this.port.postMessage({ pitch: null, clarity: 0, rms: rms });
      return;
    }

    // 2. Normalized Square Difference Function (NSDF) / MPM
    const maxLag = Math.floor(sampleRate / 60); // 60 Hz minimum
    const minLag = Math.floor(sampleRate / 850); // 850 Hz maximum
    const nsdf = new Float32Array(maxLag);

    for (let tau = 0; tau < maxLag; tau++) {
      let acf = 0;
      let m = 0;
      for (let i = 0; i < this.bufferSize - tau; i++) {
        const x = window[i];
        const y = window[i + tau];
        acf += x * y;
        m += x * x + y * y;
      }
      nsdf[tau] = m > 0 ? (2 * acf) / m : 0;
    }

    // 3. Peak picking with parabolic interpolation
    let maxClarity = 0;
    let bestTau = 0;
    let inPositiveRegion = false;

    for (let tau = minLag; tau < maxLag - 1; tau++) {
      if (nsdf[tau] > 0 && !inPositiveRegion) {
        inPositiveRegion = true;
      } else if (nsdf[tau] <= 0 && inPositiveRegion) {
        inPositiveRegion = false;
      }

      if (inPositiveRegion) {
        if (nsdf[tau] > nsdf[tau - 1] && nsdf[tau] >= nsdf[tau + 1]) {
          // Local maximum found
          const alpha = nsdf[tau - 1];
          const beta = nsdf[tau];
          const gamma = nsdf[tau + 1];
          const denom = 2 * (alpha - 2 * beta + gamma);
          const delta = denom !== 0 ? (alpha - gamma) / denom : 0;
          const refinedTau = tau + delta;
          const refinedVal = beta - (delta * (alpha - gamma)) / 4;

          if (refinedVal > maxClarity) {
            maxClarity = refinedVal;
            bestTau = refinedTau;
          }
        }
      }
    }

    // Minimum clarity threshold for vocal voicing
    if (maxClarity >= 0.55 && bestTau > 0) {
      const freq = sampleRate / bestTau;
      this.port.postMessage({ pitch: freq, clarity: maxClarity, rms: rms });
    } else {
      this.port.postMessage({ pitch: null, clarity: maxClarity, rms: rms });
    }
  }
}

registerProcessor('pitch-worklet-processor', PitchWorkletProcessor);
