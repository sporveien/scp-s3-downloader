from os import path, environ, makedirs
import logging
import boto3
import pytz
from botocore.exceptions import ClientError
from datetime import datetime
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


def download_s3_object(s3_bucket, s3_key_prefix, output_path, include_dir_structure, use_timestamp_container, latest_archive_dt):
    try:
        download_timestamp = timestamp(
            environ["BOTO3_DATE_TIME_FORMAT"])

        downloaded_s3_objects = []
        for s3_object in s3_bucket.objects.all():

            skipDownload = False

            key = s3_object.key
            obj = path.split(s3_object.key)[1]

            s3_obj_last_modified_dt = s3_object.last_modified

            if isinstance(latest_archive_dt, datetime) and isinstance(s3_obj_last_modified_dt, datetime):

                log_msg = str(
                    "Compare latest archiving datetime to only download the latest S3 object(s)")
                logging.debug(log_msg)

                try:
                    s3_obj_utc = s3_obj_last_modified_dt.astimezone(
                        pytz.UTC)
                    latest_archive_utc = latest_archive_dt.astimezone(
                        pytz.UTC)

                    log_msg = str(
                        "S3 Object '{0}' last modified (UTC) '{1}'").format(obj, s3_obj_utc)
                    logging.info(log_msg)

                    log_msg = str(
                        "S3 Object '{0}' last modified (UTC) '{1}'").format(obj, s3_obj_utc)
                    logging.info(log_msg)

                    if s3_obj_utc < latest_archive_utc:
                        log_msg = str("Latest archive datetime {0} is newer than S3 object last modified datetime {1}").format(
                            latest_archive_utc, s3_obj_utc)
                        logging.debug(log_msg)

                        log_msg = str(
                            "Skip download S3 object {0}").format(obj)
                        logging.info(log_msg)

                        skipDownload = True
                except Exception as err_only_download_latest:
                    skipDownload = True
                    raise err_only_download_latest

            if skipDownload:
                continue

            if key.startswith(s3_key_prefix) and obj:
                try:
                    if include_dir_structure:
                        log_msg = str(
                            "Preserve the directory structure from S3 bucket within the output directory")
                        logging.debug(log_msg)

                        directories = path.split(key)[0]
                        if use_timestamp_container:
                            output_directory = path.join(
                                output_path, download_timestamp, directories)

                            log_msg = str("Output directory '{0}'").format(
                                output_directory)
                            logging.debug(log_msg)
                        else:

                            output_directory = path.join(
                                output_path, directories)
                            log_msg = str("Output directory '{0}'").format(
                                output_directory)
                            logging.debug(log_msg)

                    else:
                        log_msg = str(
                            "Do not keep S3 directory structure, download all files to a flat structure of the output directory")

                        if use_timestamp_container:
                            output_directory = path.join(
                                output_path, download_timestamp)
                            log_msg = str("Output directory '{0}'").format(
                                output_directory)
                            logging.debug(log_msg)
                        else:
                            output_directory = path.join(
                                output_path)
                            log_msg = str("Output directory '{0}'").format(
                                output_directory)
                            logging.debug(log_msg)

                    # Create directories if its not existing
                    if not path.exists(output_directory):
                        makedirs(output_directory)

                    output_file = path.join(
                        output_directory, obj)

                    # Download file
                    log_msg = str("Download '{0}'").format(key)
                    logging.info(log_msg)

                    s3_bucket.download_file(key, output_file)

                    log_msg = str("Downloaded '{0}'").format(output_file)
                    logging.info(log_msg)

                    downloaded_s3_objects.append(output_file)

                except Exception as err_download:
                    raise err_download
            elif s3_key_prefix == "*" and obj:
                try:

                    if include_dir_structure:
                        log_msg = str(
                            "Preserve the directory structure from S3 bucket within the output directory")
                        logging.debug(log_msg)

                        directories = path.split(key)[0]

                        output_directory = path.join(
                            output_path, download_timestamp, directories)

                        log_msg = str("Output directory '{0}'").format(
                            output_directory)
                        logging.debug(log_msg)

                    else:
                        output_directory = path.join(
                            output_path, download_timestamp)

                        log_msg = str("Output directory '{0}'").format(
                            output_directory)
                        logging.debug(log_msg)

                    if not path.exists(output_directory):
                        makedirs(output_directory)

                    output_file = path.join(
                        output_directory, obj)

                    # Download file
                    log_msg = str("Download '{0}'").format(key)
                    logging.info(log_msg)

                    s3_bucket.download_file(key, output_file)

                    log_msg = str("Downloaded '{0}'").format(output_file)
                    logging.info(log_msg)

                    downloaded_s3_objects.append(output_file)

                except Exception as err_download:
                    raise err_download

            else:
                try:
                    log_msg = str(
                        "Skip downloading object {0}, the key '{1}' does not match configuration").format(obj, key)
                    logging.debug(log_msg)
                except Exception as err_download:
                    raise err_download
        return downloaded_s3_objects
    except Exception as download_s3_object:
        raise download_s3_object
