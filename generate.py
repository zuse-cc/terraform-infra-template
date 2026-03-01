#!/usr/bin/env python3

import argparse
import sys
import os
import shutil
import subprocess
import logging

import petname

from jinja2 import Environment, FileSystemLoader, select_autoescape

TF_STATE_BUCKET = "<replace-me>"
TF_STATE_REGION = "eu-central"
TF_STATE_S3_ENDPOINT = "https://eu-central-1.linodeobjects.com"

LINODE_TOKEN = os.environ.get("LINODE_TOKEN", None)
LINODE_OSS_API_URL = "https://api.linode.com/v4/object-storage"

PROVIDERS = ["linode"]
ENVIRONMENTS = ["dev"]
REGIONS = ["eu-central"]

DEFAULTS = {
    "module": "https://github.com/joerx/terraform-linode-bucket/releases/download/v0.1.0/terraform-linode-bucket.tar.gz",
    "domain": "<replace-me>.zuse.systems",
    "provider": PROVIDERS[0],
    "env": ENVIRONMENTS[0],
    "region": REGIONS[0],
}

def parse_args():
    # Root parser with common flags
    parser = argparse.ArgumentParser(description="Generate Terraform configuration from templates")
    parser.add_argument("--dry-run", action="store_true", help="Dry run, do not write output files, only print contents to stderr")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing output files")
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')

    subparsers = parser.add_subparsers(dest='template')

    # Subparser for workspace command
    workspace_parser = subparsers.add_parser('workspace', help='Generate generic workspace configuration')
    workspace_parser.set_defaults(func=render_workspace)
    workspace_parser.add_argument('--name', required=True, help='Name of the workspace')
    workspace_parser.add_argument('--module', default=DEFAULTS['module'], help='Terraform module source URL')
    workspace_parser.add_argument('--provider', default=DEFAULTS['provider'], choices=PROVIDERS, help='Cloud provider')
    workspace_parser.add_argument('--env', default=DEFAULTS['env'], choices=ENVIRONMENTS, help='Environment name')
    workspace_parser.add_argument('--region', default=DEFAULTS['region'], choices=REGIONS, help='Linode region')

    return parser.parse_args()


def check_format(file):
    """Check and format the given Terraform file using 'terraform fmt'.
    If 'terraform' is not found in the system path, it will print a warning."""

    if shutil.which("terraform") is None:
        logging.warning("Terraform not found in PATH, will skip formatting")
        return

    cmd = ["terraform", "fmt", file]
    cp = subprocess.run(cmd)
    if cp.returncode != 0:
        logging.warning("'%s' failed with exit code %s, ignoring", cmd, cp.returncode)


def render_workspace(params, **flags):
    """Render a generic workspace configuration based on the provided parameters."""
    logging.debug("Rendering generic workspace configuration")

    base_dir = f"{params['provider']}/{params['env']}/{params['region']}/{params['name']}"

    params["workspace_dir"] = base_dir
    params["tf_state_bucket"] = TF_STATE_BUCKET
    params["tf_state_region"] = TF_STATE_REGION
    params["tf_state_s3_endpoint"] = TF_STATE_S3_ENDPOINT

    render_templates("workspace", base_dir, params, **flags)

    print(f"Created new workspace config in {base_dir}", file=sys.stderr)
    print(file=sys.stderr)


def render_template(file, env, params, fp):
    """Render a single template file with the given parameters.
    Output will be streamed to the provided file-like object."""

    template = env.get_template(file)
    out = template.render(**params)
    print(out, file=fp)


def render_templates(template, out_dir, params, dry_run=False, force=False, file_filter=None):
    """Render templates from the specified directory with the given parameters.
    If dry_run is True, it will only print the rendered output to stderr without writing files.
    If force is True, it will overwrite any existing output files."""

    logging.debug("Rendering templates for %s with parameters: %s", template, params)

    template_dir = f"templates/{template}"
    if not os.path.exists(template_dir):
        raise ValueError(f"Template directory {template_dir} does not exist")

    j2env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True
    )

    _params = params | {
        "workspace_dir": out_dir,
    }

    if file_filter is not None:
        logging.debug("Applying file_filter to template list")
        template_list = file_filter
    else:
        template_list = j2env.list_templates()

    if dry_run:
        for t in template_list:
            fp = sys.stdout
            print(f"# {out_dir}/{t}", file=fp)
            render_template(t, j2env, _params, fp)
            print()

    else:
        if os.path.exists(out_dir) and not force:
            raise ValueError(f"Directory {out_dir} already exists, use '--force' to overwrite")

        os.makedirs(out_dir, exist_ok=True)

        for t in template_list:
            out_file = f"{out_dir}/{t}"
            with open(out_file, "w") as fp:
                render_template(t, j2env, _params, fp)
            if is_tf_file(out_file):
                check_format(out_file)


def safe_del(d, key):
    """Safely delete a key from a dictionary if it exists."""
    if key in d:
        del d[key]


def main():
    args = parse_args()

    log_level = logging.WARNING
    if args.debug:
        log_level = logging.DEBUG

    logging.basicConfig(encoding='utf-8', level=log_level, stream=sys.stderr)
    logging.debug("Parsed arguments: %s", args)

    params = args.__dict__.copy()
    safe_del(params, "func")
    safe_del(params, "dry_run")
    safe_del(params, "force")

    # Only catch ValueErrors, for all others dump the stack trace
    # Even better would be a custom exception class
    try:
        logging.debug("Parsed parameters: %s", params)
        args.func(params, dry_run=args.dry_run, force=args.force)
    except ValueError as ve:
        print(ve, file=sys.stderr)

if __name__ == "__main__":
    main()
