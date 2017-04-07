#!/bin/bash

# Authress: Chris Mykota-Reid 
# Does things not related to installing files but still needed to be setup 
# before running the build.   


if [[ ${TRAVIS_OS_NAME} == "osx" ]]; then
  # TODO: KEYS FOR ENCRYPTION FOR IOS DEPLOYMENT
  echo "should be osx"
elif [[ "${TRAVIS_OS_NAME}" == "linux" ]]; then
  if [[ "${BUILD_TYPE}" != "deployment" ]]; then
    echo "got to linux before_script"
    gulp test
  fi
else
  echo "should be andriod"
fi
