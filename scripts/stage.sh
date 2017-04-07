#!/bin/bash

# Author: Chris Mykota-Reid 
# Gets ran after the smoke tests pass.  
# Sends the sources code to a branch for more rigorous testing.
# Is a modification of the deploy script.

set -ev

# Un-encrypts the ssh key, starts up and adds it to the list of keys for the Travis machine
setup_ssh(){
  openssl aes-256-cbc -K $encrypted_fed185e319aa_key -iv $encrypted_fed185e319aa_iv -in keys/github_deploy_key.enc -out github_deploy_key -d
  chmod 600 github_deploy_key
  eval "$(ssh-agent -s)"
  ssh-add github_deploy_key
}

# Sets email and username to the person who the ssh key is linked to. 
# Changes the url to the ssh one (initially repo is cloned using https),
# then checks out the branch that more rigorous testing takes place on
setup_git(){
  git config --global user.email "clm972@mail.usask.ca"
  git config --global user.name "ChrisMykotaReid"
  git remote set-url origin git@github.com:CMPT371Team1/Project.git
  git branch "${TESTING_BRANCH}"
  git checkout "${TESTING_BRANCH}"
  git pull --no-commit origin "${TESTING_BRANCH}"
  git commit -m "smoke tests passed, merging into testing ready branch [ci skip]"
  git push
}


# Merges the successfully smoke tested code into the testing branch.
merge(){
  git merge "${TRAVIS_BRANCH}"
  git commit -m "smoke tests passed, merging into testing ready branch [ci skip]"
  git push
}

if [[ "${BUILD_TYPE}" == "test" ]]; then 
  setup_ssh
  setup_git
  merge
fi
