'''
Simple Python script (version 3.8)
Functionality:

    check if S3 bucket exist
    upload file on s3
    download file from s3
    check if file exists on s3
'''
import os

import boto3
from botocore.exceptions import ClientError


client = boto3.client("s3")

'''response = client.create_bucket(
    ACL='private',
    Bucket='testbucketwithcli11',
    CreateBucketConfiguration={
        'LocationConstraint': 'eu-north-1'
    }
)'''


def is_bucket_exist(bucket_name="testbucketwithcli11"):
    try:
        response = client.head_bucket(
                    Bucket=bucket_name,
                    )
        return "bucket exist"
    except ClientError as ex:
        return "bucket doesn't exist"


def upload_file(file, bucket, s3Key):
    response = client.put_object(
        Body =  file,
        Bucket = bucket, 
        Key = s3Key
        )
    return "successfully uploaded"


def download_from_S3(bucket, s3Key, filename):
    
    response = client.download_file(
        Bucket = bucket,
        Key = s3Key,
        Filename = filename
        )
    return f"successfulle uploaded. pls check it {filename}"


def is_file_exist(s3Key, bucket_name="testbucketwithcli11"):
    try:
        response = client.get_object(
                    Bucket=bucket_name,
                    Key=s3Key
                    )
        return "file exist"
    except ClientError as ex:
        return "file doesn't exist"
    

if __name__ == "__main__":
    #print( download_from_S3('testbucketwithcli11', "угар.jpg", os.path.join(os.path.curdir, "S3угар.jpg")) )
    print(is_file_exist("угар.jpg"))