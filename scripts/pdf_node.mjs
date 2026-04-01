import pdfjsLib from 'pdfjs-dist/legacy/build/pdf.mjs';
import { createCanvas } from 'canvas';
import fs from 'fs';
import path from 'path';

pdfjsLib.GlobalWorkerOptions.workerSrc = '';

const pdfPath = String.raw`C:\Users\Game pc\Desktop\Website bouwer claude code\Referentie_afbeeldingen\T2024010_SMART11_BASIS_HUISSTIJLHANDBOEK (1).pdf`;
const outDir = String.raw`C:\Users\Game pc\Desktop\Website bouwer claude code\temporary screenshots`;

const data = new Uint8Array(fs.readFileSync(pdfPath));
const pdf = await pdfjsLib.getDocument({ data, disableWorker: true }).promise;
console.log('Pages:', pdf.numPages);

for(let i = 1; i <= Math.min(10, pdf.numPages); i++) {
  const page = await pdf.getPage(i);
  const scale = 2;
  const vp = page.getViewport({ scale });
  const canvas = createCanvas(vp.width, vp.height);
  const ctx = canvas.getContext('2d');
  await page.render({ canvasContext: ctx, viewport: vp }).promise;
  const buf = canvas.toBuffer('image/png');
  fs.writeFileSync(path.join(outDir, `pdf-p${String(i).padStart(2,'0')}.png`), buf);
  console.log('Saved page', i);
}
