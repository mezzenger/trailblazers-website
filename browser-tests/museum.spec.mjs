import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { readFileSync } from 'node:fs';

const profileCount = JSON.parse(readFileSync('content/profiles.json', 'utf8')).length;

test('homepage, collection, filters, timeline, and keyboard path', async ({ page }, testInfo) => {
  await page.goto('./');
  await expect(page).toHaveTitle(/Trailblazers of History/);
  await expect(page.locator('#card-grid .person-card')).toHaveCount(profileCount);
  await expect(page.locator('#result-count')).toHaveText(`Showing ${profileCount} people`);
  await page.locator('#search').fill('parity violation');
  await page.locator('#category').selectOption('Science & Innovation');
  await page.locator('#era').selectOption('20th century');
  await page.locator('#region').selectOption('Asia');
  await expect(page.locator('#card-grid .person-card:visible')).toHaveCount(1);
  await expect(page.locator('#card-grid .person-card:visible')).toContainText('Chien-Shiung Wu');
  await page.locator('#search').fill('no matching biography');
  await expect(page.locator('#empty-state')).toBeVisible();
  await page.locator('#clear-filters').click();
  await expect(page.locator('#empty-state')).toBeHidden();
  await expect(page.locator('#search')).toBeFocused();
  await expect(page.locator('#card-grid .person-card:visible')).toHaveCount(profileCount);
  await page.locator('[data-category-jump="Medicine & Public Health"]').click();
  await expect(page.locator('#category')).toHaveValue('Medicine & Public Health');
  const medicineCount = JSON.parse(readFileSync('content/profiles.json', 'utf8')).filter(person => person.categories.includes('Medicine & Public Health')).length;
  await expect(page.locator('#card-grid .person-card:visible')).toHaveCount(medicineCount);
  await page.locator('#clear-filters').click();

  await page.locator('#timeline-range').evaluate(element => {
    element.value = '1900';
    element.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await expect(page.locator('#timeline-output')).toHaveText('1900');
  await expect(page.locator('#timeline-list li:visible').first()).toBeVisible();
  await page.locator('#timeline-range').evaluate(element => {
    element.value = element.max;
    element.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await page.keyboard.press('Home');
  await page.keyboard.press('Tab');
  const focused = await page.evaluate(() => document.activeElement?.tagName);
  expect(['A', 'BUTTON', 'INPUT', 'SELECT']).toContain(focused);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  expect(overflow).toBe(false);
  await page.screenshot({ path: testInfo.outputPath(`home-${testInfo.project.name}.png`), fullPage: true });
});

test('production profile route, portrait, source links, and accessibility', async ({ page }, testInfo) => {
  await page.goto('people/mary-jackson/');
  await expect(page).toHaveURL(/\/trailblazers-website\/people\/mary-jackson\/$/);
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Mary Jackson');
  await expect(page.locator('.profile-art img')).toBeVisible();
  await expect(page.locator('.source-list a')).toHaveCount(2);
  await expect(page.getByRole('link', { name: /Image record/ })).toHaveAttribute('href', /commons.wikimedia.org/);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  expect(overflow).toBe(false);
  await page.screenshot({ path: testInfo.outputPath(`profile-${testInfo.project.name}.png`), fullPage: true });
  const audit = await new AxeBuilder({ page }).analyze();
  expect(audit.violations).toEqual([]);
});

test('profile without a rights-cleared portrait uses an accessible typographic placeholder', async ({ page }, testInfo) => {
  await page.goto('people/jane-c-wright/');
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Jane C. Wright');
  const placeholder = page.locator('.profile-art[role="img"]');
  await expect(placeholder).toBeVisible();
  await expect(placeholder).toHaveAttribute('aria-label', 'Portrait not shown for Jane C. Wright');
  await expect(page.locator('.profile-art img')).toHaveCount(0);
  await page.screenshot({ path: testInfo.outputPath(`placeholder-profile-${testInfo.project.name}.png`), fullPage: true });
  const audit = await new AxeBuilder({ page }).analyze();
  expect(audit.violations).toEqual([]);
});

test('homepage accessibility in both themes and reduced motion', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('./');
  for (const theme of ['light', 'dark']) {
    if (theme === 'dark') await page.getByRole('button', { name: 'Toggle color theme' }).click();
    const audit = await new AxeBuilder({ page }).analyze();
    expect(audit.violations, `${theme}: ${JSON.stringify(audit.violations.map(v => v.id))}`).toEqual([]);
  }
});
