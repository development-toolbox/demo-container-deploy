#!/usr/bin/env python3
import requests
import json
import os

# GitHub API URL for TFLint rule documentation
TFLINT_RULES_URL = "https://api.github.com/repos/terraform-linters/tflint-ruleset-terraform/contents/docs/rules"

# Output file
DB_FILE = "scripts/tflint_issue_fetcher/tflint_issues.json"

def fetch_tflint_issues():
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(TFLINT_RULES_URL, headers=headers)

    if response.status_code != 200:
        print(f"❌ Error fetching data: {response.status_code}")
        return []

    return response.json()

def extract_rule_data(rules):
    issue_database = {}

    for rule in rules:
        rule_name = rule["name"].replace(".md", "")
        rule_url = rule["html_url"]

        issue_database[rule_name] = {
            "url": rule_url,
            "description": f"More details: [Terraform Linter Docs]({rule_url})"
        }

    return issue_database

def save_database(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ TFLint issues saved to {DB_FILE}")

if __name__ == "__main__":
    print("🔍 Fetching TFLint issues...")
    rules = fetch_tflint_issues()
    
    if rules:
        database = extract_rule_data(rules)
        save_database(database)
    else:
        print("❌ No rules fetched.")
