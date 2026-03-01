# Apply this workspace locally first & replace the bucket name below 
# Then uncomment the `backend` block below & run `terraform init -migrate-state`
# Don't forget to update TF_STATE_BUCKET in ./generate.py as well

terraform {
  # backend "s3" {
  #   bucket = "<replace me>"
  #   region = "eu-central"
  #   key    = "linode/shared/global/terraform/terraform.tfstate"

  #   # All of these skip_* arguments are used since Linode object storage doesn't implement these additional endpoints
  #   skip_region_validation      = true
  #   skip_credentials_validation = true
  #   skip_requesting_account_id  = true
  #   skip_metadata_api_check     = true
  #   skip_s3_checksum            = true

  #   use_path_style = true
  #   use_lockfile   = true

  #   endpoints = {
  #     s3 = "https://eu-central-1.linodeobjects.com"
  #   }
  # }
}
