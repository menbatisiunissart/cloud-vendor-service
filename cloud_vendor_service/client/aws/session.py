"""Credential-related functions for AWS."""
import os
import dotenv
import boto3
import sagemaker
import sagemaker.local
from cloud_vendor_service.storage.aws.client_types import S3Client


def get_sessions_and_role(local: bool = False):
    """Return session and credentials for API calls.

    :param local: Specifies whether or not to use a local session.

    :return: Boto session, sagemaker, execution role
    :rtype: Tuple[boto_session, sagemaker_session, role]

    :note:

    Credentials should be specified within a top-level .env file as follows:

        AWS_ACCESS_KEY_ID=...
        AWS_SECRET_ACCESS_KEY=...
        ROLE=arn:aws:iam::...:role/...
    """
    dotenv.load_dotenv()  # load credentials from .env file
    boto_session = boto3.Session(
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_REGION"],
    )
    if local:
        sagemaker_session = sagemaker.local.LocalSession(boto_session=boto_session)
        sagemaker_session.config = {"local": {"local_code": True}}
    else:
        sagemaker_session = sagemaker.Session(boto_session=boto_session)
    return boto_session, sagemaker_session, os.environ["ROLE"]


def get_s3_client() -> S3Client:
    boto_session, _, _ = get_sessions_and_role()
    return boto_session.resource("s3").meta.client
