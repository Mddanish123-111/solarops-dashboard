provider "aws" {
  region = "ap-south-1"
}

resource "aws_vpc" "solarops_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "solarops-vpc"
  }
}

resource "aws_subnet" "solarops_subnet" {
  vpc_id            = aws_vpc.solarops_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "ap-south-1a"
  tags = {
    Name = "solarops-subnet"
  }
}

resource "aws_internet_gateway" "solarops_igw" {
  vpc_id = aws_vpc.solarops_vpc.id
  tags = {
    Name = "solarops-igw"
  }
}

resource "aws_security_group" "solarops_sg" {
  name   = "solarops-sg"
  vpc_id = aws_vpc.solarops_vpc.id

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "solarops-sg"
  }
}