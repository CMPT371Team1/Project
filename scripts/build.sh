#!/bin/bash

# Author: Chris Mykota-Reid :>
# This script calls the commands required to compile
# and emulate our program


set -ev

# Builds the ios app.  If we are deploying, it builds a release version, otherwise,
# builds and emulates the app for testing.  A deployment build should not be done
# on this platform.
ios_build(){
  if [[ "${BUILD_TYPE}" != "deployment" ]]; then
    ionic platform add ios
    ionic build ios
    #ionic emulate ios
  fi
}

# Builds the browser version of our app. This is currently the version of our app
# that has the e2e smoke tests done on it. A deployment build should not be done
# on this platform.
browser_build(){
  if [[ "${BUILD_TYPE}" != "deployment" ]]; then
    ./scripts/smoke_test.sh
    # sudo du / | grep "geckodriver"
  fi
}

# Builds the android version of our app. If it's a deployment build 
# does a release build and if not then builds and emulates the app for testing
# TODO: GET THE APP SIGNED W/ A KEY 
android_build(){
  ionic platform remove android
  ionic platform add android
  if [[ "${BUILD_TYPE}" == "deployment" ]]; then
    ionic build android 
  else
    ionic build android
    #xvfb-run /home/travis/build/CMPT371Team1/Project/android-sdk-linux/tools/android avd   
    #ionic emulate android
  fi
}


if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then
  echo 'got to build: osx'
  ios_build
elif [[ "${TRAVIS_OS_NAME}" == 'linux' ]]; then
  echo 'got to build: linux'
  export JAVA_HOME=/usr/lib/jvm/java-8-oracle
  browser_build
else
  echo 'got to build: android'
  export JAVA_HOME=/usr/lib/jvm/java-8-oracle
  android_build
fi
