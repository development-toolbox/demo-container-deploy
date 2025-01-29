#!/usr/bin/env bash
set -e

# Fetch the latest version with retries
for i in {1..3}; do
  TRIVY_LATEST=$(curl -s https://api.github.com/repos/aquasecurity/trivy/releases/latest | jq -r '.tag_name')
  if [[ -n "$TRIVY_LATEST" && "$TRIVY_LATEST" != "null" ]]; then
    break
  fi
  echo "Warning: Failed to fetch Trivy version. Retrying ($i/3)..."
  sleep 2
done

# Fallback version if API fails
if [[ -z "$TRIVY_LATEST" || "$TRIVY_LATEST" == "null" ]]; then
  echo "Error: Could not fetch Trivy latest version from GitHub. Using fallback version 0.58.2."
  TRIVY_LATEST="v0.58.2"
fi

# Remove 'v' from the version number
TRIVY_VERSION=${TRIVY_LATEST#v}

# Detect architecture
ARCH="64bit"  # GitHub Actions runs on x86_64

# Construct the correct URL
TRIVY_URL="https://github.com/aquasecurity/trivy/releases/download/v${TRIVY_VERSION}/trivy_${TRIVY_VERSION}_Linux-${ARCH}.deb"

echo "Downloading Trivy from: $TRIVY_URL"

# Download and install
wget "$TRIVY_URL"
sudo dpkg -i "trivy_${TRIVY_VERSION}_Linux-${ARCH}.deb"

# Verify installation
trivy --version
