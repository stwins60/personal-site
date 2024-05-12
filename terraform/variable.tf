variable "image_name" {
  type        = string
  description = "Name of the Docker image"
}

variable "image_tag" {
  type        = string
  description = "Tag of the Docker image"
}

variable "external_port" {
  type        = number
  description = "Port to expose the container"
}