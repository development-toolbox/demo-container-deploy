terraform {
  required_providers {
    podman = {
      source  = "hashicorp/podman"
      version = "~> 1.0"
    }
  }
}

provider "podman" {
  uri = "unix:///run/user/${var.user_id}/podman/podman.sock"
}

variable "user_id" {
  default = "1000"  # Change this based on your user ID dynamically
}

resource "podman_image" "revealjs" {
  name       = "revealjs"
  dockerfile = "${path.module}/Dockerfile"
  context    = path.module
}

resource "podman_container" "revealjs_presentation" {
  image = podman_image.revealjs.id
  name  = "revealjs-container"

  ports = {
    "8000" = "8000"
  }

  volumes = [
    "${path.module}/presentation.md:/app/presentation.md:Z",
    "${path.module}/theme.css:/app/reveal.js/css/theme/custom.css:Z"
  ]

  command = ["sh", "-c", "/app/start.sh"]
}
