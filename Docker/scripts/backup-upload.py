import ibm_boto3
import os
import sys
from ibm_botocore.client import Config, ClientError
# Constants for IBM COS values
COS_ENDPOINT = os.environ['ENDPOINT' ]
COS_API_KEY_ID = os.environ['API_KEY']
COS_AUTH_ENDPOINT = os.environ['AUTH_ENDPOINT']
COS_RESOURCE_CRN = os.environ['RESOURCE_CRN']
# Create resource
cos = ibm_boto3.resource("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_RESOURCE_CRN,
        ibm_auth_endpoint=COS_AUTH_ENDPOINT,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
)
print ("Connection Established")
def get_buckets():
        global status
        print("Retrieving list of buckets")
        bucket_exist = 0
        try:
                buckets = cos.buckets.all()
                for bucket in buckets:
                        print("Bucket Name: {0}".format(bucket.name))
                        if os.environ['BUCKET_NAME'] == str(bucket.name):
                                bucket_exist = 1
        except ClientError as be:
                print("CLIENT ERROR: {0}\n".format(be))               
                sys.exit(1)
        except Exception as e:
                print("Unable to retrieve list buckets: {0}".format(e))
                sys.exit(1)
        if bucket_exist != 1:
                print("Bucket with name '" + os.environ['BUCKET_NAME'] + "' not found in list. Exiting.....")
                sys.exit(1)
get_buckets();
def upload_large_file(bucket_name, item_name, file_path):
        error_occured = 0
        print("Starting large file upload for {0} to bucket: {1}".format(item_name, bucket_name))
        # set the chunk size to 5 MB
        part_size = 1024 * 1024 * 5
        # set threadhold to 5 MB
        file_threshold = 1024 * 1024 * 5
        # Create client connection
        cos_cli = ibm_boto3.client("s3",
                ibm_api_key_id=COS_API_KEY_ID,
                ibm_service_instance_id=COS_RESOURCE_CRN,
                ibm_auth_endpoint=COS_AUTH_ENDPOINT,
                config=Config(signature_version="oauth"),
                endpoint_url=COS_ENDPOINT
        )
        # set the transfer threshold and chunk size in config settings
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
                multipart_threshold=file_threshold,
                multipart_chunksize=part_size
        )
        # create transfer manager
        transfer_mgr = ibm_boto3.s3.transfer.TransferManager(cos_cli, config=transfer_config)
        try:
                # initiate file upload
                future = transfer_mgr.upload(file_path, bucket_name, item_name)
                # wait for upload to complete
                future.result()
                print ("Large file upload complete!")
                os.remove(file_path)
        except Exception as e:
                print("Unable to complete large file upload: {0}".format(e))
                error_occured = error_occured + 1
        finally:
                transfer_mgr.shutdown()
                if error_occured != 0 :
                        print("Exiting from Container")
                        sys.exit(1)
upload_large_file(os.environ['BUCKET_NAME'],os.environ['BACKUP_FILE_NAME'], os.environ['BACKUP_DIR_PATH'] + os.environ['BACKUP_FILE_NAME']);
