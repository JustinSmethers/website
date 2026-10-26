# Tagging Feature Implementation Plan

## Goals
- Display standardized pill-style tags (`post`, `WIP`, `talk`, `notes`) alongside blog posts on list and detail views.
- Source tag metadata from the Markdown front matter that already feeds titles and descriptions.
- Ensure only the approved tag vocabulary is used by introducing automated checks (pre-commit or CI).

## Current State Overview
- Blog entries are populated from GitHub Markdown via `fetch_github_md` (YAML front matter parsed, but tags are currently ignored) and stored in the `BlogPost` model (`blog/models.py`).
- Templates under `blog/templates/blog/` render the post list (`blog_layout.html`) and detail (`blog_detail.html`) views without tag support.
- No styling exists for tag badges, and no tests or hooks enforce allowed tag values.

## Implementation Steps

### 1. Data Model & Migration
1. Add a `tags` field to `BlogPost` (e.g., `ArrayField` on PostgreSQL or `JSONField` for portability). Default to an empty list.
2. Generate and apply a schema migration.
3. Update the Django admin (if used) to surface the new field.

### 2. Markdown Ingestion Updates
1. Extend `fetch_github_md.Command.parse_markdown` usage to pull a `tags` list from front matter.
2. Normalize tags (trim whitespace, lowercase) and filter out values outside the approved set.
3. Update `BlogPost.objects.update_or_create` defaults to include the normalized tag list.
4. Add logging/warnings when front matter contains disallowed tags so authors get feedback during the refresh command.

### 3. Template Rendering
1. Modify `blog/templates/blog/blog_layout.html` and `blog/templates/blog/blog_detail.html` to iterate over `post.tags` and render pill elements near the title or metadata area.
2. Ensure tags gracefully degrade (no markup) when the list is empty.

### 4. Styling
1. Define reusable pill styles in a global stylesheet (`blog/static/blog/...` or the main CSS file). Each tag type should have a distinct color consistent with the design system.
2. Use utility classes (e.g., `tag tag--post`) to map tag values to colors.
3. Verify responsive behavior and contrast accessibility.

### 5. Content Updates
1. Update existing Markdown posts in `blog_posts/**/` to include a `tags:` front matter entry that matches the approved vocabulary.
2. Document the expected front matter structure (e.g., in `readme.md`).

### 6. Automated Enforcement
1. Introduce a configuration file (e.g., `scripts/validate_tags.py`) that parses Markdown front matter and asserts every declared tag is in `{post, WIP, talk, notes}`.
2. Add a unit test under `blog/tests.py` (or a new test module) that covers:
   - Metadata parsing and normalization logic.
   - Rendering helper (if a serializer/helper is introduced) returns the right classes.
3. Wire the validator into automation:
   - Option A: Add a pre-commit hook entry invoking the validation script.
   - Option B: Add a Django/Pytest test invoked in CI.
   - Prefer both so contributors receive quick feedback locally and CI enforces consistency.
4. Document how to install the pre-commit hook if the repo does not already use `pre-commit`.

### 7. Manual Verification
1. Run the refresh command to repopulate posts and confirm tags appear.
2. Check the blog pages in the browser to verify pill styling.
3. Capture a screenshot for documentation if needed.

## Open Questions / Follow-Ups
- Confirm database backend (ArrayField availability). If SQLite is used locally, prefer `JSONField` plus application-level validation.
- Determine whether tags should influence filtering or navigation in future iterations (out of scope for initial pass but should influence CSS class naming).

## Deliverables
- Updated Django model, ingestion command, templates, CSS, and Markdown content.
- Automated validation for tag vocabulary in Markdown front matter.
- Documentation updates explaining the tag workflow and validation.
