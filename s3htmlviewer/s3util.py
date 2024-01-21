import logging
import os

from minio import Minio

client = Minio(os.environ['S3_ENDPOINT_URL'],
               access_key=os.environ['S3_ACCESS_KEY_ID'],
               secret_key=os.environ['S3_SECRET_KEY'])


def get_files(parent=None, allow=None):
    logging.info("gettingshit")
    if allow is None:
        allow = ["folder"]
    for obj in client.list_objects(bucket_name=os.environ['S3_BUCKET_NAME'], recursive=False, include_version=False,
                                   include_user_meta=False, prefix=parent):
        if (obj.is_dir and "folder" in allow) or (not obj.is_dir and "file" in allow):
            yield obj.object_name


def get_file(file_path):
    return client.get_object(bucket_name=os.environ['S3_BUCKET_NAME'], object_name=file_path)
