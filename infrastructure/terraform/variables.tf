variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "sitewatch"
}

variable "aws_region" {
  description = "Região AWS"
  type        = string
  default     = "sa-east-1"
}

variable "my_ip" {
  description = "Seu IP público com /32"
  type        = string
}

variable "key_name" {
  description = "Nome da chave SSH existente na AWS"
  type        = string
}
