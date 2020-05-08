import boto
import boto.s3.connection
import os
import sys

# Get full command-line arguments
full_cmd_arguments = sys.argv

# # Keep all but the first
argument_list = full_cmd_arguments[1:]

print (argument_list)


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
for bucket in conn.get_all_buckets():
    print(bucket.name)

bucket = conn.get_bucket('Automated-Report')


for i, val in enumerate(argument_list): 
    val = val 
    print(val)
    key_name = val 
    path = 'OpenShift/'
    print(key_name)
    full_key_name = os.path.join(path, key_name)
    k = bucket.new_key(full_key_name)
    k.set_contents_from_filename(key_name)


print("Successfully uploaded onto the Openstack Object Store")


