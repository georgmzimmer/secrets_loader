"""
aws functions
"""
import os

import botocore
from boto3 import Session


def get_missing_vars(aws):
    """
    return a list of missing required env vars if any
    """
    required = ["AWS_SECRETS_NAME", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"]
    return [f'Missing env variable "{v}"' for v in required if aws.get(v, None) is None]


def get_session():
    # use the session so this will work locally with ~/.aws/config or aws machine role
    if (
        os.getenv("AWS_ACCESS_KEY_ID")
        and os.getenv("AWS_SECRET_ACCESS_KEY")
        and os.getenv("AWS_DEFAULT_REGION")
    ):
        session = Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION"),
        )
    else:
        session = Session()
    return session


def get_aws_vars():
    session = get_session()
    credentials = session.get_credentials()
    return {
        "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "AWS_DEFAULT_REGION": os.getenv("AWS_DEFAULT_REGION"),
        "AWS_SECRETS_NAME": os.environ.get("AWS_SECRETS_NAME"),
    }


def get_aws_account():
    session = get_session()
    sts_client = session.client(service_name="sts")
    org_client = session.client(service_name="organizations")
    try:
        identity = sts_client.get_caller_identity()
    except botocore.exceptions.NoCredentialsError:
        return "No Credentials"

    account_id = identity["Account"]
    arn = identity["Arn"]
    try:
        name = (
            org_client.describe_account(AccountId=account_id).get("Account").get("Name")
        )
    except:
        name = "* Unknown Name *"
    return f"{arn} ({name})"
