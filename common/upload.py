import requests,mimetypes
from pathlib import Path
# from common.baseLog import logger
from common.logger import logger
def upload_file(upload_url,apk_files_path):
    # 修改这里：打开文件并读取内容
    out_package = Path(apk_files_path)
    with open(out_package, 'rb') as f:
        file_content = f.read()

    # 修改这里：获取文件的 MIME 类型
    type = mimetypes.guess_type(out_package)
    files = {'file': (out_package.name, file_content, type)}
    data = {'type': type, 'name': out_package.name}

    try:
        response = requests.put(upload_url, files=files, data=data)
        response.raise_for_status()

        if response.json() and 'urls' in response.json() and response.json()['urls']:
            logger.info('上传成功')
            return response.json()['urls'][0]
        else:
            logger.error('上传响应格式不正确')
            raise ValueError('上传响应格式不正确')
    except Exception as error:
        logger.info('上传失败', error)
        raise
