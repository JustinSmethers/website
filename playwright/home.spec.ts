import { test, expect } from '@playwright/test';

test('homepage identifies Justin and links to his work', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveTitle('Justin Smethers | Senior Analytics Engineer');
  await expect(page.getByRole('heading', { name: 'Justin Smethers' })).toBeVisible();
  await expect(page.getByText('I’m a senior analytics engineer at Brooklyn Data.', { exact: false })).toBeVisible();
  await expect(page.getByAltText('Justin Smethers profile')).toBeVisible();
  await expect(page.getByRole('link', { name: 'Read the blog' })).toHaveAttribute('href', '/blog/');
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', 'https://www.justinsmethers.com/');
  const profile = JSON.parse(await page.locator('script[type="application/ld+json"]').innerText());
  expect(profile['@type']).toBe('ProfilePage');
  expect(profile.mainEntity).toMatchObject({
    '@type': 'Person',
    name: 'Justin Smethers',
    sameAs: [
      'https://www.linkedin.com/in/justinsmethers/',
      'https://github.com/JustinSmethers',
    ],
  });
});
