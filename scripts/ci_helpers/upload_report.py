#!/usr/bin/env python3
import subprocess
import sys
import os

# Ensure a report type is provided
if len(sys.argv) < 2:
    print("❌ Error: No report type specified. Usage: python upload_report.py <REPORT_TYPE>")
    sys.exit(1)

REPORT_TYPE = sys.argv[1].lower()  # e.g., "tflint" or "trivy"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPORT_FILE = os.path.join(PROJECT_ROOT, f"{REPORT_TYPE}_report.md")

def commit_report():
    """Commit and push the report for the specified type."""
    if not os.path.exists(REPORT_FILE):
        print(f"❌ Error: Report file not found: {REPORT_FILE}")
        sys.exit(1)

    # Configure Git for CI/CD
    subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "github-actions@github.com"], check=True)

    # Always add the report file
    subprocess.run(["git", "add", REPORT_FILE], check=True)

    # Force commit even if there are no changes
    commit_message = f"chore(ci): update {REPORT_TYPE.capitalize()} report with latest scan results"
    subprocess.run(["git", "commit", "-m", commit_message, "--allow-empty"], check=True)
    subprocess.run(["git", "push"], check=True)

    print(f"🚀 {REPORT_TYPE.capitalize()} report successfully committed and pushed!")

if __name__ == "__main__":
    commit_report()
