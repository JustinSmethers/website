import { test, expect } from '@playwright/test';

test('home page renders and shows intro text', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('link', { name: 'Justin Smethers' })).toBeVisible();
  await expect(page.getByText("I'm Justin", { exact: false })).toBeVisible();
  await expect(page.locator('.profile-banner')).toBeVisible();
  await expect(page.getByAltText('Justin Smethers profile')).toBeVisible();
});
