# Project dependency installation
- 1.python dependency installation
  ubuntu: apt-get install python3-fastapi python3-loguru
- 2.shell install 
  ubuntu: apt-get install rclone
# ubuntu Server environment deployment requirements
- 1.install java runtime，openjdk-17-jdk<br>
    apt-get install -y openjdk-17-jdk
- 2.install nodejs version: v22.2.0 or above :https://nodejs.org/en/download/package-manager
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash<br>
    export NVM_DIR="$HOME/.nvm"<br>
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"<br>
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"<br>
    nvm install 22
- 3.download android studio：
    #wget https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2024.1.2.13/android-studio-2024.1.2.13-linux.tar.gz<br>
    #tar -zxvf android-studio-2024.1.2.13-linux.tar.gz<br>
    wget https://googledownloads.cn/android/repository/commandlinetools-linux-11076708_latest.zip<br>
    jar xvf commandlinetools-linux-11076708_latest.zip
- 4.Create a new directory structure according to document requirements
    mkdir -p PWD/android/sdk/cmdline-tools/latest<br>
    cp -r cmdline-tools/* android/sdk/cmdline-tools/latest/
- 5.install android platform
    sh android/sdk/cmdline-tools/latest/bin/sdkmanager "build-tools;31.0.0" "build-tools;32.0.0" "build-tools;33.0.0" "build-tools;34.0.0" "build-tools;35.0.0" "cmake;3.22.1" "ndk;23.2.8568313" "platform-tools" "emulator" "platforms;android-34" "sources;android-34" "platforms;android-30" "sources;android-30" "platforms;android-31" "sources;android-31" "platforms;android-33" "sources;android-33" 
- 6.android tools add to env
    echo "export ANDROID_HOME=/home/ecs-user/android/sdk/" >> /etc/profile<br>
    echo "export PATH=$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$PATH" >> /etc/profile<br>
    source /etc/profile
- 7.apktool tools installation
    download install script
    wget -O apktool https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool<br>
    wget -O apktool.jar https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.10.0.jar<br>
    Set executable permissions<br>
    chmod +x apktool apktool.jar<br>
    move /usr/local/bin/ directory<br>
    mv apktool /usr/local/bin/<br>
    mv apktool.jar /usr/local/bin/<br>
    check apktool version，check the installation result<br>
    apktool -version
- 8.set enviroment
    echo 'APKSIGNER="/home/ecs-user/android/sdk/build-tools/33.0.1/apksigner"' > .env
    echo 'APKSIGNER="/Users/lukelei/Library/Android/sdk/build-tools/33.0.1/apksigner"' > .env
- 10.npm install
    npm install
