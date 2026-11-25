import { test, expect } from '@playwright/test';

test('published post pages and local images are available', async ({ page, request }) => {
  test.setTimeout(90_000);
  await page.goto('/');
  const postLinks = await page.locator('.post-list-item > a').evaluateAll(links =>
    links.map(link => (link as HTMLAnchorElement).href),
  );
  expect(postLinks.length).toBeGreaterThan(0);
  for (const link of postLinks) {
    await page.goto(link, { waitUntil: 'domcontentloaded' });
    const title = page.locator('.post-title');
    await expect(title).toBeVisible();
    await expect(page).toHaveTitle(`${(await title.innerText()).trim()} | Justin Smethers`);
    await expect(page.locator('a[rel="author"]')).toHaveAttribute('href', '/');
    await expect(page.locator('.back-button')).toHaveAttribute('href', '/');
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
      'href',
      `https://justinsmethers.com${new URL(link).pathname}`,
    );
    await expect(page.locator('.post-content')).not.toBeEmpty();
    const imagePaths = await page.locator('img[src^="/static/"]').evaluateAll(images =>
      images.map(image => (image as HTMLImageElement).src),
    );
    for (const path of imagePaths) {
      const response = await request.get(path);
      expect(response.status(), path).toBe(200);
      expect(response.headers()['content-type'], path).toMatch(/^image\//);
    }
  }
});

test('static export preserves legacy redirects and returns 404 for unpublished pages', async ({ request }) => {
  test.skip(!process.env.STATIC_SITE && !process.env.PLAYWRIGHT_BASE_URL, 'Static hosting check');
  const root = await request.get('/', { maxRedirects: 0 });
  expect(root.status()).toBe(200);
  const oldBlog = await request.get('/blog/', { maxRedirects: 0 });
  expect(oldBlog.status()).toBe(200);
  expect(await oldBlog.text()).toBe(await root.text());
  for (const [oldName, newName] of [
    ['evcontainers', 'devcontainers'],
    ['odern-python-packaging-with-uv', 'modern-python-packaging-with-uv'],
    ['terminal-agents-just-got-scary-goo', 'terminal-agents-just-got-scary-good'],
  ]) {
    const response = await request.get(`/blog/post/${oldName}/`, { maxRedirects: 0 });
    expect(response.status()).toBe(301);
    expect(response.headers()['location']).toMatch(new RegExp(`/blog/post/${newName}/$`));
  }
  for (const path of ['/blog/post/missing-post/', '/admin/', '/.env', '/static/blog_posts/devcontainers/devcontainers.md']) {
    const response = await request.get(path);
    expect(response.status(), path).toBe(404);
  }
});

test('blog listing loads', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('link', { name: 'Justin Smethers' })).toBeVisible();
  await expect(page.locator('.profile-banner')).toBeVisible();
  await expect(page.getByAltText('Justin Smethers profile')).toBeVisible();

  const posts = await page.$$eval('.post-list-item', items =>
    items.map(item => ({
      title: item.querySelector('.post-list-title')?.textContent?.trim(),
      blurb: item.querySelector('.post-list-blurb')?.textContent?.trim(),
      date: item.querySelector('.post-date')?.textContent?.trim(),
    })),
  );

  expect(posts.length).toBeGreaterThan(0);
  console.log('Playwright saw blog posts:', JSON.stringify(posts, null, 2));

  await page.screenshot({ path: 'playwright/.artifacts/blog.png', fullPage: true });
});

test('filters posts by tag', async ({ page }) => {
  await page.goto('/');

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

test('static sitemap lists the blog homepage and every post', async ({ page, request }) => {
  test.skip(!process.env.STATIC_SITE && !process.env.PLAYWRIGHT_BASE_URL, 'Static hosting check');
  const origin = 'https://justinsmethers.com';

  await page.goto('/');
  const postPaths = await page.locator('.post-list-item > a').evaluateAll(links =>
    links.map(link => new URL((link as HTMLAnchorElement).href).pathname),
  );

  const robots = await request.get('/robots.txt');
  expect(robots.status()).toBe(200);
  expect(await robots.text()).toContain(`Sitemap: ${origin}/sitemap.xml`);

  const sitemap = await request.get('/sitemap.xml');
  expect(sitemap.status()).toBe(200);
  const xml = await sitemap.text();
  const locations = Array.from(xml.matchAll(/<loc>([^<]+)<\/loc>/g), match => match[1]);
  expect(locations.sort()).toEqual(['/', ...postPaths].map(path => origin + path).sort());
});
