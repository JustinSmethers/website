import { test, expect } from '@playwright/test';

test('blog listing loads', async ({ page }) => {
  await page.goto('/blog/');

  await expect(page.getByRole('link', { name: 'Justin Smethers' })).toBeVisible();
  await expect(page.getByText("I'm Justin", { exact: false })).toBeVisible();
  await expect(page.locator('.profile-banner')).toBeVisible();
  await expect(page.getByAltText('Justin Smethers profile')).toBeVisible();

  const posts = await page.$$eval('.post-card', cards =>
    cards.map(card => ({
      title: card.querySelector('h2')?.textContent?.trim(),
      desc: card.querySelector('p')?.textContent?.trim(),
      tags: Array.from(card.querySelectorAll('.tag')).map(el => el.textContent?.trim()),
    })),
  );

  console.log('Playwright saw blog posts:', JSON.stringify(posts, null, 2));

  await page.screenshot({ path: 'playwright/.artifacts/blog.png', fullPage: true });
});
