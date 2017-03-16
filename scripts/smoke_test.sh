#!/bin/bash

# Author: Chris Mykota-Reid 
# A helper script to allow both smoke tests to run even if one fails
# while still having the build fail if either fails
echo $'\n\n\n\n*******RUNNING BACK-END SMOKE TESTS*******'
python -m unittest discover -s server-gae/ -p 'Test*.py'
export BACK_END_TEST=$?

curl -v -H "Content-Type: application/json" -X POST -d '{}' https://cmpt371g1.usask.ca:4040/initDBTESTERS

echo $'\n\n\n\n*******RUNNING FRONT-END SMOKE TESTS FOR FIREFOX*******'
screen -d -m -L ionic serve --firefox@47.0.1
sleep 50
xvfb-run protractor firefox-e2e-tests.conf.js
export FRONT_END_FF=$?

echo $'\n\n\n\n*******RUNNING FRONT-END SMOKE TESTS FOR CHROME*******'
xvfb-run protractor chrome-e2e-tests.conf.js
export FRONT_END_CHROME=$?

if [[ ${BACK_END_TEST} > 0 ]]; then
  echo ${BACK_END_TEST}
  exit 1
fi
if [[ ${FRONT_END_FF} > 0 ]]; then
  echo ${FRONT_END_FF}
  exit 2
fi
if [[ ${FRONT_END_CHROME} > 0 ]]; then
  exit 3
fi
