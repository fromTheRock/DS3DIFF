import os

#In PowerShell use the following command to set Environment Variable compatible with os.environ
#$env:AWS_ENDPOINT = "s3"
if __name__ == "__main__":
    print(os.environ);
    for key in os.environ:
        if key.startswith('S3_'):            
            print(f'var:{key}, value: {os.environ[key]}')
