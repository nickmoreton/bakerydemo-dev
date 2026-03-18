# Repository Guidelines

## Project Structure & Module Organization

`bakerydemo/` contains the Django project and app modules: `base/`, `blog/`, `breads/`, `locations/`, `people/`, `recipes/`, and `search/`. Shared templates live in `bakerydemo/templates/`, static assets in `bakerydemo/static/`, and demo fixtures in `bakerydemo/base/fixtures/bakerydemo.json`. Settings are split under `bakerydemo/settings/` with `test.py` for CI and `local.py` for untracked local overrides. Tests currently live alongside apps, for example `bakerydemo/base/tests/`.

## Build, Test, and Development Commands

Create a local environment with `python -m venv .venv`, activate it, then run `pip install -r requirements/development.txt` and `npm ci`. Start the app with `./manage.py migrate`, `./manage.py load_initial_data`, and `./manage.py runserver`. Use `make lint` to run the full lint suite, `make format` to apply autofixes, and `./manage.py test` to run Django tests with `bakerydemo.settings.test` as used in CI. For container-based work, `docker compose up --build -d` bootstraps the local stack.

## Coding Style & Naming Conventions

Use spaces for indentation: 4 spaces for Python, HTML, Markdown, and 2 spaces for JS, JSON, YAML, and CSS, per `.editorconfig`. Python formatting and import ordering are enforced by `ruff` with a target of Python 3.12 and an 88-character line length; HTML is formatted with `djhtml`, templates are parsed by `curlylint`, and frontend files are checked with `eslint`, `stylelint`, and `prettier`. Follow Django naming patterns such as `test_*.py` for tests, lowercase module names, and descriptive Wagtail app labels.

## Testing Guidelines

Write tests under the relevant app’s `tests/` package and name functions or methods with a `test_` prefix. Run `./manage.py check`, `./manage.py makemigrations --check --noinput`, and `./manage.py test` before opening a PR; those are the same server-side checks enforced by GitHub Actions. Add focused regression coverage for model, page, template, and admin changes.

## Commit & Pull Request Guidelines

Recent history favors short, imperative commit subjects such as `Add required_on_save=True...` or scoped prefixes like `fix:` and `deploy:`; issue references in parentheses are common, for example `(#647)`. Pull requests should summarize the change, link the related issue, include screenshots for visible UI/content changes, and disclose any AI assistance plus how you verified the result, as required by `CONTRIBUTING.md`.

## Configuration & Content Notes

Copy `.env.example` to `.env` and `bakerydemo/settings/local.py.example` to `bakerydemo/settings/local.py` for local overrides. Do not commit secrets or generated image renditions in `media/images`; if fixture content changes, regenerate `bakerydemo/base/fixtures/bakerydemo.json` and format it with Prettier.
