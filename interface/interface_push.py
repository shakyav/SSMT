import boto
import boto.s3.connection
import os
import sys

#Get full command-line arguments and configure aws access key
full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
access_key = os.environ.get('access_key')
secret_key = os.environ.get('secret_key')
endpoint = os.environ.get('endpoint')

conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = endpoint,
        #is_secure=False,               # uncomment if you are not using ssl
        calling_format = boto.s3.connection.OrdinaryCallingFormat(),
        )

bucket = conn.get_bucket('Automated-Report')
print(bucket)

for i, val in enumerate(argument_list): 
    val = val 
    print(val)
    key_name = val 
    path = 'OpenShift/'
    print(key_name)
    full_key_name = os.path.join(path, key_name)
    k = bucket.new_key(full_key_name)
    k.set_contents_from_filename(key_name)

