import base64

import boto3
from botocore.exceptions import ClientError


# this function tweaked from aws secretsmanager template
def get_secret(secret_name, session):
    # Create a Secrets Manager client
    client = session.client(service_name="secretsmanager")

    secret = None
    error = None
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            error = str(e)
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            error = str(e)
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            error = str(e)
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            error = str(e)
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            error = f"{str(e)} (looking in {region_name})"
        elif e.response["Error"]["Code"] == "InvalidClientTokenId":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            error = str(e)
        elif e.response["Error"]["Code"] == "SignatureDoesNotMatch":
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            error = str(e)
        else:
            # any other random issue...
            error = str(e)
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = base64.b64decode(get_secret_value_response["SecretBinary"])

    return secret, error


def mask_secret(secret):
    return "*" * (len(secret) - 4) + secret[-4:]
