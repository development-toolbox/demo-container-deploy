terraform {
  required_version = ">= 1.0.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

variable "use_podman" {
  description = "Set to true if using Podman, false if using Docker"
  type        = bool
  default     = false  # Set this to true for local Podman use
}

provider "docker" {
  host = var.use_podman ? "unix:///run/user/${var.user_id}/podman/podman.sock" : "unix:///var/run/docker.sock"
}

variable "user_id" {
  type    = number
  default = 1000  # Change this based on your system user ID
}

resource "docker_image" "revealjs" {
  name = "revealjs"
  
  build {
    context    = path.module
    dockerfile = "${path.module}/Dockerfile"
  }
}

resource "docker_container" "revealjs_presentation" {
  image = docker_image.revealjs.image_id
  name  = "revealjs-container"

  ports {
    internal = 8000
    external = 8000
  }

  mounts {
    target = "/app/presentation.md"
    source = "${path.module}/presentation.md"
    type   = "bind"
  }

  mounts {
    target = "/app/reveal.js/css/theme/custom.css"
    source = "${path.module}/theme.css"
    type   = "bind"
  }

  command = ["sh", "-c", "/app/start.sh"]
}
