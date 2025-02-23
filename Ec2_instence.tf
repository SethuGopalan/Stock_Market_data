terraform {
  required_providers {
    aws = {
      source  = "hashcorp/aws"
      version = "3.76.1"
    }
    tls = {
      source  = "hashcorp/aws"
      version = "4.0.6"
    }
  }
}

provider "aws" {

  profile = "terraform"
  region  = "us-east-1"
}
resource "aws_security_group" "stock_security_group" {
  name        = "stock-security-group"
  description = "Allow SSH and HTTP trafic"

  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  engress {
    description = "Allow all outbount traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]

  }
}

resource "aws_instence" "Stock-data-srv" {

  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  key_name      = "Dev-Ops"

  security_groups = [
    aws_security_group.stock_security_group.name
  ]
  iam_instance_profile = aws_iam_instence_profile.stock_instence_profile.name

  tags = {
    name = "stock-data-Ec2"
  }

}

