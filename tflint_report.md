# TFLint Report
Generated on Wed Jan 29 19:19:46 UTC 2025

2 issue(s) found:

main.tf:10:1: Warning - Missing version constraint for provider "podman" in `required_providers` (terraform_required_providers)
main.tf:1:1: Warning - terraform "required_version" attribute is required (terraform_required_version)

❌ Warning: Missing 'required_version' in main.tf
ℹ️  Fix: Add this block to your main.tf:
```hcl
terraform {
  required_version = ">= 1.3.0"
}
```
📌 More info: [Terraform Docs](https://developer.hashicorp.com/terraform/language/settings#specifying-a-required-terraform-version)

❌ Warning: Missing provider version for 'podman'
ℹ️  Fix: Add this block to your main.tf:
```hcl
terraform {
  required_providers {
    podman = {
      source  = "containers/podman"
      version = ">= 1.0.0"
    }
  }
}
```
📌 More info: [Terraform Docs](https://developer.hashicorp.com/terraform/language/providers/requirements)
