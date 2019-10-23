"""
aws functions
"""
import os

from boto3 import Session
import botocore


def get_missing_vars(aws):
    """
    return a list of missing required env vars if any
    """
    required = [
        "AWS_SECRETS_NAME",
        "AWS_ACCESS_KEY",
        "AWS_SECRET_ACCESS_KEY",
    ]
    return [f'Missing env variable "{v}"' for v in required if aws.get(v, None) is None]

def get_session():
    # use the session so this will work locally with ~/.aws/config
    if os.getenv("AWS_ACCESS_KEY") and os.getenv("AWS_SECRET_ACCESS_KEY") and os.getenv("AWS_SECRET_ACCESS_KEY"):
        session = Session(os.getenv("AWS_ACCESS_KEY"), os.getenv("AWS_SECRET_ACCESS_KEY"), os.getenv("AWS_SECRET_ACCESS_KEY"))
    else:
        session = Session()
    return session

def get_aws_vars():
    session = get_session()
    credentials = session.get_credentials()
    return {
        "AWS_ACCESS_KEY": getattr(credentials, "access_key") if credentials else None,
        "AWS_SECRET_ACCESS_KEY": getattr(credentials, "secret_key")
        if credentials
        else None,
        "AWS_DEFAULT_REGION": session.region_name,
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
