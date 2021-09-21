# object storage 문서
# https://guide.ncloud-docs.com/docs/storage-storage-6-1#
# https://api.ncloud-docs.com/docs/storage-objectstorage-putobjectacl
import boto3
from pathlib import Path

# 함수 설계 upload_storage
# 기능 : object storage 에 파일 업로드 (ACL:public-read 로 설정)
# input(param) : access_key, secret_key, bucket_name, local_folder, local_file, upload_folder, upload_file
# output(return) : 없음

access_key = '내 계정 access_key'
secret_key = '내 계정 secret_key'

bucket_name = '내 버킷 이름'

# 내 컴퓨터에 있는 파일 정보
local_folder = 'mp3_folder'
local_file = 'news.mp3'

upload_folder = 'news'
upload_file = '1234.mp3'


def upload_storage(access_key, secret_key, bucket_name, local_folder, local_file, upload_folder, upload_file):
    """
    object storage 에 파일 업로드 (ACL:public-read 로 설정)
    :param: str access_key
    :param: str secret_key
    :param: str bucket_name
    :param: str local_folder
    :param: str local_file
    :param: str upload_folder
    :param: str upload_file
    """
    service_name = 's3'
    endpoint_url = 'https://kr.object.ncloudstorage.com'
    region_name = 'kr-standard'

    s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)

    dir_parts = [local_folder, local_file]
    local_path = str(Path.cwd().joinpath(*dir_parts))
    # print(type(local_path), local_path)

    # object storage 에 업로드할 파일 정보
    upload_path = f'{upload_folder}/{upload_file}'

    s3.upload_file(local_path, bucket_name, upload_path,
                   ExtraArgs={'ACL': 'public-read'})


# param : dict api_info
# param : dict local_info
# param : dict bucket_info

api_info = {'access_key': '내 계정 access_key',
            'secret_key': '내 계정 secret_key'}
local_info = {'local_folder': 'mp3_folder', 'local_file': 'news.mp3'}
bucket_info = {'bucket_name': '내 버킷 이름',
               'upload_folder': 'news', 'upload_file': '123.mp3'}


def upload_storage2(api_info, local_info, bucket_info):
    """
    object storage 에 파일 업로드 (ACL:public-read 로 설정)
    :param: dict api_info / key: access_key, secret_key
    :param: dict local_info / key: local_folder, local_file
    :param: dict bucket_info / key: bucket_name, upload_folder, upload_file
    """
    service_name = 's3'
    endpoint_url = 'https://kr.object.ncloudstorage.com'
    region_name = 'kr-standard'

    s3 = boto3.client(service_name, endpoint_url=endpoint_url, aws_access_key_id=api_info['access_key'],
                      aws_secret_access_key=api_info['secret_key'])

    dir_parts = [local_info['local_folder'], local_info['local_file']]
    local_path = str(Path.cwd().joinpath(*dir_parts))
    # print(type(local_path), local_path)

    # object storage 에 업로드할 파일 정보
    upload_path = f'{bucket_info["upload_folder"]}/{bucket_info["upload_file"]}'

    s3.upload_file(local_path, bucket_info['bucket_name'], upload_path,
                   ExtraArgs={'ACL': 'public-read'})


# ======TEST========
# upload_storage(access_key, secret_key, bucket_name, local_folder,
#                local_file, upload_folder, upload_file)

# ======TEST02========
upload_storage2(api_info, local_info, bucket_info)
