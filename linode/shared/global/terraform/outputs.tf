output "bucket" {
  value = module.terraform_backend.bucket
}

output "endpoint" {
  value = module.terraform_backend.endpoint
}

output "tfstate_access_key_id" {
  sensitive = true
  value     = linode_object_storage_key.k.access_key
}

output "tfstate_secret_access_key" {
  sensitive = true
  value     = linode_object_storage_key.k.secret_key
}

output "linode_token" {
  sensitive = true
  value     = linode_token.t.token
}
