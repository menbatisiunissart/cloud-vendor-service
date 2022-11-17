import logging
import os
from cloud_vendor_service.credential.aws.session import get_s3_client
import botocore.exceptions
from cloud_vendor_service.environment import get_env_var, get_env, get_vendor, VENDOR, ENV
# TODO: import below librairies if need to enable Google cloud
# from google.cloud import storage

env = get_env()
FOLDER = env.name
STORAGE_BUCKET = get_env_var('STORAGE_BUCKET')
logger = logging.getLogger(__name__)

def upload_file(file_path: str, destination_path: str, bucket_name: str=None):
    storage_path = upload_blob(file_path, destination_path, bucket_name=bucket_name)
    if env != ENV.LOCAL:
        os.remove(file_path)
    return storage_path

def upload_blob(source_file_name: str, destination_blob_name: str, bucket_name: str=None):
    """
    Upload a file to the bucket in cloud storage.
    :param source_file_name: Local path of the file to upload (e.g. "local/path/to/file")
    :param destination_blob_name: Destination path of the file
    :param bucket_name: (Optional) The ID of your GCS bucket
    :return name: Destination path of the file
    """
    vendor = get_vendor()
    print(f'vendor = {vendor}')
    storage_path = FOLDER+'/'+destination_blob_name
    if vendor == VENDOR.AWS:
        s3 = get_s3_client()
        if bucket_name is not None:
            raise NotImplementedError(f'custom bucket not supported for vendor {VENDOR.AWS.name}')
        # TODO: add blees-ai-factory default bucket
        s3.upload_file(source_file_name, STORAGE_BUCKET, storage_path)
    elif vendor == VENDOR.GOOGLE:
        if bucket_name is None:
            bucket_name = STORAGE_BUCKET
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(storage_path)
        blob.upload_from_filename(source_file_name)
    else:
        raise NotImplementedError(f"cannot upload blob for vendor = {vendor}")
    return storage_path

def download_blob(local_file_path, origin_file_path, bucket_name=None):
    """
    Download a file from the bucket in cloud storage.
    :param local_file_path: Local path to where the file will be downloaded to
    :param origin_file_path: Origin path from where the file will be downloaded from
    :param bucket_name: (Optional) The ID of your GCS bucket
    Return name: Local path of where the downloaded file is
    """
    if bucket_name is None:
        bucket_name = STORAGE_BUCKET
    vendor = get_vendor()
    if vendor == VENDOR.AWS:
        s3 = get_s3_client()
        logger.info("downloading blob. bucket=%s, src_path=%s, dest_path=%s", bucket_name, origin_file_path, local_file_path)
        try:
            s3.download_file(bucket_name, origin_file_path, local_file_path)
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
    elif vendor == VENDOR.GOOGLE:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(FOLDER+'/'+origin_file_path)
        blob.download_to_filename(local_file_path)
    else:
        raise ValueError(f"invalid vendor: {vendor}")
    return local_file_path

def file_name(file_path):
    file_name = os.path.basename(file_path)
    return file_name


