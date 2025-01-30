#!/usr/bin/env python3
import subprocess
import os
import sys

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPORTS = {
    "TFLint": os.path.join(PROJECT_ROOT, "tflint_report.md"),
    "Trivy": os.path.join(PROJECT_ROOT, "trivy_report.md"),
}

def run_git_command(command):
    """Run a git command and return output."""
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def commit_report():
    """Commit and push report only if changes exist."""
    selected_report = None
    report_type = None

    # Find the first existing report
    for key, report_path in REPORTS.items():
        if os.path.exists(report_path):
            selected_report = report_path
            report_type = key
            break

    if not selected_report:
        print("❌ Error: No report file found. Skipping commit.")
        sys.exit(1)

    print(f"📄 Found report: {selected_report} ({report_type})")

    # Check if there are any changes
    subprocess.run(["git", "add", selected_report], check=True)
    diff_check = subprocess.run(["git", "diff", "--staged", "--exit-code"], capture_output=True)

    if diff_check.returncode == 0:
        print(f"✅ No changes detected in {report_type} report. Skipping commit.")
        sys.exit(0)

    # Configure Git for CI/CD
    subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "github-actions@github.com"], check=True)

    # Commit and push
    commit_message = f"chore(ci): update {report_type} report with latest scan results"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push"], check=True)

    print(f"🚀 {report_type} report successfully committed and pushed!")

if __name__ == "__main__":
    commit_report()
