#!/usr/bin/env python
"""
This populates environment variables from amazon secrets store and chain loads another program.
"""
import json
import os
import sys

from utils.aws import get_aws_vars, get_missing_vars, get_aws_account
from utils.secrets import get_secret, mask_secret

def main():
    if len(sys.argv) < 3:
        print(
            "\nUsage: secrets_loader [CONFIG_NAME] [program] [arguments]\n\n"
            "example: ./secrets_loader GOZER_API /usr/bin/env\n\n"
            "[CONFIG_NAME] is the name of the configuration blob you want to get\n"
            "  from the secrets blob.\n"
            "[program] is the program you wish to run\n"
            "[arguments] are optional program arguments\n\n"
            "You must have the following environment variables defined:\n"
            "    AWS_SECRETS_NAME, AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY\n"
            "    AWS_SECRETS_NAME is the name of the secrets blob you're interested in.\n"
        )
        sys.exit(-1)

    config_name = sys.argv[1]
    run_command = sys.argv[2]
    run_args = sys.argv[2:]

    get_aws_account()
    aws = get_aws_vars()
    if get_missing_vars(aws):
        print("\n".join(get_missing_vars(aws)))
        sys.exit(-1)

    secrets, error = get_secret(
        aws.get("AWS_SECRETS_NAME"), region_name=aws.get("AWS_DEFAULT_REGION")
    )
    if error:
        print(f"\n{error}")
        print(
            f"\nUsing the following:\n"
            f"AWS_SECRETS_NAME={aws['AWS_SECRETS_NAME']}\n"
            f"AWS_ACCESS_KEY={aws['AWS_ACCESS_KEY']}\n"
            f"AWS_SECRET_ACCESS_KEY={mask_secret(aws['AWS_SECRET_ACCESS_KEY'])}\n"
            f"AWS_DEFAULT_REGION={aws['AWS_DEFAULT_REGION']}\n"
        )
        print(f"AWS Account# {get_aws_account()}\n")
        sys.exit(-1)

    if secrets:
        secrets = json.loads(secrets)
        secrets = secrets.get(config_name, {})
        if len(secrets.keys()) == 0:
            print(f'Warning: no secrets defined for config name "{config_name}"')

        for secret in secrets:
            os.environ[secret] = secrets[secret]

    try:
        os.execl(run_command, *run_args)
    except Exception as e:
        print(f'Trying to run "{run_command}" with arguments {run_args[1:]}')
        print(str(e))
        sys.exit(-1)

if __name__ == "__main__":
    main()
    