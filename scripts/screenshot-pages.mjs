import puppeteer from 'puppeteer';

const chromePath = `C:\\Users\\Game pc\\.cache\\puppeteer\\chrome-headless-shell\\win64-146.0.7680.153\\chrome-headless-shell-win64\\chrome-headless-shell.exe`;
const browser = await puppeteer.launch({ headless: true, executablePath: chromePath, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
const page = await browser.newPage();
await page.setViewport({ width: 794, height: 1123, deviceScaleFactor: 2 });
await page.goto('http://localhost:3000/Smart11/html_pages/ebook-smart11-base-v3.html', { waitUntil: 'networkidle0', timeout: 30000 });
await new Promise(r => setTimeout(r, 2500));

const pages = ['cover', 'intro', 'basis', 'walkthrough', 'tips', 'cta'];
for (let i = 0; i < 6; i++) {
  await page.screenshot({
    path: `scripts/temporary screenshots/v3-p${i+1}-${pages[i]}.png`,
    clip: { x: 0, y: i * 1123, width: 794, height: 1123 }
  });
  console.log(`Page ${i+1} done`);
}

await browser.close();
console.log('All pages screenshotted');
