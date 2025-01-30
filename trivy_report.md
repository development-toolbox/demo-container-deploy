# Trivy Security Report
Generated on 2025-01-30 19:05:31

| Package | CVE | Severity | Installed | Fixed | Description |
|---------|-----|----------|-----------|-------|-------------|
| libcrypto3 | [CVE-2023-5363](https://nvd.nist.gov/vuln/detail/CVE-2023-5363) | HIGH | 3.1.2-r0 | 3.1.4-r0 | openssl: Incorrect cipher key and IV length processing |
| libssl3 | [CVE-2023-5363](https://nvd.nist.gov/vuln/detail/CVE-2023-5363) | HIGH | 3.1.2-r0 | 3.1.4-r0 | openssl: Incorrect cipher key and IV length processing |
| cross-spawn | [CVE-2024-21538](https://nvd.nist.gov/vuln/detail/CVE-2024-21538) | HIGH | 6.0.5 | 7.0.5, 6.0.6 | cross-spawn: regular expression denial of service |
| cross-spawn | [CVE-2024-21538](https://nvd.nist.gov/vuln/detail/CVE-2024-21538) | HIGH | 7.0.3 | 7.0.5, 6.0.6 | cross-spawn: regular expression denial of service |
| ip | [CVE-2024-29415](https://nvd.nist.gov/vuln/detail/CVE-2024-29415) | HIGH | 2.0.0 | N/A | node-ip: Incomplete fix for CVE-2023-42282 |
| semver | [CVE-2022-25883](https://nvd.nist.gov/vuln/detail/CVE-2022-25883) | HIGH | 7.3.7 | 7.5.2, 6.3.1, 5.7.2 | nodejs-semver: Regular expression denial of service |

**Total HIGH vulnerabilities: 6**

---

## For OSS Maintainers: VEX Notice
If you're an OSS maintainer and Trivy has detected vulnerabilities in your project that you believe are not actually exploitable, consider issuing a VEX (Vulnerability Exploitability eXchange) statement.
VEX allows you to communicate the actual status of vulnerabilities in your project, improving security transparency and reducing false positives for your users.
Learn more and start using VEX: [Trivy VEX Docs](https://aquasecurity.github.io/trivy/v0.58/docs/supply-chain/vex/repo#publishing-vex-documents)

To disable this notice, set the `TRIVY_DISABLE_VEX_NOTICE` environment variable.