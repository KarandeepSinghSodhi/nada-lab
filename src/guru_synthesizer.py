"""
Virtual Guru Generative Audio Synthesizer for Song Lab.
Synthesizes acoustic reference vocal phrases with smooth continuous portamento (Meends),
authentic 22-Shruti microtonal intonation, and vocal formant harmonics.
"""

import base64
import io
from typing import Dict, List, Optional
import numpy as np
import soundfile as sf

from src.raga_matcher import SWARA_TO_SEMITONE
from src.tonal_engine import SHRUTI_TABLE

SR = 22050


def synthesize_guru_phrase(
    sa_hz: float = 146.83,
    swaras: Optional[List[str]] = None,
    note_dur_sec: float = 0.5,
    glide_sec: float = 0.16,
    sr: int = SR,
) -> Dict:
    """
    Synthesizes ideal Guru reference audio at the exact requested Sa tonic frequency.
    Returns:
        wav_bytes: Raw 16-bit PCM WAV bytes
        data_url: Base64 data:audio/wav string for instant Web Audio / <audio> playback
        duration_sec: Total duration in seconds
        ideal_cents_trajectory: Array of ideal cents relative to Sa
    """
    if not swaras:
        swaras = ["N.", "R", "G", "M", "P"]  # Default Yaman Pakad opening

    cents_list = []
    for s in swaras:
        clean = s.replace("*", "").replace(".", "")
        octave_shift = 1200.0 if "*" in s else (-1200.0 if "." in s else 0.0)
        semi = SWARA_TO_SEMITONE.get(clean, 0)
        ratio_cent = semi * 100.0
        for item in SHRUTI_TABLE:
            if item.swara_hindustani == clean:
                ratio_cent = item.cents
                break
        cents_list.append(ratio_cent + octave_shift)

    # Build continuous frequency and cents contour
    f0_contour = []
    cents_contour = []
    dt = 1.0 / sr

    for i in range(len(cents_list)):
        c_curr = cents_list[i]
        freq_curr = sa_hz * (2.0 ** (c_curr / 1200.0))
        
        # Steady portion
        steady_dur = max(0.05, note_dur_sec - glide_sec)
        steady_samples = int(steady_dur * sr)
        f0_contour.extend([freq_curr] * steady_samples)
        cents_contour.extend([c_curr] * steady_samples)

        # Smooth glide into next note
        if i < len(cents_list) - 1:
            c_next = cents_list[i + 1]
            freq_next = sa_hz * (2.0 ** (c_next / 1200.0))
            glide_samples = int(glide_sec * sr)
            
            # Smooth Hermite/Sigmoid glide interpolation (Meend)
            t = np.linspace(0.0, 1.0, glide_samples)
            s_curve = t * t * (3.0 - 2.0 * t)
            
            f_glide = freq_curr + (freq_next - freq_curr) * s_curve
            c_glide = c_curr + (c_next - c_curr) * s_curve
            
            f0_contour.extend(f_glide.tolist())
            cents_contour.extend(c_glide.tolist())

    f0_arr = np.array(f0_contour, dtype=np.float32)
    phase = 2.0 * np.pi * np.cumsum(f0_arr) * dt

    # Multi-harmonic acoustic synthesis simulating human vocal tract [a:] vowel:
    # Rich low harmonics with realistic acoustic decay
    audio = (
        1.00 * np.sin(phase) +
        0.58 * np.sin(2.0 * phase) +
        0.32 * np.sin(3.0 * phase) +
        0.18 * np.sin(4.0 * phase) +
        0.09 * np.sin(5.0 * phase) +
        0.04 * np.sin(6.0 * phase)
    )

    # Apply 25ms smooth attack and release envelope to eliminate clipping clicks
    env_samples = int(0.025 * sr)
    if len(audio) > 2 * env_samples:
        audio[:env_samples] *= np.linspace(0.0, 1.0, env_samples)
        audio[-env_samples:] *= np.linspace(1.0, 0.0, env_samples)

    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = (audio / peak) * 0.75

    buf = io.BytesIO()
    sf.write(buf, audio.astype(np.float32), sr, format="WAV", subtype="PCM_16")
    wav_bytes = buf.getvalue()
    b64_str = base64.b64encode(wav_bytes).decode("ascii")
    data_url = f"data:audio/wav;base64,{b64_str}"

    return {
        "swaras": swaras,
        "sa_hz": round(float(sa_hz), 2),
        "duration_sec": round(float(len(audio) / sr), 3),
        "data_url": data_url,
        "cents_trajectory": [round(c, 1) for c in cents_contour[::int(sr * 0.02)]],  # 50 Hz downsample
    }
