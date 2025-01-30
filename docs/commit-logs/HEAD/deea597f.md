# Commit Log

---

## Commit Details

- **Commit Hash:**   `deea597f76cf1993f5c1dd9f945b94629cd4b88e`
- **Branch:**        `HEAD`
- **Author:**        GitHub Actions
- **Date:**          2025-01-30 20:13:53 +0100
- **Message:**

  fix(terraform): replace `volumes` with `mounts` for Docker compatibility

- Fixed `docker_container` by using `mounts {}` instead of `volumes` (unsupported).
- Ensured Podman compatibility by toggling `use_podman` for local use.
- Updated `docker_image` to use `build {}` for correctness.
- Validated working setup for both local (Podman) and CI/CD (Docker).

---

## Changed Files:

- `M	main.tf`

---
