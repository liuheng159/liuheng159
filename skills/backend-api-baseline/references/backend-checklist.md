# Backend Feature Checklist

Use this checklist before finishing a backend feature:

1. Confirm the route name, HTTP method, and response shape are consistent.
2. Validate inbound fields with clear limits or defaults.
3. Keep business logic out of the HTTP handler.
4. Add or update a service-level automated test.
5. Update any developer-facing documentation if the route is user-visible.
6. Prefer deterministic in-memory or fixture-backed tests for starter projects.
