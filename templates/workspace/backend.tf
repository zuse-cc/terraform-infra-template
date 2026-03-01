terraform {
  backend "s3" {
    bucket = "{{ tf_state_bucket }}"
    region = "{{ tf_state_region }}"
    key    = "{{ workspace_dir }}/terraform.tfstate"

    # All of these skip_* arguments are used since Linode object storage doesn't implement these additional endpoints
    skip_region_validation      = true
    skip_credentials_validation = true
    skip_requesting_account_id  = true
    skip_metadata_api_check     = true
    skip_s3_checksum            = true

    use_path_style = true
    use_lockfile   = true

    endpoints = {
      s3 = "{{ tf_state_s3_endpoint }}"
    }
  }
}
