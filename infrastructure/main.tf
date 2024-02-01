provider "aws" {
  region = "us-east-1"
  profile = "digital-bank-developers"
}

resource "aws_instance" "spring-petclinic" {
    ami = "ami-03a6eaae9938c858c"
    instance_type = "t3a.micro"
    associate_public_ip_address = true
    subnet_id = "subnet-0e87e3af1cd8ed790"

    tags = {
      Name = "spring-petclinic-instance"
      #CostCentre = "WTF Cost Centre"
    }
  
}