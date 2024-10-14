import logging.config
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取上层目录
logging_config_path = os.path.join(base_dir, 'logging.conf')  # 拼接log配置文件路径
log_file_path = os.path.join(base_dir, 'app.log')

with open(logging_config_path, 'r') as f:
    config = f.read().replace('<LOG_PATH>', log_file_path)

temp_config_path = os.path.join(base_dir, 'temp_logging.conf')
with open(temp_config_path, 'w') as f:
    f.write(config)

logging.config.fileConfig(temp_config_path)
logger = logging.getLogger('')
# logger.info('log init success')
