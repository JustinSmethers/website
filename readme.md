# Buzzz Website

Documentation for developing the Buzzz Django application.

## Prerequisites

- Python 3.11 or newer
- PostgreSQL running locally (or accessible remotely)
- `pip` for installing Python packages

## Initial Setup

1. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   ```
2. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
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
   python manage.py migrate
   ```
5. *(Optional)* **Create a superuser** for accessing the Django admin:
   ```bash
   python manage.py createsuperuser
   ```

## Running the Development Server

With the virtual environment active and the database configured, start the Django development server:
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to view the site. The server reloads automatically when code changes are detected.

## Running Tests

Execute the project's test suite with Django's built-in test runner:
```bash
python manage.py test
```

## Utility Scripts

### Generating Syntax Highlighting CSS

We're using Pygments for syntax highlighting in the application. Regenerate the CSS with the script located at `scripts/generate_pygments_css.py`:
```bash
python scripts/generate_pygments_css.py
```
