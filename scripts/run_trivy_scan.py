#!/usr/bin/env python3
import subprocess
import json
import os
import sys
from datetime import datetime

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORT_FILE = os.path.join(PROJECT_ROOT, "trivy_report.md")
JSON_REPORT_FILE = os.path.join(PROJECT_ROOT, "trivy_report.json")
UPLOAD_SCRIPT = os.path.join(PROJECT_ROOT, "scripts/ci_helpers/upload_report.py")

# Upload the report before failing
def upload_report():
    if os.path.exists(UPLOAD_SCRIPT):
        print("📤 Uploading Trivy Report...")
        subprocess.run(["python3", UPLOAD_SCRIPT, "Trivy"], check=False)
    else:
        print(f"❌ Error: Upload script not found: {UPLOAD_SCRIPT}")

# Detect if using Podman or Docker
USE_PODMAN = os.path.exists(f"/run/user/{os.getuid()}/podman/podman.sock")
if USE_PODMAN:
    os.environ["DOCKER_HOST"] = f"unix:///run/user/{os.getuid()}/podman/podman.sock"
    CONTAINER_RUNTIME = "podman"
else:
    CONTAINER_RUNTIME = "docker"

# Run Trivy and capture output
def run_trivy_scan():
    """Runs Trivy with correct runtime and generates a JSON report."""
    print(f"🚀 Running Trivy Image Scan using {CONTAINER_RUNTIME}...")

    # Ensure the image exists
    check_image_command = [CONTAINER_RUNTIME, "images", "-q", "revealjs:latest"]
    result = subprocess.run(check_image_command, capture_output=True, text=True)

    if not result.stdout.strip():
        print(f"❌ Error: Image 'revealjs:latest' not found in {CONTAINER_RUNTIME}.")
        print("💡 Build the image first: `podman build -t revealjs:latest .` (or `docker build ...`)")
        sys.exit(1)

    command = ["trivy", "image", "--format", "json", "--severity", "HIGH", "revealjs:latest"]

    with open(JSON_REPORT_FILE, "w") as json_file:
        try:
            subprocess.run(command, stdout=json_file, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Trivy scan failed: {e}")
            sys.exit(1)

# Generate Markdown Report
def generate_report():
    """Parses the JSON report and generates a Markdown report."""
    with open(JSON_REPORT_FILE, "r") as f:
        data = json.load(f)

    report_lines = [
        "# Trivy Security Report",
        f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]

    high_vulns = 0
    report_lines.append("| Package | CVE | Severity | Installed | Fixed | Description |")
    report_lines.append("|---------|-----|----------|-----------|-------|-------------|")

    for result in data.get("Results", []):
        for vuln in result.get("Vulnerabilities", []):
            if vuln.get("Severity") == "HIGH":
                high_vulns += 1

                # **Fix CVE Link** (Use NVD database instead of `aquasec`)
                cve_id = vuln.get("VulnerabilityID")
                cve_link = f"https://nvd.nist.gov/vuln/detail/{cve_id}"  # ✅ Correct link

                pkg_name = vuln.get("PkgName", "N/A")
                installed_version = vuln.get("InstalledVersion", "N/A")
                fixed_version = vuln.get("FixedVersion", "N/A") if vuln.get("FixedVersion") else "N/A"
                description = vuln.get("Title", "No description available.")

                report_lines.append(
                    f"| {pkg_name} | [{cve_id}]({cve_link}) | HIGH | {installed_version} | {fixed_version} | {description} |"
                )

    report_lines.append("")
    report_lines.append(f"**Total HIGH vulnerabilities: {high_vulns}**")

    # Add **VEX notice** at the bottom of the report
    report_lines.append("\n---\n")
    report_lines.append("## For OSS Maintainers: VEX Notice")
    report_lines.append(
        "If you're an OSS maintainer and Trivy has detected vulnerabilities in your project that you believe "
        "are not actually exploitable, consider issuing a VEX (Vulnerability Exploitability eXchange) statement."
    )
    report_lines.append(
        "VEX allows you to communicate the actual status of vulnerabilities in your project, improving security transparency "
        "and reducing false positives for your users."
    )
    report_lines.append(
        "Learn more and start using VEX: [Trivy VEX Docs](https://aquasecurity.github.io/trivy/v0.58/docs/supply-chain/vex/repo#publishing-vex-documents)"
    )
    report_lines.append("")
    report_lines.append("To disable this notice, set the `TRIVY_DISABLE_VEX_NOTICE` environment variable.")

    # Write report
    with open(REPORT_FILE, "w") as f:
        f.write("\n".join(report_lines))

    print(f"📄 Trivy security report saved: {REPORT_FILE}")

    return high_vulns  # ✅ Return vulnerability count to `main()`

# Main function
def main():
    run_trivy_scan()
    high_vulns = generate_report()

    # ✅ Upload report **before** failing
    upload_report()

    if high_vulns > 0:
        print(f"❌ Trivy detected {high_vulns} HIGH vulnerabilities. Failing workflow.")
        sys.exit(1)  # 🚨 Exit with failure AFTER uploading
    else:
        print("✅ No HIGH vulnerabilities found. Exiting cleanly.")
        sys.exit(0)


if __name__ == "__main__":
    main()
