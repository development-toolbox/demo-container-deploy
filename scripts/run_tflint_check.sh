#!/bin/bash

# Remove `set -e` since it causes issues
cd "$(dirname "$0")/.."  # Move to project root

REPORT_FILE="tflint_report.md"

echo "🚀 Running TFLint Check..."
echo "📂 Current directory: $(pwd)"

# Ensure Terraform is initialized
if [[ ! -d ".terraform" ]]; then
    echo "🔧 Initializing Terraform..."
    terraform init -input=false
fi

# Ensure TFLint is installed
if ! command -v tflint &> /dev/null; then
    echo "TFLint is not installed. Installing now..."
    curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash
fi

# Start the report
echo "# TFLint Report" > "$REPORT_FILE"
echo "Generated on $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Run TFLint **without stopping the script**
TFLINT_OUTPUT=$(tflint --format compact 2>&1 || true)
TFLINT_EXIT_CODE=$?

# Append output to report
echo "$TFLINT_OUTPUT" >> "$REPORT_FILE"

# If no output was generated, add a placeholder message
if [[ -z "$TFLINT_OUTPUT" ]]; then
    echo "No issues found." >> "$REPORT_FILE"
fi

# **Check for specific warnings and provide guidance**
if echo "$TFLINT_OUTPUT" | grep -q "terraform_required_version"; then
    echo "" >> "$REPORT_FILE"
    echo "❌ Warning: Missing 'required_version' in main.tf" >> "$REPORT_FILE"
    echo "ℹ️  Fix: Add this block to your main.tf:" >> "$REPORT_FILE"
    echo '```hcl' >> "$REPORT_FILE"
    echo 'terraform {' >> "$REPORT_FILE"
    echo '  required_version = ">= 1.3.0"' >> "$REPORT_FILE"
    echo '}' >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
    echo "📌 More info: [Terraform Docs](https://developer.hashicorp.com/terraform/language/settings#specifying-a-required-terraform-version)" >> "$REPORT_FILE"
fi

if echo "$TFLINT_OUTPUT" | grep -q "terraform_required_providers"; then
    echo "" >> "$REPORT_FILE"
    echo "❌ Warning: Missing provider version for 'podman'" >> "$REPORT_FILE"
    echo "ℹ️  Fix: Add this block to your main.tf:" >> "$REPORT_FILE"
    echo '```hcl' >> "$REPORT_FILE"
    echo 'terraform {' >> "$REPORT_FILE"
    echo '  required_providers {' >> "$REPORT_FILE"
    echo '    podman = {' >> "$REPORT_FILE"
    echo '      source  = "containers/podman"' >> "$REPORT_FILE"
    echo '      version = ">= 1.0.0"' >> "$REPORT_FILE"
    echo '    }' >> "$REPORT_FILE"
    echo '  }' >> "$REPORT_FILE"
    echo '}' >> "$REPORT_FILE"
    echo '```' >> "$REPORT_FILE"
    echo "📌 More info: [Terraform Docs](https://developer.hashicorp.com/terraform/language/providers/requirements)" >> "$REPORT_FILE"
fi

# Show report contents
echo "✅ TFLint Report:"
cat "$REPORT_FILE"

# **Commit Only If There Are Changes**
git add "$REPORT_FILE"

if git diff --staged --exit-code -- "$REPORT_FILE"; then
    echo "✅ No changes in TFLint report. Skipping commit."
else
    # Configure Git (NO AMEND)
    git config --global user.name "GitHub Actions"
    git config --global user.email "github-actions@github.com"

    echo "📌 Creating a separate commit for the TFLint report..."
    git commit -m "chore(ci): update TFLint report"
    git push
fi

# **Fail the job if TFLint found issues**
if [[ "$TFLINT_EXIT_CODE" -ne 0 ]]; then
    echo "❌ TFLint found issues. Failing the job."
    exit 1
fi
