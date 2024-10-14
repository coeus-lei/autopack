import configparser
import os

def load_config():
    config = configparser.ConfigParser()
    #获取当前目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    #获取上层目录
    parent_directory = os.path.dirname(current_directory)
    config_file = os.path.join(parent_directory, 'config.ini')
    config.read(config_file)
    if not config.sections():
        raise FileNotFoundError(f"无法加载配置文件: {config_file}")
    
    # reporturl = config.get('settings','reporturl')
    # print(reporturl)
    return config

config = load_config()
