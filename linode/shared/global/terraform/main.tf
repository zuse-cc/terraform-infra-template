module "terraform_backend" {
  source  = "https://github.com/joerx/terraform-linode-bucket/releases/download/v0.1.1/terraform-linode-bucket.tar.gz"
  stage   = var.env
  service = var.label
  region  = var.region
}

# Linode access token and OSS credentials to access terraform state
# These are intended to be used for deployment in GHA workflows
resource "linode_object_storage_key" "k" {
  label = "${var.env}-tfstate-${var.label}-${var.region}-rw"

  # The repo uses multiple backends, so we cannot restrict this key
  # FIXME: Migrate repo to use a single shared state bucket instead
  bucket_access {
    bucket_name = module.terraform_backend.bucket
    region      = var.region
    permissions = "read_write"
  }
}

resource "linode_token" "t" {
  label  = "token"
  scopes = "*"
}
