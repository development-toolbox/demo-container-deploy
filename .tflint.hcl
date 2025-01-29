# Globala settings for TFLint
config {
  ignore_module = { all = false }  # Fixed type (was a boolean, now a map)
}

# Enable rules to validate Terraform standards
rule "terraform_required_providers" {
  enabled = true
}

rule "terraform_deprecated_interpolation" {
  enabled = true
}
