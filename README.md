# scp-s3-downloader

## **Description**

---

The Python script uses the [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library to download files from a given key of an AWS S3 bucket.\
To be able to authenticate against AWS a secrets.yml file is required.\
Even though a good rule of thumb is to never store any sensitive information in paths.. Just to be sure.. file paths are also set in the secrets.yml file.\
Logging is configured in the config.yml as well as opt-in-out settings to suit different needs.\
<br/>



## **Utilization**

---

*Clone the [scp-s3-downloader](https://github.com/sporveien/scp-s3-downloader) Github repository to your local systems current location.*

#### Git CLI
```git
git clone https://github.com/sporveien/scp-s3-downloader.git
```

#### API Call - Linux/MacOS
```bash
curl -JLO  https://api.github.com/repos/sporveien/scp-s3-downloader/zipball
unzip sporveien-scp-s3-uploader-%shaxxx%.zip
```

#### API Call - Windows
```powershell
$Response = Invoke-WebRequest -Uri https://api.github.com/repos/sporveien/scp-s3-uploader/zipball;
$Filename = $Response.headers['content-disposition'].Split('=')[1];
Set-Content -LiteralPath ".\$Filename" -Encoding byte -Value $Response.Content; 
```

### **Requirements**


From local repository root, install packages from *requirements.txt* file

```
pip install -r requirements.txt
```


### **Script variables**

Before running the Python script, create a *secrets.yml* in the root directory of the local repository and assign the following variables.


- *AWS_ACCESS_KEY*
    - AWS Access Key ID, with access to the S3 bucket.
- *AWS_SECRET_KEY*
    - AWS Access Secret, with access to the S3 bucket. 
- *S3_BUCKET*
    - The S3 bucket name
- *S3_KEY_PREFIX*
    - The S3 bucket key, set to "*" to download everything from the bucket (**should be used carefully**).
- *LOG_ROOT*
    - The root path of script logging
- *DATA_ROOT*
    - The root path of script data
- *TEMP_ROOT*
    - The root path of script logging
- *ARCHIVE_ROOT*
    - The root path of script data

```yml
# secrets.yml file example

AWS_ACCESS_KEY: XXXXXXYourAccessKeyIdXXXXXXXXXXXX
AWS_SECRET_KEY: XXXXXXYourSecretAccessKeyXXXXXXXX
S3_BUCKET: s3-bucket-name
S3_KEY_PREFIX: s3-key
LOG_ROOT: c:\example\path\log
DATA_ROOT: c:\example\path\data
TEMP_ROOT: c:\example\path\temp
ARCHIVE_ROOT: c:\example\path\archive
```

(Optional) Change the *secrets.yml* in the root directory of the local repository to use needs.

```yml
TAKE_NO_ACTION: false
# Amount of log files to store before removing the oldest one
MAX_LOGFILES: 10
# Turn archive management on or/off. This would also turn off the archive clean up.
ARCHIVE_FILES: True
# Turn cleaning up archive on/off.
CLEAN_UP_ARCHIVE: True
# Archive file prefix
ARCHIVE_FILE_PREFIX: "pre_"
# Archive file suffix
ARCHIVE_FILE_SUFFIX: "_suf"
# Archive file time stamp format
ARCHIVE_FILE_TIMESTAMP_FORMAT: "%Y.%d.%m-%H.%M.%S.%f"
# Use archive container
ARCHIVE_CONTAINER: True
# Archive container dir time stamp format
ARCHIVE_CONTAINER_TIMESTAMP_FORMAT: "%Y.%d.%m-%H.%M.%S.%f"
# Archive container dir prefix
ARCHIVE_CONTAINER_PREFIX: "pre_"
# Archive container dir suffix
ARCHIVE_CONTAINER_SUFFIX: "_suf"
# Amount of hours to store transfered files in archive.
ARCHIVE_RETENTION_TIME_HOURS: 1
# Log file extension
LOG_FILE_EXTENTSION: ".log"
# Log file timestamp format
LOG_DATE_TIME_FORMAT: "%d%m%Y_%H%M%S"
# Boto3 log level
BOTO3_LOG_LEVEL: "boto3.resources"
# S3 download container timestamp format
BOTO3_DATE_TIME_FORMAT: "%d%m%Y_%H%M%S" #'%Y.%d.%m-%H.%M.%S.%f'
# Set to 'true' to keep directory structure inside the download container
BOTO3_KEEP_DIRECTORY_STRUCTURE: false
# Set to 'true' to put downloaded S3 objectes in a timestamp named container (directory). Experimental, only works without archiving.  
BOTO3_USE_TIMESTAMP_CONTAINER: false
# Set to 'true' to only download files created after the last archive was created. Only works with archiving.
BOTO3_ONLY_DOWNLOAD_LATEST: true
```



### **Trigger**

#### **Initialization**

Initialize the *main.py* file to start the script.

```bash
python3 the/path/to/scp-s3-downloader/main.py
```

#### **Testing/Development**

#### Linux/MacOS

Run the *test.sh* script to setup download environment **(required paths in the *secrets,yml* is created within the local repository)** and run a quick test in your in local repository.

```bash
chmod +x test.sh && ./test.sh
```

#### Windows

Run the *test.ps1* script to setup a test environment and run a quick test in your in local repository.

```powershell
.\test.ps1
```


