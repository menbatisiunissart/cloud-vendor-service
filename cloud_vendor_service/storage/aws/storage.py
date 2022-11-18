import os
import logging
import botocore.exceptions
from cloud_vendor_service.client.aws.session import get_s3_client
from cloud_vendor_service.environment import VENDOR

logger = logging.getLogger(__name__)
s3_client = get_s3_client()

def upload_blob(
    source_file_name: str,
    destination_blob_name: str,
    bucket_name: str
    ) -> str:
    """
    Upload a file to the bucket in cloud storage.
    :param source_file_name: Local path of the file to upload (e.g. "local/path/to/file")
    :param destination_blob_name: Destination path of the file
    :param bucket_name: The name of the bucket
    :return storage_path: Destination path of the file
    """
    if bucket_name is not None:
        raise NotImplementedError(f'custom bucket not supported for vendor {VENDOR.AWS.name}')
    s3_client.upload_file(source_file_name, bucket_name, destination_blob_name)
    return destination_blob_name

def download_blob(local_file_path: str, origin_file_path: str, bucket_name: str):
    """
    Download a file from the bucket in cloud storage.
    :param local_file_path: Local path to where the file will be downloaded to
    :param origin_file_path: Origin path from where the file will be downloaded from
    :param bucket_name: The name of the bucket
    Return name: Local path of where the downloaded file is
    """
    logger.info("downloading blob. bucket=%s, src_path=%s, dest_path=%s", bucket_name, origin_file_path, local_file_path)
    try:
        s3_client.download_file(bucket_name, origin_file_path, local_file_path)
    except botocore.exceptions.ClientError as e:
        logger.error("an error has occured when trying to download the file. This file may not exist."
                    " bucket=%s, src_path=%s, dest_path=%s",
                    bucket_name,
                    origin_file_path,
                    local_file_path
        )
        if "404" in str(e):
            raise FileNotFoundError from e
        raise e
    return local_file_path

def download_dir(
    local: str,
    prefix: str,
    bucket_name: str,
    ):
    """
    params:
    - local: local path to folder in which to place files
    - prefix: pattern to match in s3
    - bucket_name: s3 bucket with target contents
    """
    keys = []
    dirs = []
    next_token = ''
    base_kwargs = {
        'Bucket':bucket_name,
        'Prefix':prefix,
    }
    while next_token is not None:
        kwargs = base_kwargs.copy()
        if next_token != '':
            kwargs.update({'ContinuationToken': next_token})
        results = s3_client.list_objects_v2(**kwargs)
        contents = results.get('Contents')
        for i in contents:
            k = i.get('Key')
            if k[-1] != '/':
                keys.append(k)
            else:
                dirs.append(k)
        next_token = results.get('NextContinuationToken')
    for d in dirs:
        dest_pathname = os.path.join(local, d)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
    for k in keys:
        dest_pathname = os.path.join(local, k)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
        s3_client.download_file(bucket_name, k, dest_pathname)