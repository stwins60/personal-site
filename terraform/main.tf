
resource "docker_container" "this" {
  name  = var.container_name
  image = "${var.image_name}:${var.image_tag}"
  ports {
    internal = 5001
    external = var.external_port
  }
  provider = docker
  
}