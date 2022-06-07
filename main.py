import sys
import logging
import os
import yaml
import subprocess
from boto import get_s3_bucket, session, download_s3_object
from logger import logger
from datetime import datetime
from files import move_files, remove_archive, get_subdirectories, get_file_creation_datetime


def main():
    try:
        # .yml files
        try:
            # Read .yml config file
            with open("config.yml", 'r', encoding='utf8') as stream:
                conf = yaml.safe_load(stream)
            # Read .yml secrets file
            with open("secrets.yml", 'r', encoding='utf8') as stream:
                secrets = yaml.safe_load(stream)
        except Exception as err_yml:
            log_err = str(".yml exception: {0}").format(err_yml)
            print(log_err)
            raise log_err

        # Set environment variables from secrets file
        os.environ["AWS_ACCESS_KEY_ID"] = secrets['AWS_ACCESS_KEY']
        os.environ["AWS_SECRET_ACCESS_KEY"] = secrets['AWS_SECRET_KEY']

        # Set environment variables from config file
        os.environ["BOTO3_LOG_LEVEL"] = conf['BOTO3_LOG_LEVEL']
        os.environ["BOTO3_DATE_TIME_FORMAT"] = conf['BOTO3_DATE_TIME_FORMAT']

        # Start logger
        logger(conf['MAX_LOGFILES'], secrets['LOG_ROOT'],
               conf['LOG_FILE_EXTENTSION'], conf['LOG_DATE_TIME_FORMAT'])

        # Boto session
        logging.debug(
            "Starting Boto session")
        botosession = session(os.environ["AWS_ACCESS_KEY_ID"],
                              os.environ["AWS_SECRET_ACCESS_KEY"])
        logging.debug(
            "Boto session successfully started")

        # Get s3 bucket
        logging.debug(
            "Getting bucket '%s'", secrets['S3_BUCKET'])

        bucket = get_s3_bucket(botosession, secrets['S3_BUCKET'])
        print(bucket)
        logging.debug(
            "Successfully got s3 bucket '%s'", bucket.name)

        # Archive configuration and handle existing archives
        if conf["ARCHIVE_FILES"]:
            archive_root_path = secrets["ARCHIVE_ROOT"]
            archive_file_timestamp_format = conf["ARCHIVE_FILE_TIMESTAMP_FORMAT"]
            archive_file_prefix = conf["ARCHIVE_FILE_PREFIX"]
            archive_file_suffix = conf["ARCHIVE_FILE_SUFFIX"]
            archive_container_timestamp_format = conf["ARCHIVE_CONTAINER_TIMESTAMP_FORMAT"]
            archive_container_prefix = conf["ARCHIVE_CONTAINER_PREFIX"]
            archive_container_suffix = conf["ARCHIVE_CONTAINER_SUFFIX"]

            archives = get_subdirectories(archive_root_path)

            if conf["BOTO3_ONLY_DOWNLOAD_LATEST"] and len(archives) > 0:
                logging.debug("Configured to only download latest S3 objects compared to the latest archive")
                if conf["BOTO3_ONLY_DOWNLOAD_LATEST"] == True:
                    latest_archive = max(archives, key=os.path.getctime)
                    only_download_after_date = get_file_creation_datetime(
                        latest_archive)
                else:
                    only_download_after_date = datetime.strptime(
                        conf["BOTO3_ONLY_DOWNLOAD_LATEST"])
            else:
                logging.debug("No archives or configured to download all S3 objects")
                only_download_after_date = False

        # Take No Action
        if conf["TAKE_NO_ACTION"]:
            log_msg = str(
                "Take no action is turned on in .yml config")
            logging.info(log_msg)
            return

        downloaded = download_s3_object(bucket, secrets['S3_KEY_PREFIX'], secrets['DATA_ROOT'],
                                        conf['BOTO3_KEEP_DIRECTORY_STRUCTURE'], conf['BOTO3_USE_TIMESTAMP_CONTAINER'], only_download_after_date)

        if len(downloaded) < 1:
            log_msg = str(
                "No file(s) downloaded. Exiting..").format(downloaded)
            logging.info(log_msg)
            print(log_msg)
            return

        log_msg = str(
            "Downloaded file(s) {0}").format(downloaded)
        logging.info(log_msg)
        print(log_msg)

        if conf['BOTO3_USE_TIMESTAMP_CONTAINER']:
            log_msg = str(
                "Completed S3 download with 'BOTO3_USE_TIMESTAMP_CONTAINER' turned on (set to '{0}' in config.yml)").format(conf['BOTO3_USE_TIMESTAMP_CONTAINER'])
            logging.info(log_msg)
            print(log_msg)
            return downloaded

        # Archiving
        if not conf["ARCHIVE_FILES"]:
            log_msg = str(
                "Archiving is turned off in .yml config file")
            logging.info(log_msg)
            return

        # Move files to temp folder to make sure files are not locked. E.g. being written to by another user / job
        move_from_path = str(secrets["DATA_ROOT"])
        move_to_path = str(secrets["TEMP_ROOT"])

        log_msg = str("Move files from {0} to {1}").format(
            move_from_path, move_to_path)
        logging.info(log_msg)

        moved_files = move_files(move_from_path, move_to_path)

        log_msg = str("Moved a total of {0} file(s)").format(
            str(len(moved_files)))
        logging.info(log_msg)

        if len(moved_files) < 1:
            log_warning = str(
                "No files to upload since no file(s) were moved to {0}").format(move_to_path)
            logging.warning(log_warning)
            return

        # Archive container
        if conf["ARCHIVE_CONTAINER"]:
            archive_stamp = datetime.now().strftime(
                archive_container_timestamp_format)

            archive_container = str("{0}{1}{2}").format(
                archive_container_prefix, archive_stamp, archive_container_suffix)

            archive_container = archive_container.replace(" ", "")

            to_archive_path = os.path.join(
                archive_root_path, archive_container)
        else:
            to_archive_path = archive_root_path

        log_msg = str("Archive file(s) from archive temp root path {0} to archive root path {1}").format(
            move_to_path, to_archive_path)
        logging.info(log_msg)

        # Move files from temp root folder path to archive
        archived_files = move_files(
            move_to_path, to_archive_path)

        log_msg = str("Archived a total of {0} file(s)").format(
            str(len(archived_files)))
        logging.info(log_msg)

        # Clean up the archive
        if not conf["CLEAN_UP_ARCHIVE"]:
            log_msg = str(
                "Clean up archive is turned off in .yml config file. Exiting.")
            logging.info(log_msg)
            return

        archive_retention_time = conf["ARCHIVE_RETENTION_TIME_HOURS"]

        log_msg = str("Clean up archives in archive root path {0}").format(
            archive_root_path)
        logging.info(log_msg)

        if conf["ARCHIVE_CONTAINER"]:
            cleaup_up_result = remove_archive(archive_retention_time, archive_root_path, archive_container_prefix,
                                              archive_container_suffix, archive_container_timestamp_format, True)
        else:
            cleaup_up_result = remove_archive(archive_retention_time, archive_root_path, archive_file_prefix,
                                              archive_file_suffix, archive_file_timestamp_format, False)

        log_msg = str("Clean up archive result {0}").format(cleaup_up_result)
        logging.info(log_msg)

    # Main error handler
    except Exception as err_main:
        logging.error('Main exception: %s', str(err_main))
        raise


if __name__ == '__main__':
    main()
