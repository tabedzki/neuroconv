import os
import boto3

from neuroconv import ConverterPipe
from neuroconv.datainterfaces import SpikeGLXRecordingInterface

folder_path = os.environ["FOLDER_PATH"]
ap_file_name = os.environ["AP_FILE_NAME"]
lf_file_name = os.environ["LF_FILE_NAME"]

s3_resource = boto3.resource(
    "s3", "us-east-2", aws_access_key_id=os.environ["ACCESS_KEY"], aws_secret_access_key=os.environ["SECRET_KEY"]
)
bucket = s3_resource.Bucket(os.environ["BUCKET_NAME"])
for obj in bucket.objects.filter(Prefix=folder_path):
    if not os.path.exists(os.path.dirname(obj.key)):
        os.makedirs(os.path.dirname(obj.key))
    bucket.download_file(obj.key, obj.key)  # save to same path

ap_band = SpikeGLXRecordingInterface(file_path=f"./{folder_path}/{ap_file_name}")
lf_band = SpikeGLXRecordingInterface(file_path=f"./{folder_path}/{lf_file_name}")

converter = ConverterPipe(data_interfaces=[ap_band, lf_band])
converter.run_conversion()
