/**
 * SONG LAB — Official Marketing Video & Product Demo Generator
 * Uses Headless Chrome via CDP, Local HTTP Server for reliable WAV streaming,
 * HTML5 Canvas 60fps/30fps renderer, Studio-Mastered Acoustic Indian Classical Soundtrack,
 * and MediaRecorder to produce a broadcast-ready marketing video (marketing_demo.webm).
 */

import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';
import { createServer } from 'node:http';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';

async function main() {
  console.log('===============================================================');
  console.log('SONG LAB — GENERATING OFFICIAL 42-SECOND CINEMATIC MARKETING VIDEO');
  console.log('Synchronizing Multi-Track Acoustic Soundtrack with Visual Scenes');
  console.log('===============================================================');

  const wavPath = resolve('marketing_soundtrack.wav');
  if (!existsSync(wavPath)) {
    throw new Error('marketing_soundtrack.wav not found! Please run generate_cinematic_soundtrack.py first.');
  }

  // Create local HTTP server for zero-latency WAV streaming
  const server = createServer((req, res) => {
    if (req.url === '/soundtrack.wav') {
      const data = readFileSync(wavPath);
      res.writeHead(200, {
        'Content-Type': 'audio/wav',
        'Content-Length': data.length,
        'Access-Control-Allow-Origin': '*'
      });
      res.end(data);
      return;
    }
    res.writeHead(404);
    res.end();
  });

  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;
  console.log(`Local audio server running on http://127.0.0.1:${port}`);

  const width = 1280;
  const height = 720;
  const durationSec = 42;

  console.log(`Launching headless Chrome at ${width}x${height} for video generation...`);
  const browser = await Browser.launch({
    width,
    height,
    extraArgs: [
      '--autoplay-policy=no-user-gesture-required',
      '--disable-web-security',
      '--allow-file-access-from-files'
    ]
  });

  const page = await browser.newPage({ width, height });

  console.log('Setting up motion graphics canvas and audio routing...');

  const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #07090e; overflow: hidden; display: flex; align-items: center; justify-content: center; width: 1280px; height: 720px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    canvas { width: 1280px; height: 720px; background: #07090e; }
  </style>
</head>
<body>
  <canvas id="stage" width="1280" height="720"></canvas>
  <script>
    async function startProduction() {
      const canvas = document.getElementById('stage');
      const ctx = canvas.getContext('2d');
      const W = 1280, H = 720;

      // 1. Fetch & Decode Studio Master Soundtrack
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      const audioCtx = new AudioContext();
      const dest = audioCtx.createMediaStreamDestination();

      const resp = await fetch('http://127.0.0.1:${port}/soundtrack.wav');
      const arrayBuf = await resp.arrayBuffer();
      const decodedBuf = await audioCtx.decodeAudioData(arrayBuf);

      const bufferSource = audioCtx.createBufferSource();
      bufferSource.buffer = decodedBuf;
      bufferSource.connect(dest);

      // 2. Setup MediaRecorder
      const stream = canvas.captureStream(30);
      const audioTrack = dest.stream.getAudioTracks()[0];
      if (audioTrack) {
        stream.addTrack(audioTrack);
      }

      const recorder = new MediaRecorder(stream, {
        mimeType: 'video/webm;codecs=vp8,opus',
        videoBitsPerSecond: 4500000
      });

      const recordedChunks = [];
      recorder.ondataavailable = e => {
        if (e.data && e.data.size > 0) recordedChunks.push(e.data);
      };

      window.__recordingFinished = false;
      window.__recordingDataUrl = null;

      recorder.onstop = () => {
        const blob = new Blob(recordedChunks, { type: 'video/webm' });
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = () => {
          window.__recordingDataUrl = reader.result;
          window.__recordingFinished = true;
        };
      };

      // Particle background
      const particles = [];
      for (let i = 0; i < 80; i++) {
        particles.push({
          x: Math.random() * W,
          y: Math.random() * H,
          r: Math.random() * 2 + 0.8,
          vx: (Math.random() - 0.5) * 0.4,
          vy: (Math.random() - 0.5) * 0.4,
          alpha: Math.random() * 0.5 + 0.2
        });
      }

      // Synchronized Kick-off
      bufferSource.start(0);
      recorder.start();
      const startTime = performance.now();

      // Reliable timeout to stop recording at exactly 42.2s
      setTimeout(() => {
        recorder.stop();
      }, 42200);

      function render() {
        const now = performance.now();
        const elapsedSec = (now - startTime) / 1000;

        ctx.fillStyle = '#07090e';
        ctx.fillRect(0, 0, W, H);

        // Radial background glow
        const grad = ctx.createRadialGradient(W / 2, H / 2, 50, W / 2, H / 2, 600);
        grad.addColorStop(0, 'rgba(16, 185, 129, 0.08)');
        grad.addColorStop(0.5, 'rgba(14, 165, 233, 0.04)');
        grad.addColorStop(1, 'rgba(7, 9, 14, 0)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, W, H);

        // Animate particles
        ctx.fillStyle = '#38bdf8';
        particles.forEach(p => {
          p.x += p.vx;
          p.y += p.vy;
          if (p.x < 0) p.x = W;
          if (p.x > W) p.x = 0;
          if (p.y < 0) p.y = H;
          if (p.y > H) p.y = 0;
          ctx.save();
          ctx.globalAlpha = p.alpha;
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          ctx.fill();
          ctx.restore();
        });

        // Top persistent header bar
        ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
        ctx.fillRect(40, 25, W - 80, 48);
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
        ctx.strokeRect(40, 25, W - 80, 48);

        ctx.fillStyle = '#10b981';
        ctx.font = 'bold 15px -apple-system, sans-serif';
        ctx.fillText('● SONG LAB', 60, 55);

        ctx.fillStyle = '#94a3b8';
        ctx.font = '500 13px -apple-system, sans-serif';
        ctx.fillText('MICROTONAL AI VOCAL & ACOUSTIC PLATFORM', 170, 55);

        ctx.fillStyle = '#f59e0b';
        ctx.font = 'bold 12px -apple-system, sans-serif';
        ctx.fillText('R&D RELEASE 2026', W - 200, 55);

        // Determine active scene
        if (elapsedSec < 7) {
          renderScene1(elapsedSec);
        } else if (elapsedSec < 14) {
          renderScene2(elapsedSec - 7);
        } else if (elapsedSec < 21) {
          renderScene3(elapsedSec - 14);
        } else if (elapsedSec < 28) {
          renderScene4(elapsedSec - 21);
        } else if (elapsedSec < 35) {
          renderScene5(elapsedSec - 28);
        } else {
          renderScene6(elapsedSec - 35);
        }

        // Progress bar at bottom
        const progress = Math.min(1.0, elapsedSec / 42);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.fillRect(0, H - 6, W, 6);
        const pGrad = ctx.createLinearGradient(0, 0, W, 0);
        pGrad.addColorStop(0, '#10b981');
        pGrad.addColorStop(0.5, '#06b6d4');
        pGrad.addColorStop(1, '#f59e0b');
        ctx.fillStyle = pGrad;
        ctx.fillRect(0, H - 6, W * progress, 6);

        if (elapsedSec < 42.5) {
          requestAnimationFrame(render);
        }
      }

      // SCENE 1: The Problem with Big Tech Generative Audio
      function renderScene1(t) {
        const alpha = Math.min(1, t * 1.5);
        ctx.save();
        ctx.globalAlpha = alpha;

        ctx.fillStyle = 'rgba(239, 68, 68, 0.15)';
        ctx.strokeStyle = '#ef4444';
        ctx.beginPath();
        ctx.roundRect(W / 2 - 170, 110, 340, 32, 16);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#fca5a5';
        ctx.font = 'bold 12px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('THE GENERATIVE AUDIO BOTTLENECK', W / 2, 131);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 40px sans-serif';
        ctx.fillText('Beyond 12-TET Quantization', W / 2, 185);

        ctx.fillStyle = '#94a3b8';
        ctx.font = '18px sans-serif';
        ctx.fillText('Why Suno, Udio, and OpenAI struggle to model the human soul.', W / 2, 220);

        const cardY = 270;
        const cardW = 540;
        const cardH = 340;

        // Left: Discrete RVQ
        ctx.fillStyle = 'rgba(15, 23, 42, 0.8)';
        ctx.strokeStyle = 'rgba(239, 68, 68, 0.4)';
        ctx.beginPath();
        ctx.roundRect(80, cardY, cardW, cardH, 12);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#ef4444';
        ctx.font = 'bold 18px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText('✕ Discrete RVQ Tokenization (Suno / Udio)', 110, cardY + 45);

        ctx.fillStyle = '#94a3b8';
        ctx.font = '14px sans-serif';
        ctx.fillText('• 100-cent semitone quantization lattice', 110, cardY + 80);
        ctx.fillText('• Collapses microtonal 22-shrutis into static bins', 110, cardY + 110);
        ctx.fillText('• Non-physiological staircase derivative jerk', 110, cardY + 140);
        ctx.fillText('• Phase drift across portamenti & meends', 110, cardY + 170);

        // Draw staircase waveform
        ctx.strokeStyle = '#ef4444';
        ctx.lineWidth = 3;
        ctx.beginPath();
        const stepW = 60;
        let sx = 110;
        let sy = cardY + 280;
        ctx.moveTo(sx, sy);
        for (let i = 0; i < 7; i++) {
          sx += stepW;
          ctx.lineTo(sx, sy);
          sy -= 20;
          ctx.lineTo(sx, sy);
        }
        ctx.stroke();

        // Right: Song Lab Continuous
        ctx.fillStyle = 'rgba(15, 23, 42, 0.8)';
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.6)';
        ctx.beginPath();
        ctx.roundRect(660, cardY, cardW, cardH, 12);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#10b981';
        ctx.font = 'bold 18px sans-serif';
        ctx.fillText('✓ Song Lab Continuous Riemannian Manifold', 690, cardY + 45);

        ctx.fillStyle = '#cbd5e1';
        ctx.font = '14px sans-serif';
        ctx.fillText('• Smooth sub-cent 22-shruti resolution (< 1.5 cents)', 690, cardY + 80);
        ctx.fillText('• Physics-informed vocal tract velocity constraints', 690, cardY + 110);
        ctx.fillText('• True continuous meends & 2.1 Hz andolan waves', 690, cardY + 140);
        ctx.fillText('• 87.2% reduction in intonation deviation', 690, cardY + 170);

        // Draw smooth golden curve
        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(690, cardY + 280);
        for (let x = 690; x <= 1160; x += 5) {
          const norm = (x - 690) / 470;
          const cy = cardY + 280 - 130 / (1 + Math.exp(-8 * (norm - 0.5))) + Math.sin(norm * 12 + t * 4) * 8;
          ctx.lineTo(x, cy);
        }
        ctx.stroke();

        ctx.restore();
      }

      // SCENE 2: Real-time 22-Shruti Dynamic Canvas & Universal Acoustic Engine
      function renderScene2(t) {
        ctx.save();
        ctx.textAlign = 'center';

        ctx.fillStyle = 'rgba(16, 185, 129, 0.15)';
        ctx.strokeStyle = '#10b981';
        ctx.beginPath();
        ctx.roundRect(W / 2 - 140, 95, 280, 30, 15);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#6ee7b7';
        ctx.font = 'bold 12px sans-serif';
        ctx.fillText('UNIVERSAL ACOUSTIC ENGINE', W / 2, 115);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 36px sans-serif';
        ctx.fillText('Real-Time 22-Shruti Pitch Ribbon', W / 2, 160);

        const insts = ['🎙️ Voice', '🪈 Bansuri Flute', '🪕 Sitar', '🎸 Guitar Strum', '🥁 Tabla & Live BPM'];
        const activeIdx = Math.floor(t * 1.2) % insts.length;
        let startX = W / 2 - 380;
        insts.forEach((inst, idx) => {
          const isActive = idx === activeIdx;
          ctx.fillStyle = isActive ? 'rgba(245, 158, 11, 0.25)' : 'rgba(255, 255, 255, 0.05)';
          ctx.strokeStyle = isActive ? '#f59e0b' : 'rgba(255, 255, 255, 0.15)';
          ctx.beginPath();
          ctx.roundRect(startX, 185, 140, 36, 18);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = isActive ? '#fbbf24' : '#94a3b8';
          ctx.font = (isActive ? 'bold' : 'normal') + ' 13px sans-serif';
          ctx.fillText(inst, startX + 70, 208);
          startX += 155;
        });

        const canY = 240;
        const canH = 390;
        ctx.fillStyle = '#0b0f19';
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.3)';
        ctx.beginPath();
        ctx.roundRect(60, canY, W - 120, canH, 12);
        ctx.fill();
        ctx.stroke();

        const shrutis = [
          { name: 'Sa (0c)', y: canY + canH - 40, col: '#f59e0b' },
          { name: 'r₁ Ekashruti (66c)', y: canY + canH - 85, col: '#64748b' },
          { name: 'r₂ Komal Re (112c)', y: canY + canH - 125, col: '#94a3b8' },
          { name: 'R₁ Chatusshruti (204c)', y: canY + canH - 175, col: '#38bdf8' },
          { name: 'g₂ Komal Ga (316c)', y: canY + canH - 225, col: '#94a3b8' },
          { name: 'G₂ Shuddha Ga (386c)', y: canY + canH - 275, col: '#38bdf8' },
          { name: 'M₂ Teevra Ma (590c)', y: canY + canH - 330, col: '#10b981' },
        ];

        shrutis.forEach(s => {
          ctx.strokeStyle = s.col === '#f59e0b' ? 'rgba(245, 158, 11, 0.5)' : 'rgba(255, 255, 255, 0.08)';
          ctx.setLineDash([4, 6]);
          ctx.beginPath();
          ctx.moveTo(70, s.y);
          ctx.lineTo(W - 70, s.y);
          ctx.stroke();
          ctx.setLineDash([]);

          ctx.fillStyle = s.col;
          ctx.font = '11px monospace';
          ctx.textAlign = 'left';
          ctx.fillText(s.name, 80, s.y - 6);
        });

        ctx.lineWidth = 4;
        ctx.strokeStyle = '#38bdf8';
        ctx.beginPath();
        for (let x = 70; x < W - 70; x += 6) {
          const norm = (x - 70) / (W - 140);
          const pitchWave = Math.sin(norm * 14 - t * 5) * 45 + Math.sin(norm * 4) * 80;
          const cy = canY + canH - 160 - pitchWave;
          if (x === 70) ctx.moveTo(x, cy);
          else ctx.lineTo(x, cy);
        }
        ctx.stroke();

        const headX = W - 140;
        const headNorm = (headX - 70) / (W - 140);
        const headY = canY + canH - 160 - (Math.sin(headNorm * 14 - t * 5) * 45 + Math.sin(headNorm * 4) * 80);
        ctx.fillStyle = '#f59e0b';
        ctx.beginPath();
        ctx.arc(headX, headY, 9, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
        ctx.strokeStyle = '#38bdf8';
        ctx.beginPath();
        ctx.roundRect(headX - 160, headY - 45, 150, 32, 6);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#38bdf8';
        ctx.font = 'bold 12px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('Ga: +384.2c (Δ -1.8c)', headX - 85, headY - 24);

        ctx.restore();
      }

      // SCENE 3: Real-Time Rasa & Affective Radar
      function renderScene3(t) {
        ctx.save();
        ctx.textAlign = 'center';

        ctx.fillStyle = 'rgba(217, 70, 239, 0.15)';
        ctx.strokeStyle = '#d946ef';
        ctx.beginPath();
        ctx.roundRect(W / 2 - 170, 95, 340, 30, 15);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#f0abfc';
        ctx.font = 'bold 12px sans-serif';
        ctx.fillText('AFFECTIVE REASONING & NATYASHASTRA', W / 2, 115);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 36px sans-serif';
        ctx.fillText('Real-Time Rasa & Affective Radar', W / 2, 160);

        const cx = 380;
        const cy = 410;
        const R = 170;

        ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(cx, cy, R, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(cx, cy, R * 0.66, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(cx, cy, R * 0.33, 0, Math.PI * 2);
        ctx.stroke();

        ctx.strokeStyle = 'rgba(255, 255, 255, 0.25)';
        ctx.beginPath();
        ctx.moveTo(cx - R - 20, cy);
        ctx.lineTo(cx + R + 20, cy);
        ctx.moveTo(cx, cy - R - 20);
        ctx.lineTo(cx + R + 20);
        ctx.stroke();

        ctx.font = 'bold 13px sans-serif';
        ctx.fillStyle = '#10b981';
        ctx.fillText('SHRINGARA (Love / Devotion)', cx + 100, cy + 45);
        ctx.fillStyle = '#38bdf8';
        ctx.fillText('SHANTA (Peace / Stillness)', cx - 90, cy + 120);
        ctx.fillStyle = '#f59e0b';
        ctx.fillText('VIRA / ADBHUTA (Heroic / Awe)', cx + 100, cy - 80);
        ctx.fillStyle = '#ef4444';
        ctx.fillText('RAUDRA (Fury / Intensity)', cx - 90, cy - 80);

        const orbProgress = Math.min(1.0, t / 7.0);
        const startAngle = Math.PI * 0.75;
        const targetAngle = Math.PI * 0.25;
        const currAngle = startAngle + (targetAngle - startAngle) * orbProgress;
        const orbR = 85 + Math.sin(t * 3) * 20;

        const orbX = cx + Math.cos(currAngle) * orbR;
        const orbY = cy + Math.sin(currAngle) * orbR;

        ctx.fillStyle = '#f59e0b';
        ctx.shadowColor = '#f59e0b';
        ctx.shadowBlur = 20;
        ctx.beginPath();
        ctx.arc(orbX, orbY, 12, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;

        const rx = 660;
        const rw = 540;

        ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
        ctx.strokeStyle = 'rgba(217, 70, 239, 0.4)';
        ctx.beginPath();
        ctx.roundRect(rx, 220, rw, 400, 14);
        ctx.fill();
        ctx.stroke();

        ctx.textAlign = 'left';
        ctx.fillStyle = '#f0abfc';
        ctx.font = 'bold 20px sans-serif';
        ctx.fillText('Continuous 2D Emotion Guidance (CFG)', rx + 35, 265);

        ctx.fillStyle = '#cbd5e1';
        ctx.font = '15px sans-serif';
        ctx.fillText('Song Lab models emotional vectors continuously:', rx + 35, 305);

        const items = [
          '• Continuous Valence V(t) in [-1, +1] & Arousal A(t)',
          '• Bharata Muni Natyashastra Chapter 29 mapping',
          '• Dynamic modulation: Karuna -> Shringara -> Shanta',
          '• Steers probability flow field in real time',
          '• Live affective radar feedback for vocalists & instrumentalists'
        ];
        items.forEach((item, idx) => {
          ctx.fillStyle = '#94a3b8';
          ctx.fillText(item, rx + 35, 345 + idx * 36);
        });

        const currentValence = (-0.75 + 1.45 * orbProgress).toFixed(2);
        const currentArousal = (-0.45 + 0.85 * orbProgress).toFixed(2);

        ctx.fillStyle = 'rgba(16, 185, 129, 0.2)';
        ctx.strokeStyle = '#10b981';
        ctx.beginPath();
        ctx.roundRect(rx + 35, 540, 210, 44, 8);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = '#34d399';
        ctx.font = 'bold 14px monospace';
        ctx.fillText('Valence: ' + currentValence + ' (Real)', rx + 50, 567);

        ctx.fillStyle = 'rgba(245, 158, 11, 0.2)';
        ctx.strokeStyle = '#f59e0b';
        ctx.beginPath();
        ctx.roundRect(rx + 270, 540, 210, 44, 8);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = '#fbbf24';
        ctx.fillText('Arousal: ' + currentArousal + ' (Live)', rx + 285, 567);

        ctx.restore();
      }

      // SCENE 4: AI Virtual Guru & Circadian Bio-Clock
      function renderScene4(t) {
        ctx.save();
        ctx.textAlign = 'center';

        ctx.fillStyle = 'rgba(245, 158, 11, 0.15)';
        ctx.strokeStyle = '#f59e0b';
        ctx.beginPath();
        ctx.roundRect(W / 2 - 160, 95, 320, 30, 15);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#fde68a';
        ctx.font = 'bold 12px sans-serif';
        ctx.fillText('CIRCADIAN NEURO-ENDOCRINE ALIGNMENT', W / 2, 115);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 36px sans-serif';
        ctx.fillText('AI Forensic Guru & 8-Prahara Clock', W / 2, 160);

        const dialX = 350;
        const dialY = 405;
        const dialR = 160;

        ctx.strokeStyle = 'rgba(245, 158, 11, 0.3)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(dialX, dialY, dialR, 0, Math.PI * 2);
        ctx.stroke();

        const praharas = ['Dawn (Bhairav)', 'Morning (Bilawal)', 'Noon (Sarang)', 'Afternoon (Multani)', 'Sunset (Marwa)', 'Night (Yaman)', 'Midnight (Darbari)', 'Late Night (Malkauns)'];
        praharas.forEach((p, idx) => {
          const ang = (idx * Math.PI * 2) / 8 - Math.PI / 2;
          const px = dialX + Math.cos(ang) * (dialR - 35);
          const py = dialY + Math.sin(ang) * (dialR - 35);

          ctx.fillStyle = idx === 5 ? '#f59e0b' : '#64748b';
          ctx.font = (idx === 5 ? 'bold 12px' : '10px') + ' sans-serif';
          ctx.fillText(p.split(' ')[0], px, py);
        });

        ctx.strokeStyle = '#f59e0b';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(dialX, dialY);
        const handAng = (5 * Math.PI * 2) / 8 - Math.PI / 2 + Math.sin(t) * 0.1;
        ctx.lineTo(dialX + Math.cos(handAng) * (dialR - 20), dialY + Math.sin(handAng) * (dialR - 20));
        ctx.stroke();

        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(dialX, dialY, 8, 0, Math.PI * 2);
        ctx.fill();

        const gx = 590;
        const gw = 610;

        ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.4)';
        ctx.beginPath();
        ctx.roundRect(gx, 215, gw, 410, 14);
        ctx.fill();
        ctx.stroke();

        ctx.textAlign = 'left';
        ctx.fillStyle = '#10b981';
        ctx.font = 'bold 20px sans-serif';
        ctx.fillText('✨ AI Guru Forensic Diagnostic Assessment', gx + 35, 260);

        ctx.fillStyle = '#f8fafc';
        ctx.font = 'bold 16px sans-serif';
        ctx.fillText('Identified Mode: Raga Yaman (Kalyan Thaat)', gx + 35, 295);

        ctx.fillStyle = '#cbd5e1';
        ctx.font = '14px sans-serif';
        const points = [
          '• Nyasa Resting Purity: 98.4% on Shuddha Gandhar (386 cents)',
          '• Tivra Madhyam Inflection: +592 cents (Sharp Prati Madhyam clean)',
          '• Meend Curvature: Sigmoidal optimal transport curvature confirmed',
          '• Gamak Frequency: 2.12 Hz (Within natural vocal resonance band)',
          '• Chronobiological Match: Optimal for Shashta Prahara (Sunset relaxation)'
        ];
        points.forEach((pt, idx) => {
          ctx.fillText(pt, gx + 35, 335 + idx * 34);
        });

        ctx.fillStyle = 'rgba(245, 158, 11, 0.15)';
        ctx.strokeStyle = '#f59e0b';
        ctx.beginPath();
        ctx.roundRect(gx + 35, 515, gw - 70, 75, 8);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#fbbf24';
        ctx.font = 'bold 13px sans-serif';
        ctx.fillText('💡 Actionable Guru Recommendation:', gx + 50, 542);
        ctx.fillStyle = '#fef3c7';
        ctx.font = '13px sans-serif';
        ctx.fillText('"Hold Mandra Nishad for 0.4s longer before gliding to Rishabh to evoke full Shringara."', gx + 50, 568);

        ctx.restore();
      }

      // SCENE 5: Research Lab: NEURO-RASA
      function renderScene5(t) {
        ctx.save();
        ctx.textAlign = 'center';

        ctx.fillStyle = 'rgba(56, 189, 248, 0.15)';
        ctx.strokeStyle = '#38bdf8';
        ctx.beginPath();
        ctx.roundRect(W / 2 - 160, 95, 320, 30, 15);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#7dd3fc';
        ctx.font = 'bold 12px sans-serif';
        ctx.fillText('R&D BREAKTHROUGH: NEURO-RASA', W / 2, 115);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 36px sans-serif';
        ctx.fillText('Publication-Grade Science vs. Big Tech', W / 2, 160);

        const cardW = 360;
        const cardH = 220;
        const cardY = 220;

        // Card 1
        ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
        ctx.strokeStyle = '#10b981';
        ctx.beginPath();
        ctx.roundRect(80, cardY, cardW, cardH, 12);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#10b981';
        ctx.font = 'bold 44px monospace';
        ctx.fillText('87.2%', 80 + cardW / 2, cardY + 70);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 18px sans-serif';
        ctx.fillText('Error Reduction', 80 + cardW / 2, cardY + 110);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '14px sans-serif';
        ctx.fillText('1.20c DTW RMSE vs 9.44c', 80 + cardW / 2, cardY + 145);
        ctx.fillText('in Discrete RVQ Codebooks', 80 + cardW / 2, cardY + 175);

        // Card 2
        ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
        ctx.strokeStyle = '#06b6d4';
        ctx.beginPath();
        ctx.roundRect(460, cardY, cardW, cardH, 12);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#06b6d4';
        ctx.font = 'bold 36px monospace';
        ctx.fillText('M = R x S¹', 460 + cardW / 2, cardY + 70);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 18px sans-serif';
        ctx.fillText('Riemannian Manifold Flow', 460 + cardW / 2, cardY + 110);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '14px sans-serif';
        ctx.fillText('Optimal Transport Straight Paths', 460 + cardW / 2, cardY + 145);
        ctx.fillText('Exact Continuous ODE Integration', 460 + cardW / 2, cardY + 175);

        // Card 3
        ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
        ctx.strokeStyle = '#f59e0b';
        ctx.beginPath();
        ctx.roundRect(840, cardY, cardW, cardH, 12);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#f59e0b';
        ctx.font = 'bold 44px monospace';
        ctx.fillText('PIKL', 840 + cardW / 2, cardY + 70);
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 18px sans-serif';
        ctx.fillText('Physics Kinematic Loss', 840 + cardW / 2, cardY + 110);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '14px sans-serif';
        ctx.fillText('Vocal Tract Velocity Limit', 840 + cardW / 2, cardY + 145);
        ctx.fillText('Zero Staircase Jerk Energy', 840 + cardW / 2, cardY + 175);

        const banY = 470;
        ctx.fillStyle = 'rgba(30, 41, 59, 0.7)';
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
        ctx.beginPath();
        ctx.roundRect(80, banY, W - 160, 150, 12);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#f8fafc';
        ctx.font = 'bold 18px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText('📄 Research Publication Manuscript Ready in research_lab/manuscript/', 110, banY + 45);

        ctx.fillStyle = '#94a3b8';
        ctx.font = '14px sans-serif';
        ctx.fillText('• Target Venues: IEEE/ACM TASLP / NeurIPS / ISMIR 2026', 110, banY + 80);
        ctx.fillText('• Complete LaTeX manuscript (main.tex) + 30+ peer-reviewed citations (references.bib)', 110, banY + 110);

        ctx.fillStyle = '#10b981';
        ctx.font = 'bold 14px sans-serif';
        ctx.textAlign = 'right';
        ctx.fillText('Strictly Excluded from Git (.gitignore) ✓', W - 110, banY + 45);

        ctx.restore();
      }

      // SCENE 6: Call to Action & Product Launch
      function renderScene6(t) {
        const alpha = Math.min(1, t * 1.2);
        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.textAlign = 'center';

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 64px sans-serif';
        ctx.fillText('SONG LAB', W / 2, 230);

        const tGrad = ctx.createLinearGradient(W / 2 - 250, 0, W / 2 + 250, 0);
        tGrad.addColorStop(0, '#10b981');
        tGrad.addColorStop(0.5, '#38bdf8');
        tGrad.addColorStop(1, '#f59e0b');
        ctx.fillStyle = tGrad;
        ctx.font = 'bold 28px sans-serif';
        ctx.fillText('Sing with Soul. Measure with Science.', W / 2, 285);

        ctx.fillStyle = '#94a3b8';
        ctx.font = '18px sans-serif';
        ctx.fillText('The world’s first microtonal AI vocal & musical intelligence workstation.', W / 2, 335);

        const pillW = 260;
        const pillH = 70;
        const pillY = 380;

        const pillars = [
          { title: '22-Shruti Engine', sub: 'Sub-cent live intonation' },
          { title: 'AI Forensic Guru', sub: 'Instantaneous critique' },
          { title: 'NEURO-RASA R&D', sub: 'Riemannian Flow Matching' },
          { title: 'Universal Tracker', sub: 'Voice, Flute, Sitar & Tabla' }
        ];

        let px = 80;
        pillars.forEach(p => {
          ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
          ctx.beginPath();
          ctx.roundRect(px, pillY, pillW, pillH, 10);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 16px sans-serif';
          ctx.fillText(p.title, px + pillW / 2, pillY + 30);
          ctx.fillStyle = '#94a3b8';
          ctx.font = '12px sans-serif';
          ctx.fillText(p.sub, px + pillW / 2, pillY + 52);
          px += pillW + 20;
        });

        const btnY = 500;
        const bGrad = ctx.createLinearGradient(W / 2 - 160, 0, W / 2 + 160, 0);
        bGrad.addColorStop(0, '#10b981');
        bGrad.addColorStop(1, '#06b6d4');
        ctx.fillStyle = bGrad;
        ctx.beginPath();
        ctx.roundRect(W / 2 - 180, btnY, 360, 60, 30);
        ctx.fill();

        ctx.fillStyle = '#07090e';
        ctx.font = 'bold 20px sans-serif';
        ctx.fillText('LAUNCH SONG LAB NOW', W / 2, btnY + 38);

        ctx.fillStyle = '#64748b';
        ctx.font = '14px monospace';
        ctx.fillText('Local-First MIR Workstation • Zero Cloud Latency • Available Now', W / 2, 600);

        ctx.restore();
      }

      requestAnimationFrame(render);
    }

    startProduction().catch(console.error);
  </script>
</body>
</html>
  `;

  await page.eval((html) => {
    document.open();
    document.write(html);
    document.close();
  }, htmlContent);

  console.log(`Recording marketing video with studio master audio (${durationSec} seconds)...`);

  const checkInterval = 2000;
  const maxWaitMs = (durationSec + 25) * 1000;
  let elapsed = 0;

  while (elapsed < maxWaitMs) {
    await sleep(checkInterval);
    elapsed += checkInterval;

    const isDone = await page.eval(() => window.__recordingFinished);
    process.stdout.write(`  • Recording progress: ${Math.round(elapsed / 1000)}s / ${durationSec}s...\r`);

    if (isDone) {
      console.log('\nRecording completed inside browser! Fetching base64 video payload...');
      break;
    }
  }

  console.log('Capturing marketing poster screenshots...');
  const posterPath = resolve('marketing_poster.png');
  await page.screenshot({ path: posterPath, format: 'png' });
  console.log(`Poster image saved to: ${posterPath}`);

  const dataUrl = await page.eval(() => window.__recordingDataUrl);
  if (!dataUrl) {
    throw new Error('No video data captured from MediaRecorder.');
  }

  const base64Data = dataUrl.split(',')[1];
  const videoBuffer = Buffer.from(base64Data, 'base64');
  const videoPath = resolve('marketing_demo.webm');
  writeFileSync(videoPath, videoBuffer);

  console.log('===============================================================');
  console.log(`SUCCESS! Official marketing video re-rendered with authentic soundtrack:`);
  console.log(`  File: ${videoPath}`);
  console.log(`  Size: ${(videoBuffer.length / (1024 * 1024)).toFixed(2)} MB`);
  console.log(`  Audio: Multi-track Acoustic Indian Classical Master (Miraj Tanpura, Sitar, Flute, Tabla, Vocal)`);
  console.log(`  Duration: ~42 seconds`);
  console.log('===============================================================');

  await browser.close();
  server.close();
}

main().catch(err => {
  console.error('Fatal error generating marketing video:', err);
  process.exit(1);
});
