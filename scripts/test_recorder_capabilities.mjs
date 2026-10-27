import { Browser } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function test() {
  console.log('Launching browser...');
  const browser = await Browser.launch({ width: 1280, height: 720 });
  const page = await browser.newPage({ width: 1280, height: 720 });
  
  console.log('Evaluating MediaRecorder test...');
  const result = await page.eval(async () => {
    return {
      hasMediaRecorder: typeof MediaRecorder !== 'undefined',
      vp8Supported: typeof MediaRecorder !== 'undefined' && MediaRecorder.isTypeSupported('video/webm;codecs=vp8'),
      canvasCapture: typeof HTMLCanvasElement.prototype.captureStream === 'function',
      audioContext: typeof AudioContext !== 'undefined'
    };
  });
  
  console.log('Capabilities:', result);
  await browser.close();
}

test().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
