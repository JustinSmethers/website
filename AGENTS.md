# Repository Guidelines

## Project Structure & Module Organization
- `manage.py` runs the Django entrypoint; core settings live in `buzzz/`.
- Primary app code is under `blog/` (models, views, forms, templates, static assets, and `tests.py`).
- Blog content is markdown with YAML front matter in `blog_posts/`; templates are also shared in `templates/`.
- Helper scripts live in `scripts/` (e.g., `generate_pygments_css.py`, `validate_tags.py`); Playwright specs sit in `playwright/` with config in `playwright.config.ts`.
- Test artifacts from Playwright land in `test-results/`; static output from scripts goes to `blog/static/pygments.css`.

## Build, Test, and Development Commands
- Create env and install deps: `uv venv && source .venv/bin/activate && uv pip install -r requirements.txt`.
- Run the dev server: `uv run python manage.py runserver 0.0.0.0:8000`.
- Apply migrations: `uv run python manage.py migrate`; create superuser: `uv run python manage.py createsuperuser`.
- Django tests: `uv run python manage.py test`.
- E2E tests (needs server; Playwright auto-starts one): `npm test` or `npx playwright test`; headed/UI modes via `npm run test:e2e:headed` or `npm run test:e2e:ui`.
- Validate blog tags: `uv run python scripts/validate_tags.py`; regenerate syntax CSS: `uv run python scripts/generate_pygments_css.py`.

## Coding Style & Naming Conventions
- Follow Django/PEP 8 defaults: 4-space indentation, snake_case for Python, PascalCase for classes, and meaningful verbose names for model fields.
- Keep templates and static files mirrored by feature (e.g., `blog/templates/blog/*.html`, `blog/static/blog/...`).
- Prefer type hints in new Python code and small, focused view functions; avoid global state in settings.
- Keep Playwright spec names descriptive (e.g., `home.spec.ts`, `blog.spec.ts`) and colocate helper selectors near tests.

## Testing Guidelines
- Unit/integration tests live in `blog/tests.py`; use Django’s `TestCase` and fixture data when needed.
- Name tests by behavior (`test_renders_homepage`, `test_requires_auth_for_admin`); prefer one assertion focus per test.
- Playwright specs expect a running server via `webServer` in `playwright.config.ts`; keep selectors resilient (roles/text over CSS when possible).
- Add tests for new views, forms, or templates; ensure blog tag validation passes for new posts.
- Validate UI-facing changes with Playwright before submitting (`npm test` or `npx playwright test`) and attach traces if failures occur.

## Commit & Pull Request Guidelines
- Commits in history use short, imperative summaries (“remove img”, “simplify layout”); follow that style and keep scope tight.
- Reference related issues in commit bodies if applicable; avoid committing secrets or `.env` files.
- Pull requests should describe intent, list key changes, and note how to verify (commands run, screenshots for UI-facing changes).
- Include test coverage notes: which Django/Playwright suites ran and results; mention migrations or data impacts explicitly.
