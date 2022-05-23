from os import path
import logging
import boto3
from botocore.exceptions import ClientError


def session(aws_access_key_id, aws_secret_access_key):
    try:
        boto_session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        # Log everything. Change to 'INFO', or comment out to disable detailed AWS logging
        boto3.set_stream_logger('', logging.INFO)

        if boto_session:
            return boto_session
    except Exception as err_session:
        raise err_session


def get_bucket(boto_session, s3_bucket):
    try:
        s3 = boto_session.resource('s3')
        bucket = s3.Bucket(s3_bucket)
        return bucket
    except Exception as err_get_bucket:
        raise err_get_bucket
