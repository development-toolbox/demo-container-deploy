#!/bin/bash

#set -e  # Exit immediately on non-zero commands, except where handled

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

# **Always write the report, even if TFLint fails**
echo "$TFLINT_OUTPUT" >> "$REPORT_FILE"

# If no output was generated, add a placeholder message
if [[ -z "$TFLINT_OUTPUT" ]]; then
    echo "No issues found." >> "$REPORT_FILE"
fi

# Show report contents
echo "✅ TFLint Report:"
cat "$REPORT_FILE"

# Ensure Git detects file changes
git add "$REPORT_FILE"

if git diff --staged --exit-code -- "$REPORT_FILE"; then
    echo "✅ No changes in TFLint report. Skipping commit."
else
    # Configure Git and **amend the original commit**
    git config --global user.name "GitHub Actions"
    git config --global user.email "github-actions@github.com"

    echo "📌 Amending original commit with updated TFLint report..."
    git commit --amend --no-edit
    git push --force
fi


# **Fail the job if TFLint found issues**
if [[ "$TFLINT_EXIT_CODE" -ne 0 ]]; then
    echo "❌ TFLint found issues. Failing the job."
    exit 1
fi
