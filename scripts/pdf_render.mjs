import puppeteer from 'puppeteer';

const chromePath = process.env.PUPPETEER_EXECUTABLE_PATH;
const outDir = 'C:/Users/Game pc/Desktop/Website bouwer claude code/temporary screenshots/';

const browser = await puppeteer.launch({
  headless: true,
  executablePath: chromePath || undefined,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
});

const page = await browser.newPage();
await page.setViewport({ width: 1300, height: 950 });
await page.goto('http://localhost:3000/pdfview.html', { waitUntil: 'networkidle0', timeout: 30000 });
await page.waitForFunction('window.pageRendered === true', { timeout: 45000 });

const total = await page.evaluate(() => window.totalPages);
console.log('Total pages:', total);

for (let i = 1; i <= total; i++) {
  await page.evaluate((n) => window.goToPage(n), i);
  await page.waitForFunction('window.pageRendered === true', { timeout: 20000 });
  await new Promise(r => setTimeout(r, 1000));
  const canvasEl = await page.$('canvas');
  const num = String(i).padStart(2, '0');
  await canvasEl.screenshot({ path: outDir + 'pdf-p' + num + '.png' });
  console.log('Page', i, 'of', total, 'saved');
}

await browser.close();
console.log('Done - all pages rendered');
