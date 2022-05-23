from os import path, environ, makedirs
import logging
import boto3
from botocore.exceptions import ClientError
from utils import timestamp


def session(aws_access_key_id, aws_secret_access_key):
    try:
        boto_session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        # Log everything. Change to 'INFO', or comment out to disable detailed AWS logging
        boto3.set_stream_logger(environ["BOTO3_LOG_LEVEL"], logging.INFO)

        if boto_session:
            return boto_session
        else:
            raise Exception("No boto3 session")
    except Exception as err_session:
        raise err_session


def get_s3_bucket(boto_session, s3_bucket):
    try:
        s3 = boto_session.resource('s3')
        bucket = s3.Bucket(s3_bucket)
        return bucket
    except Exception as err_get_bucket:
        raise err_get_bucket


def download_s3_object(boto_session, s3_bucket, s3_key_prefix, output_path, include_dir_structure):
    download_timestamp = timestamp(
        environ["BOTO3_DATE_TIME_FORMAT"])
    for s3_object in s3_bucket.objects.all():
        key = s3_object.key
        obj = path.split(s3_object.key)[1]
        if key.startswith(s3_key_prefix) and obj:
            try:
                if include_dir_structure:
                    directories = path.split(key)[0]
                    output_directory = path.join(
                        output_path, download_timestamp, directories)
                else:
                    output_directory = path.join(
                        output_path, download_timestamp)

                # # Create directories if its not existing
                if not path.exists(output_directory):
                    makedirs(output_directory)

                output_file = path.join(
                    output_directory, obj)

                # # Download file
                s3_bucket.download_file(key, output_file)

            except Exception as err_download:
                raise err_download
        elif s3_key_prefix == "*" and obj:
            try:
                if include_dir_structure:
                    directories = path.split(key)[0]
                    output_directory = path.join(
                        output_path, download_timestamp, directories)
                else:
                    output_directory = path.join(
                        output_path, download_timestamp)

                if not path.exists(output_directory):
                    makedirs(output_directory)

                output_file = path.join(
                    output_directory, obj)

                # # Download file
                s3_bucket.download_file(key, output_file)
            except Exception as err_download:
                raise err_download
        else:
            try:
                print("Skip " + obj)
            except Exception as err_download:
                raise err_download
