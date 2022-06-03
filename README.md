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

### **Dependencies**


From local repository root, install packages from *requirements.txt* file

```
pip install -r requirements.txt
```


### **Script variables**

Before running the Python script, create a *secrets.yml* in the root directory of the local repository and assign the followin .


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



### **Test**

#### Linux/MacOS

Run the *test.sh* script to setup a test environment and run a quick test in your in local repository.

```bash
chmod +x test.sh && ./test.sh
```

#### Windows

Run the *test.ps1* script to setup a test environment and run a quick test in your in local repository.

```powershell
./test.ps1
```


