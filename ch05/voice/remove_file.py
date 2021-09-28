# -*- coding: utf-8 -*-
import os
from pathlib import Path


file_folder = 'mp3_folder'
file_name = 'test.mp3'


def remove_file(file_folder, file_name):
    """
    파일 삭제
    :param: file_folder: 파일 폴더
    :param: file_name: 파일 이름
    :result: 처리 결과 메시지
    """
    result = ''

    dir_parts = [file_folder, file_name]
    path = Path.cwd().joinpath(*dir_parts)
    # 파일이 존재하면 삭제
    try:
        if os.path.isfile(path):
            os.remove(path)
            result = f'{path} 파일이 삭제되었습니다.'
        else:
            result = f'Error: {path} 를 찾을 수 없습니다.'
    except OSError as e:
        result = f'Error: {e.filename} - {e.strerror}.'

    return result


# =====TEST======
result_msg = remove_file(file_folder, file_name)
print(result_msg)
