#!/bin/bash

################################################
# Add a key so we can login to travisci vm
- cat ssh/travisci.pub >> ~/.ssh/authorized_keys
- chmod 600 ssh/travisci
  
# Install netcat
- brew --cache
- brew update
- brew install netcat
  
# Enable remote SSH
# Forward ssh to a non privileged port (to avoid sharing of non privileged
# ports)
- netcat -L localhost:22 -p 2222 &
- sleep 5
# Check for open ports
- netstat -an|grep -i listen
# Create reverse SSH tunner
- ssh -fn -v -N -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i
  ssh/travisci -R 2222:localhost:2222
ubuntu@@someremotehostonaws.eu-west-1.compute.amazonaws.com
# Note: the connection only works once as netcat will exit after first
# connection
# Travisci seems to cut outgoing connections after a few minutes
# login user = ssh -p 2222 travis@localhost
# sudo is password less
# you need to kill the ssh tunnel on the server to let your build finish, it
# seems build servers live a while beyond you stopping the build
#################################################
# Creating screenshot at hanged builds  (after 5min)
#################################################
# Enable AT
- sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.atrun.plist
# Prepare screenshot script to upload to remote ssh server
- echo "screencapture screenshot.jpg" > screenshot.sh
- echo "scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no  -i
  ssh/travisci screenshot.jpg ubuntu@someremotehostonaws.compute.amazonaws.com:"
>> screenshot.sh
- cat screenshot.sh
- chmod +x screenshot.sh
# After 5 minutes take a screenshot
- at -f screenshot.sh now+5min
#################################################
# Enable Apple Remote mgmt of system (can be tunneled using same mechanism as
# ssh tunnel -R)
#################################################
- sudo
  /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart
-activate -configure -access -off -restart -agent -privs -all -allowAccessFor
-allUsers