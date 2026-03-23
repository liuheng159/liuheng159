---
name: backend-api-baseline
description: Build or extend small Python backend services with a consistent handler-service-model-test workflow. Use when creating CRUD endpoints, adding input validation, scaffolding service modules, standardizing JSON responses, or setting up backend feature structure in a lightweight starter repository.
---

# Backend API Baseline

## Overview

Use this skill to add backend features in a predictable way:

1. Define request and response payloads first.
2. Keep HTTP handlers thin and move business logic into a service module.
3. Add a focused automated test for the service or feature behavior.
4. Update the README or API notes when a new route changes how the app is used.

## Recommended Workflow

### 1. Inspect the current feature shape

Check the existing handler, service, and test layout before adding a new capability. Reuse the current naming and folder structure instead of inventing a parallel pattern.

### 2. Model the contract

Create explicit payload shapes and validation rules. Keep fields narrow and default values obvious.

### 3. Add or update the service layer

Put persistence and domain behavior in a dedicated service module. Favor small methods such as `list_items`, `create_item`, `mark_done`, or `delete_item`.

### 4. Wire the HTTP handler

Serialize service results close to the HTTP boundary and translate domain errors into stable JSON responses.

### 5. Add tests and run checks

At minimum, add one automated check covering the new happy path and one failure path if the feature can fail.

## Resources

### `scripts/bootstrap_backend_feature.py`

Run this script to scaffold a lightweight feature skeleton with model, service, handler, and test files:

```bash
python skills/backend-api-baseline/scripts/bootstrap_backend_feature.py <feature_name>
```

By default it writes into `app/` and `tests/`. Override the roots with `--app-dir` or `--tests-dir` when needed.

### `references/backend-checklist.md`

Read this file when you want a concise checklist for shipping a small API feature consistently.
