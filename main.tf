terraform {
  required_version = ">= 1.0.0"
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  uri = "unix:///run/user/${var.user_id}/podman/podman.sock"
}

variable "user_id" {
  type    = number
  default = "1000"  # Change this based on your user ID dynamically
}

resource "docker_image" "revealjs" {
  name       = "revealjs"
  dockerfile = "${path.module}/Dockerfile"
  context    = path.module
}

resource "docker_container" "revealjs_presentation" {
  image = docker_image.revealjs.id
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
