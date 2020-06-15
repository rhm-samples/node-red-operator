import ibm_boto3
import sys
import os
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

def get_buckets():
	global status
	print("Retrieving list of buckets")
	bucket_exist = 0
	try:
		buckets = cos.buckets.all()
		print(buckets)
		print(type(buckets))
		for bucket in buckets:
			print("Bucket Name: {0}".format(bucket.name))
			print(type(bucket))
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

# Create Client
cos = ibm_boto3.client("s3",
        ibm_api_key_id=COS_API_KEY_ID,
        ibm_service_instance_id=COS_RESOURCE_CRN,
        ibm_auth_endpoint=COS_AUTH_ENDPOINT,
        config=Config(signature_version="oauth"),
        endpoint_url=COS_ENDPOINT
)


def download_file_cos(bucket_name, object_name, download_file_path):
	try:
		res=cos.download_file(bucket_name, Key=object_name, Filename=download_file_path)
	except Exception as e:
		print("Restore failed")
		print(Exception, e)
		sys.exit(1)
		print("Restore exit")
	else:
		print('File Downloaded')

download_file_cos(os.environ['BUCKET_NAME'],os.environ['RESTORE_FILE_NAME'], os.environ['RESTORE_DIR_PATH'] + os.environ['RESTORE_FILE_NAME']);
