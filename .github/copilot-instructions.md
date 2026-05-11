# Repo guidance for AI coding agents

Purpose: concise, actionable notes to help an AI be immediately productive in this Django codebase.

- **Big picture**: This is a Django 6 project named `job_portal` with a single app `jobs`. The project exposes a small REST API using Django REST Framework. Core responsibilities:
  - `job_portal/` — global Django settings and URL routing.
  - `jobs/` — domain models, serializers, DRF views and URL endpoints.
  - API root is included under `/api/` via `job_portal/urls.py` -> `jobs/urls.py`.

- **Key files (examples to inspect/modify)**
  - `job_portal/settings.py` — DB config, `INSTALLED_APPS`, `AUTH_USER_MODEL`.
  - `job_portal/urls.py` — mounts `jobs.urls` at `/api/`.
  - `jobs/models.py` — `User` (custom user) and `Job` model definitions.
  - `jobs/serializers.py` — `RegisterSerializer` (uses `create_user`).
  - `jobs/views.py` — `register` view (POST endpoint).
  - `jobs/urls.py` — endpoint routes (e.g. `register/`).
  - `jobs/migrations/0001_initial.py` — canonical schema generated for this app.

- **Architecture & important decisions**
  - The project uses a custom user model: `AUTH_USER_MODEL = 'jobs.User'`. Always reference the user model via `settings.AUTH_USER_MODEL` or `get_user_model()` when creating foreign keys or serializers.
  - DRF is used for API endpoints; views are simple function-based `@api_view` handlers (see `register`).
  - `jobs.Job.posted_by` is a FK to the custom user model — maintain referential integrity when creating jobs.

- **Developer workflows & commands**
  - Activate the included virtualenv: `source env/bin/activate` (macOS).
  - Typical Django commands from repo root:
    - `python manage.py makemigrations jobs`
    - `python manage.py migrate`
    - `python manage.py createsuperuser`
    - `python manage.py runserver`
  - Note: `job_portal/settings.py` is configured for PostgreSQL (DATABASES['default'] uses `django.db.backends.postgresql`, NAME=`jobportal_db`, USER=`navadeep`). There is also a `db.sqlite3` file present in the workspace — this indicates a local sqlite DB exists but settings point to Postgres. For quick local testing either:
    - run a local Postgres and create a DB/user matching settings, or
    - temporarily switch `DATABASES` in `job_portal/settings.py` to sqlite (ENGINE=`django.db.backends.sqlite3`, NAME=BASE_DIR / 'db.sqlite3').

- **Code patterns & project-specific conventions**
  - Password handling: `RegisterSerializer` marks `password` as `write_only` and calls `User.objects.create_user(**validated_data)` in `create()` — do not assign `password` directly; always use `create_user()` or `set_password()`.
  - Routes: API endpoints are mounted under `/api/` (see `job_portal/urls.py`); `jobs/urls.py` contains per-app paths.
  - Keep changes small and explicit: models are simple and migrations are present (`jobs/migrations/0001_initial.py`). Update serializers/views when changing model fields and add migrations.

- **Integration points & dependencies**
  - External requirement: Django 6 and Django REST Framework (`rest_framework` in `INSTALLED_APPS`). The repo includes a `env/` virtualenv with these packages installed.
  - Database: PostgreSQL intended by settings; confirm running DB during integration tests or CI.

- **Examples**
  - Register user (JSON POST to `/api/register/`):

    {
      "username": "alice",
      "password": "s3cret",
      "phone": "1234567890"
    }

  - Minimal curl example:

    curl -X POST http://127.0.0.1:8000/api/register/ -H 'Content-Type: application/json' -d '{"username":"alice","password":"s3cret","phone":"123"}'

- **Tests & CI**
  - No app tests or CI configuration discovered (`jobs/tests.py` is empty). If adding tests, follow Django's TestCase conventions and prefer API-level tests using DRF's `APIClient`.

- **What to watch for when editing**
  - Changing `User` model after initial migrations requires care — follow Django's guidance for altering custom user models.
  - Because `AUTH_USER_MODEL` is custom, always use `settings.AUTH_USER_MODEL` for FK references in new models or migrations.
  - Keep `rest_framework` usage consistent (function-based views are used here; prefer keeping the style unless migrating to class-based views with a clear plan).

If anything here is unclear or you want the file to include examples for other workflows (e.g., running with Postgres locally or adding CI config), tell me which part to expand and I'll iterate.
