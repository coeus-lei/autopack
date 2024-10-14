from common.config_loader import config
from common.logger import logger
import requests

'''
    参数说明
    nativeAppId:马甲包ID
    progress: 枚举值: Packaged, PackagingFailed 。对应打包成功，打包失败
    downloadUrl: APK下载地址(打包成功的时候填)
    errorMsg: 打包失败的错误信息
'''
def report_status(nativeAppId, progress, report_url, header_info, download_url=None, error_msg=None):
    #检查progress的枚举值，根据情况检查downloadUrl和errorMsg
    if progress == "Packaged":
        if not download_url:
            logger.error("When progress is 'Packaged', downloadUrl must be provided.")
            raise ValueError("When progress is 'Packaged', downloadUrl must be provided.")
        payload = {
            'nativeAppId': nativeAppId,
            'progress': "Packaged",
            'downloadUrl': download_url,
            'errorMsg': ""
        }
    elif progress == "PackagingFailed":
        if not error_msg:
            logger.error("When progress is 'PackagingFailed', errorMsg must be provided.")
            raise ValueError("When progress is 'PackagingFailed', errorMsg must be provided.")
        payload = {
            'nativeAppId': nativeAppId,
            'progress': "PackagingFailed",
            'downloadUrl': "",
            "errorMsg": error_msg
        }
    else:
        logger.error("Invalid progress value. Allowed values are 'Packaged' or 'PackagingFailed'.")
        raise ValueError("Invalid progress value. Allowed values are 'Packaged' or 'PackagingFailed'.")
    

    try:
        response = requests.post(report_url, json=payload, headers=header_info)

        if response.status_code == 200:
            logger.info(f"nativeAppId: {nativeAppId}, Status reported successfully, {response.json()}")
        else:
            logger.error(f"nativeAppId: {nativeAppId}, Failed to report status. HTTP Status code: {response.status_code}", response.text)

    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while reporting status: {e}")
