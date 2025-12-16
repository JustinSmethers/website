# Buzzz Website

Documentation for developing the Buzzz Django application.

## Prerequisites

- Python 3.11 or newer
- PostgreSQL running locally (or accessible remotely)
- [`uv`](https://docs.astral.sh/uv/) for managing the Python environment and dependencies

## Initial Setup

1. **Create and activate a virtual environment**
   ```bash
   uv venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   ```
2. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```
3. **Configure environment variables**
   Create a `.env` file in the project root (alongside `manage.py`) with values appropriate for your local setup. Example configuration:
   ```dotenv
   DJANGO_SECRET_KEY=dev-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_NAME=buzzz
   DATABASE_USER=postgres
   DATABASE_PASSWORD=postgres
   HOST=127.0.0.1
   PORT=5432
   STATIC_URL=/static/
   STATIC_ROOT=staticfiles
   # Optional: provide a GitHub token if needed by integrations
   # GITHUB_TOKEN=your-token
   ```

   Ensure the referenced PostgreSQL database exists before continuing.

4. **Apply database migrations**
   ```bash
   uv run python manage.py migrate
   ```
5. *(Optional)* **Create a superuser** for accessing the Django admin:
   ```bash
   uv run python manage.py createsuperuser
   ```

## Running in the Devcontainer

Simply reopen the repo in the devcontainer. On start, `.devcontainer/post-start.sh` will:
- Create `.env` next to `manage.py` if missing (defaults below).
- Ensure `.venv` exists and install `requirements.txt`.
- Start a Postgres container named `buzzz-db` on port `5432` (if Docker is available).
- Run Django migrations, then start the dev server on `0.0.0.0:8000` (logs: `/tmp/devserver.log`).

Port 8000 is forwarded by `.devcontainer/devcontainer.json`, so you can visit `http://localhost:8000/` on the host right after the container finishes starting.

To adjust automation, edit `.devcontainer/flags.local.env` (values below override defaults):
```
DEVCONTAINER_AUTO_CREATE_ENV=0|1
DEVCONTAINER_AUTO_START_DB=0|1
DEVCONTAINER_DB_CONTAINER_NAME=buzzz-db
DEVCONTAINER_DB_PORT=5432
DEVCONTAINER_AUTO_START_SERVER=0|1
DEVCONTAINER_DJANGO_PORT=8000
```

### Default .env values (created if missing)
```dotenv
DJANGO_SECRET_KEY=dev-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DATABASE_NAME=buzzz
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
HOST=host.docker.internal
PORT=5432
STATIC_URL=/static/
STATIC_ROOT=staticfiles
```

## Running the Development Server (outside the devcontainer)

With the virtual environment active and the database configured, start the Django development server:
```bash
uv run python manage.py runserver
```

Visit http://127.0.0.1:8000/ to view the site. The server reloads automatically when code changes are detected.

## Running Tests

Execute the project's test suite with Django's built-in test runner:
```bash
uv run python manage.py test
```

## Utility Scripts

### Generating Syntax Highlighting CSS

We're using Pygments for syntax highlighting in the application. Regenerate the CSS with the script located at `scripts/generate_pygments_css.py`:
```bash
uv run python scripts/generate_pygments_css.py
```

### Validating Blog Post Tags

Blog post metadata is defined in the YAML front matter at the top of each markdown file in `blog_posts/`. Every post must
declare a `tags` list using the controlled vocabulary `{post, WIP, talk, notes}` (values are case-insensitive). Tags are
rendered on the site and drive automated validation.

Run the validation script to confirm all posts use supported tags:

```bash
uv run python scripts/validate_tags.py
```

You can integrate the check locally by installing the repository's pre-commit hooks:

```bash
uv run pre-commit install
```

The `validate-blog-tags` hook will prevent commits that introduce unsupported tags.
