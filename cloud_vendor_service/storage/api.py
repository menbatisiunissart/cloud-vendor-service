
import os
from cloud_vendor_service.environment import get_env_var, get_env, get_vendor, VENDOR, ENV

vendor = get_vendor()
if vendor == VENDOR.GOOGLE.name:
    import cloud_vendor_service.storage.google.storage as vendor_storage
elif vendor == VENDOR.AWS.name:
    import cloud_vendor_service.storage.aws.storage as vendor_storage
else:
    raise NotImplementedError(f"cannot upload blob for vendor = {vendor}")

env = get_env()
FOLDER = env.name
STORAGE_BUCKET = get_env_var('STORAGE_BUCKET')

def upload_file(file_path: str, destination_path: str, bucket_name: str=None):
    destination_path = FOLDER+'/'+destination_path
    storage_path = upload_blob(file_path, destination_path, bucket_name=bucket_name)
    if env != ENV.LOCAL:
        os.remove(file_path)
    return storage_path

def upload_blob(source_file_name: str, destination_blob_name: str, bucket_name: str=STORAGE_BUCKET):
    """
    Upload a file to the bucket in cloud storage.
    :param source_file_name: Local path of the file to upload (e.g. "local/path/to/file")
    :param destination_blob_name: Destination path of the file
    :param bucket_name: (Optional) The ID of your GCS bucket
    :return name: Destination path of the file
    """
    vendor_storage.upload_blob(
        source_file_name=source_file_name,
        destination_blob_name=destination_blob_name,
        bucket_name=bucket_name
    )
    return destination_blob_name

def download_blob(local_file_path: str, origin_file_path: str, bucket_name: str=STORAGE_BUCKET):
    """
    Download a file from the bucket in cloud storage.
    :param local_file_path: Local path to where the file will be downloaded to
    :param origin_file_path: Origin path from where the file will be downloaded from
    :param bucket_name: (Optional) The ID of your GCS bucket
    Return name: Local path of where the downloaded file is
    """
    origin_file_path = FOLDER+'/'+origin_file_path
    vendor_storage.download_blob(
        local_file_path=local_file_path,
        origin_file_path=origin_file_path,
        bucket_name=bucket_name
    )
    return local_file_path

def file_name(file_path):
    file_name = os.path.basename(file_path)
    return file_name


