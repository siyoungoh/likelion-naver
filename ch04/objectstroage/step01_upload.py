# object storage 문서
# https://guide.ncloud-docs.com/docs/storage-storage-6-1#
# https://api.ncloud-docs.com/docs/storage-objectstorage-putobjectacl
import boto3
from pathlib import Path

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'

access_key = '내 계정 access_key'
secret_key = '내 계정 secret_key'

s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=access_key,
                  aws_secret_access_key=secret_key)

bucket_name = '내 버킷 이름'

# 내 컴퓨터에 있는 파일 정보
local_folder = "mp3_folder"
local_file = "news.mp3"
dir_parts = [local_folder, local_file]
local_path = str(Path.cwd().joinpath(*dir_parts))
# print(type(local_path), local_path)

# object storage 에 업로드할 파일 정보
upload_folder = 'news'
upload_file = '12345.mp3'
upload_path = f'{upload_folder}/{upload_file}'

s3.upload_file(local_path, bucket_name, upload_path,
               ExtraArgs={'ACL': 'public-read'})
