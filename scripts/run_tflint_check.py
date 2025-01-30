#!/usr/bin/env python3
import subprocess
import json
import os
from datetime import datetime

# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORT_FILE = os.path.join(PROJECT_ROOT, "tflint_report.md")
DB_FILE = os.path.join(PROJECT_ROOT, "scripts/tflint_issue_fetcher/tflint_issues.json")
UPLOAD_SCRIPT = os.path.join(PROJECT_ROOT, "scripts/ci_helpers/upload_report.py")


# Ensure TFLint is installed
def install_tflint():
    try:
        subprocess.run(["tflint", "--version"], check=True, stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        print("🚀 Installing TFLint...")
        subprocess.run(
            "curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash",
            shell=True,
            check=True,
        )

# Run TFLint and capture output
def run_tflint():
    try:
        result = subprocess.run(["tflint", "--format", "compact"], text=True, capture_output=True, check=False)
        return result.stdout, result.returncode
    except FileNotFoundError:
        print("❌ Error: TFLint not found. Run `install_tflint()` first.")
        return "", 1

# Load TFLint issue database
def load_issue_database():
    if not os.path.exists(DB_FILE):
        print(f"❌ Database not found: {DB_FILE}")
        return {}

    with open(DB_FILE, "r") as f:
        return json.load(f)

# Match TFLint output against known issues
def analyze_tflint_output(tflint_output, issue_db):
    report_lines = ["# TFLint Report", f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ""]

    issues_found = False
    for line in tflint_output.split("\n"):
        if "terraform_" in line:
            # Extract rule name and full message
            rule_name = line.split()[-1].strip("()")
            fix_info = issue_db.get(rule_name.lower(), {}).get("description", "No additional information available.")
            original_message = line.strip()

            issues_found = True

            report_lines.append(f"❌ Issue detected: **{rule_name}**")
            report_lines.append(f"📝 **Original Message:** `{original_message}`")
            report_lines.append(f"ℹ️ More details: {fix_info}")
            report_lines.append("")

    if not issues_found:
        report_lines.append("✅ No issues found.")

    return "\n".join(report_lines), issues_found

# Save the report
def save_report(report_text):
    with open(REPORT_FILE, "w") as f:
        f.write(report_text)
    print(f"📄 TFLint report saved: {REPORT_FILE}")

# Upload the report before failing
def upload_report():
    if os.path.exists(UPLOAD_SCRIPT):
        print("📤 Uploading TFLint Report...")
        subprocess.run(["python3", UPLOAD_SCRIPT], check=False)
    else:
        print(f"❌ Error: Upload script not found: {UPLOAD_SCRIPT}")

# Main function
def main():
    install_tflint()
    
    tflint_output, exit_code = run_tflint()
    issue_db = load_issue_database()
    
    report_text, issues_found = analyze_tflint_output(tflint_output, issue_db)
    save_report(report_text)
    
    # **Upload report before failing the job**
    upload_report()

    # **Exit with TFLint's status code to fail CI/CD if needed**
    if issues_found:
        print("❌ TFLint found issues. Allowing report upload before failing.")
        exit(1) # 🚨 Exit with failure AFTER uploading
    else:
        print("✅ No critical issues found. Exiting cleanly.")
        exit(0)

if __name__ == "__main__":
    main()
