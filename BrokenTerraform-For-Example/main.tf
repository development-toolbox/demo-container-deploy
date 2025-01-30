provider "podman" {
  uri = "unix:///run/user/$(id -u)/podman/podman.sock"
}

resource "podman_image" "revealjs" {
  name   = "revealjs"
  source = "./Dockerfile"
}

resource "podman_container" "revealjs_presentation" {
  image = podman_image.revealjs.id
  name  = "revealjs-container"

  ports {
    external = 8000
    internal = 8000
  }

  volumes = [
    "${path.module}/presentation.md:/app/presentation.md",
    "${path.module}/theme.css:/app/reveal.js/css/theme/custom.css"
  ]

  command = ["sh", "-c", "/app/start.sh"]
}