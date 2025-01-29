#!/usr/bin/env python3
import subprocess
import os
import sys

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPORT_FILE = os.path.join(PROJECT_ROOT, "tflint_report.md")

def run_git_command(command):
    """Run a git command and return output."""
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def commit_tflint_report():
    """Commit and push TFLint report only if changes exist."""
    if not os.path.exists(REPORT_FILE):
        print(f"❌ Error: Report file not found: {REPORT_FILE}")
        sys.exit(1)

    # Check if there are any changes
    subprocess.run(["git", "add", REPORT_FILE], check=True)
    diff_check = subprocess.run(["git", "diff", "--staged", "--exit-code"], capture_output=True)

    if diff_check.returncode == 0:
        print("✅ No changes detected in TFLint report. Skipping commit.")
        sys.exit(0)

    # Configure Git for CI/CD
    subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "github-actions@github.com"], check=True)

    # Commit and push
    commit_message = "chore(ci): update TFLint report with latest scan results"
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "push"], check=True)

    print("🚀 TFLint report successfully committed and pushed!")

if __name__ == "__main__":
    commit_tflint_report()
