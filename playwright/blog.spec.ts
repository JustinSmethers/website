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

test('filters posts by tag', async ({ page }) => {
  await page.goto('/blog/');

  const filterButtons = page.locator('[data-filter-tag]');
  await expect(filterButtons.first()).toBeVisible();
  const buttonCount = await filterButtons.count();
  expect(buttonCount).toBeGreaterThan(1);

  const targetButton = filterButtons.nth(1);
  const targetTag = await targetButton.getAttribute('data-filter-tag');
  expect(targetTag).toBeTruthy();
  const selectedTag = targetTag as string;

  await targetButton.click();

  const visibility = await page.$$eval('.post-list-item', items =>
    items.map(item => {
      const style = window.getComputedStyle(item as HTMLElement);
      const tags = (item as HTMLElement).dataset.tags?.split(',').filter(Boolean) ?? [];
      return {
        visible: style.display !== 'none',
        tags,
      };
    }),
  );

  const visible = visibility.filter(item => item.visible);
  expect(visible.length).toBeGreaterThan(0);
  visible.forEach(item => expect(item.tags).toContain(selectedTag));

  await page.getByRole('button', { name: 'All' }).click();

  const visibleAfterReset = await page.$$eval('.post-list-item', items =>
    items.filter(item => window.getComputedStyle(item as HTMLElement).display !== 'none').length,
  );
  expect(visibleAfterReset).toBeGreaterThanOrEqual(visible.length);
});
