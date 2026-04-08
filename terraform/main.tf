terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Upload your public SSH key to AWS
resource "aws_key_pair" "fitlab" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

# Firewall rules
resource "aws_security_group" "fitlab" {
  name        = "fitlab-sg"
  description = "Allow SSH and HTTP"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance
resource "aws_instance" "fitlab" {
  ami                    = "ami-0a422d70f727fe93e" # Ubuntu 24.04 eu-west-1
  instance_type          = var.instance_type
  key_name               = aws_key_pair.fitlab.key_name
  vpc_security_group_ids = [aws_security_group.fitlab.id]

  tags = {
    Name = "fitlab"
  }
}
