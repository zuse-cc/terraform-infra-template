# Example Terraform module for creating a Linode object storage bucket
module "default" {
  source  = "{{ module }}"
  stage   = var.env
  region  = var.region
  service = var.label
}
