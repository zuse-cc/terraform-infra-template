# Terraform Infrastructure

Terraform deployment repository template

## Usage

```sh
OWNER=...
SERVICE=...
gh repo create ${OWNER}/${SERVICE}-infra --template zuse-cc/terraform-module-template --private
git clone git@github.com:${OWNER}/${SERVICE}-infra
```

## Setup

- One time setup to install dependencies:

```sh
make venv
```

- Edit [linode/shared/global/terraform/terraform.tfvars](./linode/shared/global/terraform/terraform.tfvars), set `label`
- Apply backend configuration:

```sh
terraform -chdir=linode/shared/global/terraform init
terraform -chdir=linode/shared/global/terraform apply
```

- Then uncomment the backend config in `linode/shared/global/terraform/backend.tf`
- Replace the bucket name with the bucket we just created (see Terraform outputs)
- Migrate the local state to the remote backend:

```sh
terraform -chdir=linode/shared/global/terraform init -migrate-state
```

- Set `TF_STATE_BUCKET` in `generate.py` to the bucket just created
- See [this runbook](./docs/runbooks/github-secrets.md) to set up required secrets in GHA

## Generators

- To generate a generic workspace config:

```sh
./generate.py workspace --name foo
```

- To preview what would be generated, pass `--dry-run`

```sh
./generate.py --debug --dry-run workspace --name foo
```
