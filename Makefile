# Usage:
#	make ubuntu_gnome3_packages git
#	make ubuntu_gnome3_packages git htop mc
#	make list_ubuntu_gnome3_packages

# make manual:
# 	http://www.gnu.org/software/make/manual/make.html#Automatic-Variables


# Get all args
ARGS = $(filter-out $@, $(MAKECMDGOALS))

# %: - rule which match any task name;
# @: - empty recipe = do nothing


ubuntu_gnome3_packages: ubuntu/gnome3_packages.sh
	zsh ubuntu/gnome3_packages.sh $(ARGS)

list_ubuntu_gnome3_packages: ubuntu/gnome3_packages.sh
	make ubuntu_gnome3_packages

ubuntu_unity_packages: ubuntu/unity_packages.sh
	zsh ubuntu/unity_packages.sh $(ARGS)

list_ubuntu_unity_packages: ubuntu/unity_packages.sh
	make ubuntu_unity_packages

test: ubuntu/gnome3_packages.sh
	make ubuntu_gnome3_packages git htop mc
%:
	@:
