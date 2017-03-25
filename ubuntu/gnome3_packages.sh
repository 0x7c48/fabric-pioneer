#!/bin/zsh

# ========================
# Fabric tool for installing packages for Ubuntu 14.04 Gnome3

# Requirements:
#	OS - Ubuntu
#	Gnome3	
#	bash: zsh
#   fabfile/gnome3_packages.py

# Usage:
# 	chmod +x gnome3_packages.sh
# 	zsh gnome3_packages.sh


SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
LOGFILE=$SCRIPTPATH/log/gnome3_packages.log


function logo {
	echo
	echo ' ___________     ___.         .__                .__                                   '
	echo ' \_   _____/____ \_ |_________|__| ____   ______ |__| ____   ____   ____   ___________ '
	echo '  |    __) \__  \ | __ \_  __ \  |/ ___\  \____ \|  |/  _ \ /    \_/ __ \_/ __ \_  __ \'
	echo '  |     \   / __ \| \_\ \  | \/  \  \___  |  |_> >  (  <_> )   |  \  ___/\  ___/|  | \/'
	echo '  \___  /  (____  /___  /__|  |__|\___  > |   __/|__|\____/|___|  /\___  >\___  >__|   '
	echo '      \/        \/    \/              \/  |__|                  \/     \/     \/       '
	echo 
	echo '2015'
	echo
}


# Args case, check only first and call first and rest functions
if [ $1 ]
then
	logo
	
	# Custom prompt password
	echo
	stty -echo
	printf 'Enter [sudo] password: '
	IFS= read -r PASSWORD
	printf '\n'
	
	# fabric
	echo "First of all install fabric."
	echo $PASSWORD|sudo -S apt-get install -y fabric

	# Run fabfile via script, get rest args
	echo "Run fabfile: $SCRIPTPATH/fabfile/gnome3_packages.py"
	FAB="echo $PASSWORD|sudo -S fab --password=$PASSWORD -f $SCRIPTPATH/fabfile/gnome3_packages.py localhost $*"
	# script command. It will copy everything that goes to screen in a log file.
	if [ $LOGFILE ]
	then
		script -a -c "$FAB" $LOGFILE
	else
		script -c "$FAB" $LOGFILE
	fi	
else
    logo
    printf '%s\n' 'No args'
    # List of all commands
    printf '%s\n' 'List of all args'
    fab -f $SCRIPTPATH/fabfile/gnome3_packages.py --list
fi
