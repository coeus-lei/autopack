#!/usr/bin/env bash
#定义工作目录
WORKDIR=/home/ecs-user
#判定工作目录是否存在
if [ ! -d $WORKDIR ]; then
    mkdir -p $WORKDIR
fi
#1.判定是否为ubuntu系统
# system=`lsb_release -a 2>/dev/null | grep "istributor ID:" | cut -d ":" -f2`
system=`lsb_release -a 2>/dev/null | grep "istributor ID:" | cut -d ":" -f2`
if [ "$(echo ${system})" != "Ubuntu" ]; then
    echo "This script is only for Ubuntu system."
    exit 1
fi
#2.安装java运行时openjdk-17-jdk,安装命令curl,wget,git,python依赖python3-fastapi,python3-loguru
apt-get update >/dev/null 2>&1
apt-get install -y curl wget git python3-fastapi python3-loguru >/dev/null 2>&1
if command -v java >/dev/null 2>&1; then
    echo "Java has been installed."
    exit 0
else
    apt-get install -y openjdk-17-jdk >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Java has been installed."
        java -version
    else
        echo "Failed to install Java."
        exit 1
    fi
fi
#3.安装nodejs 版本v22.2.0或以上版本
if command -v node >/dev/null 2>&1; then
    echo "Node.js has been installed."
    exit 0
else
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash >/dev/null 2>&1
    export NVM_DIR="$HOME/.nvm" 
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
    nvm install 22 >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Node.js has been installed."
        node -v
    else
        echo "Failed to install Node.js."
        exit 1
    fi
fi
#4.下载android studio
cd $WORKDIR
if [ -f commandlinetools-linux-11076708_latest.zip ]; then
    echo "commandlinetools-linux has been downloaded."
else
    wget https://googledownloads.cn/android/repository/commandlinetools-linux-11076708_latest.zip  >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "commandlinetools-linux has been downloaded."
    else
        echo "Failed to download commandlinetools-linux."
        exit 1
    fi
fi
jar xvf commandlinetools-linux-11076708_latest.zip >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "commandlinetools-linux has been extracted."
else
    echo "Failed to extract commandlinetools-linux."
    exit 1
fi
#5.按commandlinetools文档要求新建目录结构拷贝压缩包内文件
if [ -d ${WORKDIR}/android/sdk/cmdline-tools/latest ]; then
    echo "Android SDK has been installed."
else
    mkdir -p ${WORKDIR}/android/sdk/cmdline-tools/latest && cp -r ${WORKDIR}/cmdline-tools/* ${WORKDIR}/android/sdk/cmdline-tools/latest/ >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Android SDK has been installed."
    else
        echo "Failed to install Android SDK."
        exit 1
    fi
fi
#6.安装android platform tools
yes | sh android/sdk/cmdline-tools/latest/bin/sdkmanager "build-tools;31.0.0" "build-tools;32.0.0" "build-tools;33.0.0" "build-tools;34.0.0" "build-tools;35.0.0" "cmake;3.22.1" "ndk;23.2.8568313" "platform-tools" "emulator" "platforms;android-34" "sources;android-34" "platforms;android-30" "sources;android-30" "platforms;android-31" "sources;android-31" "platforms;android-33" "sources;android-33" >/dev/null 2>&1
#7.将android 工具添加到环境变量
echo "export ANDROID_HOME=${WORKDIR}/android/sdk" >> ~/.bashrc
echo "export PATH=\$PATH:\$ANDROID_HOME/cmdline-tools/latest/bin" >> ~/.bashrc
echo "export PATH=\$PATH:\$ANDROID_HOME/platform-tools" >> ~/.bashrc
source ~/.bashrc
#8.apktool工具安装
if command -v apktool >/dev/null 2>&1; then
    echo "Apktool has been installed."
    exit 0
fi
wget -O apktool https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Apktool has been downloaded."
else
    echo "Failed to download Apktool."
    exit 1
fi
wget -O apktool.jar https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.10.0.jar >/dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Apktool.jar has been downloaded."
else
    echo "Failed to download Apktool.jar."
    exit 1
fi
chmod +x apktool apktool.jar
mv apktool apktool.jar /usr/local/bin/
apktool -version
#9.git clone buildH5Package代码库,需要输入github仓库的用户名和密码
cd $WORKDIR
git clone https://github.com/888panda/buildH5Package.git
cd buildH5Package/buildScript/
echo 'APKSIGNER="/home/ecs-user/android/sdk/build-tools/33.0.1/apksigner"' > .env
npm install
