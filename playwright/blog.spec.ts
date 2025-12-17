import { test, expect } from '@playwright/test';

test('blog listing loads', async ({ page }) => {
  await page.goto('/blog/');

  await expect(page.getByRole('link', { name: 'Justin Smethers' })).toBeVisible();
  await expect(page.getByText("I'm Justin", { exact: false })).toBeVisible();
  await expect(page.locator('.profile-banner')).toBeVisible();
  await expect(page.getByAltText('Justin Smethers profile')).toBeVisible();

  const posts = await page.$$eval('.post-list-item', items =>
    items.map(item => ({
      title: item.querySelector('.post-list-title')?.textContent?.trim(),
      blurb: item.querySelector('.post-list-blurb')?.textContent?.trim(),
      date: item.querySelector('.post-date')?.textContent?.trim(),
    })),
  );

  console.log('Playwright saw blog posts:', JSON.stringify(posts, null, 2));

  await page.screenshot({ path: 'playwright/.artifacts/blog.png', fullPage: true });
});
