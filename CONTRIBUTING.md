# Contributing Guidelines

## Repo Structure

- Please keep ETL, batch, streaming, ML, and infra scripts modular.
- Add comments and docstrings explaining logic.
- Use PRs and issues for all changes or suggestions.


## Local Test & Lint

- Run `flake8 .` for Python.
- Run unit tests in `tests/` before PR.

## Issue Templates

- Use issue templates for bug, feature request, infra, documentation.

## CI/CD

- All PRs are tested automatically (lint, tests, terraform plan).