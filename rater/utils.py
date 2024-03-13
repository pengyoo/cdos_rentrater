import logging
import boto3
from botocore.exceptions import ClientError
import os
import io
from PIL import Image
from django.conf import settings

# Upload file to s3


def upload_file(file_name, object_name=None, bucket=settings.S3_BUCKET):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_fileobj(
            file_name, bucket, object_name)
        s3_client.put_object_acl(
            Bucket=bucket,
            Key=object_name,
            ACL='public-read'
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True
