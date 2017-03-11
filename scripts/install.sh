#!/bin/bash
set -v

# Author: Chris Mykota-Reid ~.u 
# Installs all the packages required for whatever build is being done.
# Travis is a bad influence on Ionic and got it drunk
# and now needs it's hand held through the build.  That's what 'mkdir www' is for.


# Downloads and installs all the files required to run ios.
# You can find the versions inside the doc or posted at the end 
# of the build log
ios_install(){
  brew update
  brew cask install java
  npm install -g grunt-cli cordova ionic
  npm install
  ionic state restore
}

# Downloads and installs all the common files required to run android/linux.
# You can find the versions inside the doc or posted at the end 
# of the build log.
lindroid_install(){
  sudo apt-get install oracle-java8-set-default screen xvfb
  npm install -g protractor@5.0.0 cordova ionic jasmine jasmine-core
  # installs packages specified in the ionic json
  npm install
  webdriver-manager update
  sudo apt-get install sshpass
  # commented out for now, we could use chrome at some point and this might be needed for it
  # chrome_install
}

# Downloads and installs all the files required to run android.
# You can find the versions inside the doc or posted at the end 
# of the build log.
android_install(){
  ionic state restore
  wget http://dl.google.com/android/android-sdk_r24.4-linux.tgz
  tar -xf android-sdk_r24.4-linux.tgz
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter tools-25.2.5
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter platform-tools
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter tools
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter build-tools-25.0.1
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter android-25 
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-support 
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-android-m2repository 
  echo y | ./android-sdk-linux/tools/android update sdk --no-ui --all --filter extra-google-m2repository
}

# Downloads and installs google app engine for our server build.
gae_install(){
  gcloud -v
  sudo gcloud components update
  echo "" | sudo gcloud components install app-engine-python
  echo "" | sudo gcloud components install app-engine-python-extras
  sudo pip install PyYAML
  sudo pip install webapp2
  sudo pip install WebOb
  sudo pip install django
}

if [[ "${TRAVIS_OS_NAME}" == "osx" ]]; then
  echo "got to install osx"
  ios_install
elif [[ "${TRAVIS_OS_NAME}" == "linux" ]]; then
  echo "got to linux install"
  lindroid_install
  sudo apt-get install sshpass
  
  # prevent dialogue messages from appearing in gooogle app engine install
  export CLOUDSDK_INSTALL_DIR=/$HOME
  export CLOUDSDK_CORE_DISABLE_PROMPTS=1
  
  gae_install
  sudo du / | grep "gae"
  #echo "${PYTHONPATH}"
else
  echo "got to install: android"
  lindroid_install
  android_install
fi
mkdir www
