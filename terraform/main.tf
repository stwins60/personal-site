
resource "docker_container" "this" {
  name  = "personal-site"
  image = "${var.image_name}:${var.image_tag}"
  ports {
    internal = 5001
    external = var.external_port
  }
  provider = docker
  
}