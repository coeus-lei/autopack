import subprocess
import os

#获取当前Python文件所在目录
project_directory = os.path.dirname(os.path.abspath(__file__))
#指定rclone配置文件路径
config_path = os.path.join(project_directory, 'rclone.conf')
# local_path = os.path.join(project_directory, 'main.py')
local_path = "/Users/lukelei/project/package/buildH5Package/outPackage/android/"
remote_bucket_path = "cloudflare_r2:"
remote_bucketfiles_path = "cloudflare_r2:package-pre"
# print(f"Rclone config path: {config_path}")

#指定rclone配置同步文件执行同步或其他命令
def sync_files(source, destination):
    try:
        # 调用 rclone 命令，指定配置文件
        result = subprocess.run(
            ["rclone", "--config", config_path, "copy", source, destination],
            capture_output=True,
            text=True,
            check=True
        )
        # 打印命令的标准输出
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        # 打印错误信息
        print(f"Error: {e.stderr}")


def list_remote_bucket(remote_name):
    try:
        # 使用 rclone ls 命令列出远程存储桶列表
        result = subprocess.run(
            ["rclone", "--config",config_path, "lsd", remote_name],
            capture_output=True, 
            text=True, 
            check=True
        )
        print(result.stdout)  # 输出 rclone 命令的结果
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")

def list_remote_bucket_files(remote_name):
    try:
        # 使用 rclone ls 命令列出远程存储桶列表
        result = subprocess.run(
            ["rclone", "--config",config_path, "ls", remote_name],
            capture_output=True, 
            text=True, 
            check=True
        )
        print(result.stdout)  # 输出 rclone 命令的结果
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")

# list_remote_bucket(remote_bucket_path)
# list_remote_bucket_files(remote_bucketfiles_path)
# sync_files(local_path,remote_bucketfiles_path)
