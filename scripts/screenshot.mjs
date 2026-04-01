import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const screenshotsDir = path.join(__dirname, 'temporary screenshots');

if (!fs.existsSync(screenshotsDir)) {
  fs.mkdirSync(screenshotsDir, { recursive: true });
}

const url = process.argv[2] || 'http://localhost:3000';
const label = process.argv[3] || '';

// Find next available screenshot number
const existing = fs.readdirSync(screenshotsDir)
  .filter(f => f.startsWith('screenshot-') && f.endsWith('.png'))
  .map(f => parseInt(f.match(/screenshot-(\d+)/)?.[1] || '0', 10))
  .filter(n => !isNaN(n));
const nextN = existing.length > 0 ? Math.max(...existing) + 1 : 1;
const filename = label
  ? `screenshot-${nextN}-${label}.png`
  : `screenshot-${nextN}.png`;
const outputPath = path.join(screenshotsDir, filename);

// Use chrome-headless-shell if available
let chromePath = process.env.PUPPETEER_EXECUTABLE_PATH;
if (!chromePath) {
  const headlessShell = `C:\\Users\\Game pc\\.cache\\puppeteer\\chrome-headless-shell\\win64-146.0.7680.153\\chrome-headless-shell-win64\\chrome-headless-shell.exe`;
  if (fs.existsSync(headlessShell)) {
    chromePath = headlessShell;
  }
}

const browser = await puppeteer.launch({
  headless: true,
  executablePath: chromePath,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
});

const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1.5 });
await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
await new Promise(r => setTimeout(r, 1500));
// Force all animated elements visible for full-page screenshots
await page.evaluate(() => {
  document.querySelectorAll('.fade-up').forEach(el => el.classList.add('visible'));
});
await new Promise(r => setTimeout(r, 300));
await page.screenshot({ path: outputPath, fullPage: true });

await browser.close();
console.log(`Screenshot opgeslagen: ${outputPath}`);
