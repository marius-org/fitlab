variable "aws_region" {
  default = "eu-west-1"
}

variable "instance_type" {
  default = "t3.micro"
}

variable "key_name" {
  description = "Name of the SSH key pair in AWS"
  default     = "fitlab-key"
}

variable "public_key_path" {
  description = "Path to your local public SSH key"
  default     = "~/.ssh/id_rsa.pub"
}
