# scp-s3-downloader

## General description

The Python script uses the [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library to download files from a given key of an AWS S3 bucket.\
To be able to authenticate against AWS a secrets.yml file is required.\
Even though a good rule of thumb is to never store any sensitive information in paths.. Just to be sure.. file paths are set in the secrets.yml file.\
Logging is configured in the config.yml as well as opt-in-out settings to suit different needs.\
<br/>

---

## Install packages from requirements.txt file

```
pip install -r requirements.txt
```

---

## Running local test and debugging

- Update secrets.yml file
  - log directory --> LOG_ROOT
  - temp directory --> TEMP_ROOT
  - archive directory --> ARCHIVE_ROOT
  - data directory --> DATA_ROOT

```
# secrets.yml file example
LOG_ROOT: test/_log
DATA_ROOT: test/data
TEMP_ROOT: test/temp
ARCHIVE_ROOT: test/archive
```

- Create directories
  - log directory
  - temp directory
  - archive directory
  - data directory

```
# Run test.sh test.sh to setup test environment and run a quick test with some dummy data.

chmod +x test.sh && ./test.sh;

```