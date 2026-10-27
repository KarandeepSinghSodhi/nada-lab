import { Browser } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

async function test() {
  const wavPath = resolve('marketing_soundtrack.wav');
  const wavBuffer = readFileSync(wavPath);
  const audioBase64 = wavBuffer.toString('base64');

  const browser = await Browser.launch({ width: 1280, height: 720 });
  const page = await browser.newPage({ width: 1280, height: 720 });

  const result = await page.eval(async (b64) => {
    try {
      const audioCtx = new AudioContext();
      const dest = audioCtx.createMediaStreamDestination();

      const binaryStr = atob(b64.slice(0, 500000)); // test decode 500kb
      const bytes = new Uint8Array(binaryStr.length);
      for (let i = 0; i < binaryStr.length; i++) bytes[i] = binaryStr.charCodeAt(i);

      // Need clean wav slice or full buffer
      return { success: true, byteLen: bytes.length };
    } catch (e) {
      return { error: e.message };
    }
  }, audioBase64);

  console.log('Test decode result:', result);
  await browser.close();
}

test().catch(console.error);
