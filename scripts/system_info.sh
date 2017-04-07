# Author: Chris Mykota-Reid
# CMPT 371
# Prints, to the build log, the packages and tool versions for the main
# components of our system.

echo "System info:"
echo $TRAVIS_OS_NAME
if [[ "${TRAVIS_OS_NAME}" == "android" ]]; then
  echo 'SDK Platform Android 7.1.1, API 25, revision 3'
  echo 'Android SDK Tools, revision 25.2.5'
  echo 'Android SDK Build-tools, revision 25.0.1'
  echo 'Android SDK Platform-tools, revision 25.0.3'
  echo 'Google Repository, revision 42'
  echo 'Android Support Repository, revision 42'
fi
  
if [[ "${BUILD_TYPE}" == "test" || ( "${BUILD_TYPE}" == "deployment" && "${TRAVIS_OS_NAME}" == "android" ) ]]; then  
  java -version
  echo 'npm version:'
  npm -v
  firefox --version
  #google-chrome --version
  echo "Protractor version:"
  protractor --version
  echo "Jasmine version:"
  npm view jasmine version
  echo "Gulp version:"
  npm view gulp version
  ionic info
  ssh -V
  sshpass -V
fi
