/* Run against `python3 -m http.server 8765` with Playwright on NODE_PATH. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.DOCUMENT_TEST_URL || 'http://127.0.0.1:8765';
let passed = 0;
function check(condition, message) { assert.ok(condition, message); passed++; }

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(`${base}/pages/developer-docs.html`, { waitUntil: 'domcontentloaded' });
    await page.locator('#document-search-controls').waitFor({ state: 'visible' });
    await page.evaluate(() => document.fonts.ready);
    const first = await page.locator('#document-browse a[href="../docs/pulsetrackr-support.html"]').boundingBox();
    check(first.y + first.height <= 812, `First document ends at ${first.y + first.height}`);
    check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'Mobile overflow');
    const input = page.locator('#document-search-input');
    await input.fill('PulseTrackr SOS');
    await page.waitForTimeout(300);
    check((await page.locator('.search-result').count()) > 0, 'Multiword search has results');
    check((await page.locator('.search-result').allTextContents()).every(t => t.includes('PulseTrackr')), 'Product restriction respected');
    check(await page.locator('.search-result a[href$="#sos"]').count() > 0, 'SOS section is linked');
    check(new URL(page.url()).searchParams.get('q') === 'PulseTrackr SOS', 'Query persisted');
    await page.locator('[data-document-type="support"]').click();
    await page.waitForTimeout(100);
    check(await page.locator('.search-result').count() === 1, 'Product + support returns one grouped document');
    check(await page.locator('[data-document-type="support"]').getAttribute('aria-pressed') === 'true', 'Filter state accessible');
    const shareURL = page.url();
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.locator('.search-result').waitFor();
    check(await input.inputValue() === 'PulseTrackr SOS' && page.url() === shareURL, 'Shared state restored');
    await page.locator('#document-search-clear').click();
    check(await page.locator('#document-browse').isVisible() && await input.inputValue() === '', 'Clear restores browse');
    check(await input.evaluate(el => el === document.activeElement), 'Clear returns focus');
    await page.locator('[data-document-type="terms"]').click();
    await page.waitForTimeout(100);
    check(await page.locator('.search-result').count() === 2, 'Two maintained terms documents');
    check((await page.locator('.search-result').first().textContent()).includes('PulseTrackr'), 'Filter results follow browse product order');
    await page.locator('#document-search-clear').click();
    await input.fill('jxl routes');
    await page.waitForTimeout(300);
    check((await page.locator('.search-result').allTextContents()).every(t => t.includes('JxL Scheduler')) && await page.locator('.search-result').count() > 0, 'JxL body query');
    await input.fill('zzzz-no-such-document');
    await page.waitForTimeout(300);
    check(await page.locator('.search-result').count() === 0 && /no|0/i.test(await page.locator('#document-search-status').textContent()), 'Empty state');
    await input.fill('<img src=x onerror=alert(1)>');
    await page.waitForTimeout(300);
    check(await page.locator('#document-search-results img').count() === 0, 'Query remains text');
    await page.locator('#document-search-clear').click();
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.reload({ waitUntil: 'domcontentloaded' });
    await page.locator('#document-search-controls').waitFor({ state: 'visible' });
    check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'Desktop overflow');
    for (const file of fs.readdirSync(path.join(__dirname, '../docs')).filter(f => f.endsWith('.html'))) {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto(`${base}/docs/${file}`, { waitUntil: 'domcontentloaded' });
      check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `${file} overflow`);
    }
    await page.goto(`${base}/docs/pulsetrackr-support.html#sos`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(300);
    check(await page.locator('#sos').evaluate(el => el.getBoundingClientRect().top >= document.querySelector('.navbar').getBoundingClientRect().bottom), 'Section clears fixed header');
    await page.goto(`${base}/pages/developer-docs.html?q=SOS&type=constructor`, { waitUntil: 'domcontentloaded' });
    await page.locator('.search-result').first().waitFor();
    check(await page.locator('[data-document-type="all"]').getAttribute('aria-pressed') === 'true', 'Invalid URL filter defaults to All');
    const noJS = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 375, height: 812 } });
    const fallback = await noJS.newPage();
    await fallback.goto(`${base}/pages/developer-docs.html`);
    check(await fallback.locator('#document-browse').isVisible() && await fallback.locator('#document-browse a').count() === 15, 'No-JS browse intact');
    await noJS.close();
    await page.route('**/assets/document-index.json*', route => route.abort());
    await page.goto(`${base}/pages/developer-docs.html`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(300);
    check(await page.locator('#document-browse').isVisible() && await page.locator('#document-search-status').isVisible(), 'Index failure is explained and browse survives');
    check(errors.length === 0, `Runtime errors: ${errors.join(', ')}`);
    console.log(`${passed} browser checks passed`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
