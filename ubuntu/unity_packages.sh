#!/bin/zsh

# ========================
# Fabric tool for installing packages for Ubuntu 14.04 Unity

# Requirements:
#	OS - Ubuntu
#	Unity	
#	bash: zsh
#   fabfile/unity_packages.py

# Usage:
# 	chmod +x unity_packages.sh
# 	zsh unity_packages.sh


function logo {
	echo 
	echo ___________     ___.         .__                .__                                   
	echo \_   _____/____ \_ |_________|__| ____   ______ |__| ____   ____   ____   ___________ 
	echo  |    __) \__  \ | __ \_  __ \  |/ ___\  \____ \|  |/  _ \ /    \_/ __ \_/ __ \_  __ \
	echo  |     \   / __ \| \_\ \  | \/  \  \___  |  |_> >  (  <_> )   |  \  ___/\  ___/|  | \/
	echo  \___  /  (____  /___  /__|  |__|\___  > |   __/|__|\____/|___|  /\___  >\___  >__|   
	echo      \/        \/    \/              \/  |__|                  \/     \/     \/       
	echo 
	echo '2015'
	echo
}


echo
read -p "Enter [sudo] password: " PASSWORD
echo
echo

echo "First of all install fabric."
echo $PASSWORD|sudo -S apt-get install -y fabric

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

# run fabfile via script
echo "Run fabfile: $SCRIPTPATH/ubuntu/fabfile/unity_packages.py"
# Run fabric.
FAB="echo $PASSWORD|sudo -S fab --password=$PASSWORD -f $SCRIPTPATH/fabfile/unity_packages.py localhost $1"

# script command. It will copy everything that goes to screen in a log file.
script -c "$FAB" ../unity_packages.log
