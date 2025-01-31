# Commit Log for Branch: `main`

This file provides a summary of all commits in the branch `main`.
Each commit links to its detailed log.

### 📈 [View Full Git Timeline](./git_timeline_report.md)

| Commit Hash | Date & Time       | Author       | Message           |
|-------------|------------------|--------------|-------------------|
| [a6b18588](./a6b18588.md) | 2025-01-31 13:10 | GitHub Actions | chore(demo): adding failing main.tf |
| [060e1d74](./060e1d74.md) | 2025-01-30 20:13 | GitHub Actions | fix(terraform): replace `volumes` with `mounts` for Docker compatibility |
| [d1ac9f97](./d1ac9f97.md) | 2025-01-30 19:59 | GitHub Actions | fix(terraform): correct provider argument for Docker compatibility |
| [610e2c4e](./610e2c4e.md) | 2025-01-30 19:48 | GitHub Actions | fix(terraform): forgot to change podman to docker in every linegit add main.tf |
| [0dd9bb65](./0dd9bb65.md) | 2025-01-30 19:42 | GitHub Actions | fix(terraform): replace Podman provider with Docker for compatibility |
| [a13db8a0](./a13db8a0.md) | 2025-01-30 19:32 | GitHub Actions | fix(terraform): add required_version and define variable type |
| [ed2a93b6](./ed2a93b6.md) | 2025-01-30 19:27 | GitHub Actions | fix(docs): added missing docs |
| [291d3adc](./291d3adc.md) | 2025-01-30 19:25 | GitHub Actions | fix(terraform): heeh changed the wrong main last time :-D now the broken is in the Example folder |
| [25e57545](./25e57545.md) | 2025-01-30 19:16 | GitHub Actions | fix(terraform): add required provider block and correct podman resource definitions |
| [c5f8a100](./c5f8a100.md) | 2025-01-30 19:06 | GitHub Actions | fix(script): Updated executable bit |
| [416d0688](./416d0688.md) | 2025-01-30 19:05 | GitHub Actions | chore(ci): update Trivy report with latest scan results |
| [442bad96](./442bad96.md) | 2025-01-30 18:59 | GitHub Actions | fix(ci): corrected upload_report call to handle multiple scan types |
| [9d719f6a](./9d719f6a.md) | 2025-01-30 18:27 | GitHub Actions | chore(ci): ensure Trivy report always uploads before failing workflow |
| [ef972b4c](./ef972b4c.md) | 2025-01-30 18:08 | GitHub Actions | chore(ci): update TFLint report with latest scan results |
| [b066dffa](./b066dffa.md) | 2025-01-30 17:45 | GitHub Actions | chore(gitignore): fix so gitignore do not ignore my docs/commit-logs |
| [5b48800f](./5b48800f.md) | 2025-01-30 17:40 | GitHub Actions | refactor(ci): unify report upload logic for TFLint & Trivy scans |
| [9a3fdba1](./9a3fdba1.md) | 2025-01-30 16:47 | GitHub Actions | fix(security-scan): created a script to do the securityscan and create a md file v1 |
| [ddac656c](./ddac656c.md) | 2025-01-29 21:01 | GitHub Actions | fix(ci): ensure TFLint report is uploaded before failing the job |
| [3831d222](./3831d222.md) | 2025-01-29 20:50 | GitHub Actions | fix(ci): removed terraform init because that should not be there! |
| [7ba1bc3a](./7ba1bc3a.md) | 2025-01-29 20:43 | GitHub Actions | chore(ci): added executable to the file .. |
| [24f5fab3](./24f5fab3.md) | 2025-01-29 20:40 | GitHub Actions | chore(ci): update TFLint report with latest scan results |
| [45b8e25a](./45b8e25a.md) | 2025-01-29 20:35 | GitHub Actions | feat(ci): Updated Terraform CI workflow to run the python scripts instead |
| [b3f842b6](./b3f842b6.md) | 2025-01-29 20:30 | GitHub Actions | feat(ci): add Git function to upload TFLint report |
| [04a17632](./04a17632.md) | 2025-01-29 20:19 | GitHub Actions | feat(ci): add TFLint issue fetcher and improved TFLint report generator |
| [d554cbad](./d554cbad.md) | 2025-01-29 19:44 | GitHub Actions | fix(ci): avoid commit conflicts by using separate TFLint report commit |
| [efc1ef4a](./efc1ef4a.md) | 2025-01-29 19:23 | GitHub Actions | fix(ci): ensure TFLint report changes trigger commit correctly |
| [186218bc](./186218bc.md) | 2025-01-29 19:02 | Johan Sörell | chore(ci): add run_tflint_check.sh for consistent TFLint execution |
| [5cfe261f](./5cfe261f.md) | 2025-01-29 17:26 | Johan Sörell | fix(ci): ensure TFLint report is always created and committed |
| [26aa0ff3](./26aa0ff3.md) | 2025-01-29 15:32 | Johan Sörell | fix(ci): ensure TFLint report is always created and committed |
| [437413e3](./437413e3.md) | 2025-01-29 15:21 | Johan Sörell | fix(ci): restrict GitHub Actions to commit only reports |
| [2b85018d](./2b85018d.md) | 2025-01-29 14:45 | Johan Sörell | fix(ci): ensure TFLint and Trivy jobs fail on errors, append reports to original commit |
| [560723eb](./560723eb.md) | 2025-01-29 14:14 | Johan Sörell | fix(tflint): update config to match latest TFLint version |
| [5b306a24](./5b306a24.md) | 2025-01-29 14:06 | Johan Sörell | fix(ci): resolve TFLint installation issue in Terraform workflow |
| [f5f3ddcd](./f5f3ddcd.md) | 2025-01-29 14:00 | Johan Sörell | fix(docs): update GitHub Actions badge URLs |
| [577e6f54](./577e6f54.md) | 2025-01-29 12:49 | Johan Sörell | refactor(ci): move Trivy installation to standalone script |
| [c6dd791b](./c6dd791b.md) | 2025-01-29 12:38 | Johan Sörell | fix(security): improve Trivy report formatting and retain VEX notice |
| [2041d290](./2041d290.md) | 2025-01-29 12:26 | Johan Sörell | feat(security): automate Trivy vulnerability reporting in CI/CD |
| [f4d400a8](./f4d400a8.md) | 2025-01-29 11:36 | Johan Sörell | fix(trivy): correct deb package architecture mapping to 64bit |
| [81939a74](./81939a74.md) | 2025-01-29 11:30 | Johan Sörell | fix(workflow): bugfix installation of trivy using Ubuntu .deb package instead |
| [88aca7e0](./88aca7e0.md) | 2025-01-29 09:39 | Johan Sörell | feat(init): initial commit with Terraform, container deployment, and CI/CD |
