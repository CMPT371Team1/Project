#!/bin.sh

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
  # encrypting and decrypting keys goes here
  mkdir www
  java -version
else
  wget http://dl.google.com/android/android-sdk_r24.3.4-linux.tgz
  echo $JAVA_HOME
  tar -xvf android-sdk_r24.3.4-linux.tgz
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter platform-tools
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter build-tools-23.0.3
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter android-24
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-support
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-m2repository
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-google-m2repository
  export ANDROID_HOME=$PWD/android-sdk-linux
  mkdir www
  java -version
  ls /usr/lib/jvm/
  export PATH=${PATH}:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$ANDROID_HOME/build-tools/23.0.2