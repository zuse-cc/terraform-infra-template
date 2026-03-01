module "terraform_backend" {
  source  = "https://github.com/joerx/terraform-linode-bucket/releases/download/v0.1.1/terraform-linode-bucket.tar.gz"
  stage   = var.env
  service = var.label
  region  = var.region
}

locals {
  label = "${var.env}-tf-${var.label}-rw"
}

# Linode access token and OSS credentials to access terraform state
# These are intended to be used for deployment in GHA workflows
resource "linode_object_storage_key" "k" {
  label = local.label

  bucket_access {
    bucket_name = module.terraform_backend.bucket
    region      = var.region
    permissions = "read_write"
  }
}

resource "linode_token" "t" {
  label  = local.label
  scopes = "*"
}
