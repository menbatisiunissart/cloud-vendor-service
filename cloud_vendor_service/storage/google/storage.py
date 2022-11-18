# TODO: import below librairies if need to enable Google cloud
# from google.cloud import storage

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
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    return destination_blob_name

def download_blob(
    local_file_path: str,
    origin_file_path: str,
    bucket_name: str
    ):
    """
    Download a file from the bucket in cloud storage.
    :param local_file_path: Local path to where the file will be downloaded to
    :param origin_file_path: Origin path from where the file will be downloaded from
    :param bucket_name: (Optional) The ID of your GCS bucket
    Return name: Local path of where the downloaded file is
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(origin_file_path)
    blob.download_to_filename(local_file_path)
    return local_file_path