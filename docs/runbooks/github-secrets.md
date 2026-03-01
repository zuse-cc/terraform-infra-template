# GitHub Workspace Secrets

These secrets are needed for the GitHub actions workflow to authenticate with cloud providers. To prevent them from being exposed in the repo itself, we store them as [secrets](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/using-secrets-in-github-actions) instead.

- Secrets are stored in GHA in two environments: `read-only` and `deployment`
- The former is used in pull requests for `terraform plan`, the latter is for `apply` after merging
- To get the values for the required secrets, some TF operations need to be run locally

**LINODE_TOKEN**

- Apply the workspace configuration in [./linode/shared/global/terraform](../../linode/shared/global/terraform/)
- Get the value of `linode_token` and store it as `LINODE_TOKEN` in Github

```sh
terraform output -raw linode_token; echo
```

**AWS_CREDENTIALS**

- Apply the workspace configuration in [./linode/shared/global/terraform](../../linode/shared/global/terraform/)

```sh
terraform -chdir=linode/shared/global/terraform apply
```

- Using the TF outputs, generate the AWS shared credentials file to use in GHA:

```sh
cat << EOF | base64
[default]
aws_access_key_id = $(terraform -chdir=linode/shared/global/terraform output -raw tfstate_access_key_id)
aws_secret_access_key = $(terraform -chdir=linode/shared/global/terraform output -raw tfstate_secret_access_key)
EOF
```

- Store the output as `AWS_CREDENTIALS` in Github

## Environment and Branch Protection Rules

> [!CAUTION]
> You MUST setup protection rules for the `main` branch and the `deployment` environment or anyone could make changes to live infrastructure. The `read-only` environment should only contain credentials with access needed to run `terraform plan`.

![Environment protection rules](../images/env-protection.png)
