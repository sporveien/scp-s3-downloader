import logging
import os
import yaml
from boto import get_bucket, session
from logger import logger


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

        # Set environment variables from config file
        os.environ["AWS_ACCESS_KEY_ID"] = secrets['AWS_ACCESS_KEY']
        os.environ["AWS_SECRET_ACCESS_KEY"] = secrets['AWS_SECRET_KEY']

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
        bucket = get_bucket(botosession, secrets['S3_BUCKET'])
        bucket_name = bucket.name
        logging.debug(
            "Successfully got s3 bucket '%s'", bucket_name)

    # Main error handler
    except Exception as err_main:
        logging.error('Main exception: %s', str(err_main))
        raise


if __name__ == '__main__':
    main()
