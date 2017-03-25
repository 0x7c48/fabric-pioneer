"""
Fabric tool for installing packages for Ubuntu 14.04 Gnome3


Usage:
	fab --password=PASSWORD --fabfile=gnome3_packages.py localhost software

Answer Yes always:
    sudo apt-get install -y gimp
    sudo add-apt-repository repo -y

Docs:
    Sources list: /etc/apt/sources.list
    "http://repogen.simplylinux.ch/generate.php"

Fabric:
    https://nulab-inc.com/blog/nulab/advanced-method-define-tasks-fabric

"""

import inspect
import sys
import os

from fabric.tasks import Task
from fabric.state import env
from fabric.api import task, cd, lcd
from fabric.operations import local
from fabric.api import task, execute
from fabric.operations import prompt, run
from fabric.colors import red, green


SUDO_INSTALL = "sudo apt-get install -y "
SUDO_UPDATE = "sudo apt-get update"
PIP_INSTALL = "sudo pip install "

SUDO_ADD_APT = "sudo add-apt-repository "
SUDO_UPDATE = "sudo apt-get update"


@task
def localhost():
    """localhost install.

    Core helpers function for fabric.
    If you wont install software local use this function belov.
    Usage:
        fab --password=$PASSWORD --fabfile=gnome3_packages.py localhost same_fab_task
    """
    env.run = local
    env.hosts = ['localhost']
    env.warn_only = True
    env.colorize_errors = True


# SYSTEM


# Must be first task.
@task
def update_upgrade():
    """System update upgrade."""
    r1 = env.run("sudo apt-get autoremove -y && sudo apt-get update && sudo apt-get upgrade -y")
    return r1


@task
def aptitude():
    """Install aptitude."""
    r1 = env.run(SUDO_INSTALL + "aptitude")
    return r1


@task
def gdebi_core():
    """For installing deb packeges."""
    r1 = env.run(SUDO_INSTALL + "gdebi-core")
    return r1


@task
def lshw_gtk():
    """Install lshw-gtk.

    Hardware informations.
    """
    r1 = env.run(SUDO_INSTALL + "lshw-gtk")
    return r1


@task
def psycopg2():
    """Install psycopg2."""
    r1 = env.run(SUDO_INSTALL + "python-psycopg2")
    return r1


@task
def git():
    """Install git."""
    r1 = env.run(SUDO_INSTALL + "git")
    return r1


@task
def pip():
    """Install and upgrade pip."""
    r1 = env.run(SUDO_INSTALL + "python-dev python-pip build-essential python-setuptools")
    r2 = env.run(PIP_INSTALL + "--upgrade pip")
    return r1, r2


@task
def virtualenv():
    """Install and upgrade virtualenv."""
    r1 = env.run(PIP_INSTALL + "--upgrade virtualenv")
    return r1


@task
def sublime_text_2():
    """Install sublime-text-2.
    
    http://community.linuxmint.com/tutorial/view/907

    Source:
    http://www.sublimetext.com/2
    """
    r1 = env.run(SUDO_ADD_APT + "ppa:webupd8team/ -y")
    r2 = env.run(SUDO_UPDATE)
    r3 = env.run(SUDO_INSTALL + "sublime-text")
    return r1, r2, r3


@task
def sublime_text_3():
    """Install sublime-text-3.
    
    http://community.linuxmint.com/tutorial/view/907

    Source:
    http://www.sublimetext.com/2
    """
    r1 = env.run(SUDO_ADD_APT + "ppa:webupd8team/sublime-text-3 -y")
    r2 = env.run(SUDO_UPDATE)
    r3 = env.run(SUDO_INSTALL + "sublime-text-installer")
    return r1, r2, r3


@task
def indicator_multiload():
    """Install indicator-multiload.""" 
    r1 = env.run("sudo add-apt-repository ppa:indicator-multiload/stable-daily -y")
    r2 = env.run(SUDO_UPDATE)
    r3 = env.run(SUDO_INSTALL + "indicator-multiload")
    return r1, r2, r3


@task
def java():
    """Install java."""
    r1 = env.run(SUDO_ADD_APT + "ppa:webupd8team/java -y")
    r2 = env.run(SUDO_UPDATE)
    r3 = env.run(SUDO_INSTALL + "echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections")
    r4 = env.run(SUDO_INSTALL + "oracle-java8-installer")
    return r1, r2, r3, r4


@task
def pycharm():
    """Install pycharm."""
    with lcd("/opt"):
        r1 = env.run("wget http://download.jetbrains.com/python/pycharm-professional-3.4.1.tar.gz")
        r2 = env.run("sudo tar -xzvf pycharm-professional-3.4.1.tar.gz")
        r3 = env.run("sudo rm pycharm-professional-3.4.1.tar.gz")
        r4 = env.run("sudo ln -s /opt/pycharm-professional-3.4.1/bin/pycharm.sh /usr/bin/pycharm")
    return r1, r2, r3, r4


@task
def htop():
    """Install htop.
    """
    r1 = env.run(SUDO_INSTALL + "htop")
    return r1


#@task
#def generate_ssh_key_local():
#    """Generate ssh_key on localhost."""
#    SSH_PATCH = "~/.ssh"
#    ID_RSA_PUB = "~/.ssh/id_rsa.pub"
#    AUTHORIZED_KEYS = "~/.ssh/authorized_keys"
#    ID_RSA = "~/.ssh/id_rsa"
#
#    if not os.path.exists(os.path.expanduser(ID_RSA_PUB)):
#        with lcd(SSH_PATCH):
#            email = raw_input("Email: ")
#            local("ssh-keygen -t rsa -C {email}".format(email=email))
#            local("ssh-add {id_rsa}".format(id_rsa=ID_RSA))
#    else:
#        # Once type passphrase at start of deploy.
#        if os.path.exists(os.path.expanduser(ID_RSA)):
#            local("ssh-add {0}".format(ID_RSA))
#

# NVIDIA


@task
def bumblebee():
    """Install bumblebee.
    
    $ optirun [options] <application> [application-parameters]

    https://wiki.ubuntu.com/Bumblebee
    http://community.linuxmint.com/tutorial/view/1299
    
    Check:
          optirun -vv
          tail /var/log/kern.log
    """
    r1 = env.run(SUDO_ADD_APT + "ppa:bumblebee/stable -y")
    r2 = env.run(SUDO_UPDATE)
    r3 = env.run(SUDO_INSTALL + "linux-headers-generic bbswitch-dkms nvidia-current bumblebee bumblebee-nvidia primus acpidump iasl dmidecode")
    # sudo gedit /etc/bumblebee/bumblebee.conf
    # Manualy you need set: 
      # Driver=nvidia
      # KernelDriver=nvidia-current
      # Module=nvidia
    # TODO: add check for optirun: optirun nvidia-settings -c :8
    return r1, r2, r3


@task
def bumblebee_gui():
    """Install bumblebee gui.

       http://askubuntu.com/questions/452556/how-to-set-up-nvidia-optimus-bumblebee-in-14-04
    """
    r1 = env.run(SUDO_INSTALL + "python-appindicator")
    # cd home
    with lcd("~"):
        r2 = env.run("git clone https://github.com/Bumblebee-Project/bumblebee-ui.git")
        r3 = env.run("cd bumblebee-ui")
        r4 = env.run("sudo ./INSTALL")
    return r1, r2, r3, r4


@task
def compiz():
    """Install compiz."""
    r1 = env.run(SUDO_INSTALL + "compizconfig-settings-manager compiz-plugins-extra")
    return r1


@task
def postgresql():
    """Install postgresql."""
    r1 = env.run(SUDO_ADD_APT + "ppa:tualatrix/ppa -y")
    r2 = env.run(SUDO_UPDATE)
    r3 = env.run(SUDO_INSTALL + "ubuntu-tweak")
    return r1, r2, r3


@task
def postgresql():
    """Install postgresql."""
    r1 = env.run(SUDO_INSTALL + "postgresql pgadmin3")
    return r1


@task
def virtualbox():
    """Install virtualbox."""
    r1 = env.run(SUDO_INSTALL + "virtualbox")
    return r1


@task
def nginx():
    """Install nginx."""
    r1 = env.run(SUDO_INSTALL + "nginx")
    return r1


@task
def build_essential_binutils():
    """Install build-essential binutils."""
    r1 = env.run(SUDO_INSTALL + "build-essential binutils")
    return r1


@task
def python_setuptools():
    """Install python-setuptools."""
    r1 = env.run(SUDO_INSTALL + "python-setuptools")
    return r1


@task
def python_dev():
    """Install python_dev."""
    r1 = env.run(SUDO_INSTALL + "python-dev")
    return r1


# PYPI


@task
def django():
    """Install django."""
    r1 = env.run(PIP_INSTALL + "django")
    return r1


@task
def ipython():
    """Install and upgrade ipython."""
    r1 = env.run(PIP_INSTALL + "--upgrade ipython[all]")
    r2 = env.run(PIP_INSTALL + "nose")
    print(green('Run iptest for ipython.'))
    r3 = env.run("iptest")
    return r1, r2, r3

@task
def requests():
    """Install requests."""
    r1 = env.run(PIP_INSTALL + "requests")
    return r1


# WEB/communications APPS


@task
def google_chrome_stable():
    """Install google-chrome-stable."""
    r1 = env.run(SUDO_INSTALL + "libxss1 libappindicator1 libindicator7")
    r2 = env.run("wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
    r3 = env.run("sudo dpkg -i google-chrome*.deb")
    r4 = env.run("sudo rm google-chrome*.deb")
    return r1, r2, r3, r4


@task
def flashplugin_installer():
    """Install flashplugin-installer."""
    r1 = env.run(SUDO_INSTALL + "flashplugin-installer")
    return r1


@task
def skype():
    """Install scype.

    Source:
    http://www.skype.com/go/getskype-linux-ubuntu-64
    """
    with lcd("~"):
        r1 = env.run("wget http://www.skype.com/go/getskype-linux-ubuntu-64")
        r2 = env.run("mv getskype-linux-ubuntu-64 getskype-linux-ubuntu-64.deb")
        r3 = env.run("sudo dpkg -i getskype-linux-ubuntu-64.deb")
        # clean up, delete downloaded file.
        # TODO: delete when install only.
        r4 = env.run("rm getskype-linux-ubuntu-64.deb")
    return r1, r2, r3, r4


@task
def skype_call_recorder():
    """Install skype call recorder.
    
    Source file:
    skype-call-recorder-ubuntu_0.10_amd64.deb
    """
    r1 = env.run("sudo wget http://atdot.ch/scr/files/0.10/skype-call-recorder-ubuntu_0.10_amd64.deb")
    r2 = env.run("sudo dpkg --install skype-call-recorder-ubuntu_0.10_amd64.deb")
    # clean up, delete downloaded file.
    r3 = env.run("sudo rm skype-call-recorder-ubuntu_0.10_amd64.deb")
    return r1, r2, r3


# VIDEO/AUDIO


@task
def amarok():
    """Install amarok.

    Amarok is a powerful music player with an intuitive interface.
    It makes playing the music you love and discovering new music
     easier than ever before and it looks good doing it! 
    """
    r1 = env.run(SUDO_INSTALL + "amarok")
    return r1


@task
def audacity():
    """Install audacity.

    Audacity is a free open source digital audio editor and recording 
    computer software application, available for Windows, Mac OS X, 
    Linux and other operating systems."""
    r1 = env.run(SUDO_INSTALL + "audacity")
    return r1


@task
def vlc():
    """Install vlc."""
    r1 = env.run(SUDO_INSTALL + "vlc")
    return r1


# UTILITIES


@task
def mc():
    """Install mc."""
    r1 = env.run(SUDO_INSTALL + "mc")
    return r1


@task
def unrar():
    """Install unrar."""
    r1 = env.run(SUDO_INSTALL + "unrar")
    return r1


@task
def rar():
    """Install rar."""
    r1 = env.run(SUDO_INSTALL + "rar")
    return r1


@task
def p7zip_full():
    """Install p7zip-full.
    Usage: 7z e /path/to/file

    When error:
    skipping: need PK compat. v5.1 (can do v4.6)
    skipping: need PK compat. v5.1 (can do v4.6)
    """
    r1 = env.run(SUDO_INSTALL + "p7zip-full")
    return r1


@task
def unetbootin():
    """Install unetbootin."""
    r1 = env.run(SUDO_INSTALL + "unetbootin")
    return r1


@task
def dropbox():
    """Install dropbox."""
    r1 = env.run(SUDO_INSTALL + "nautilus-dropbox")
    return r1


@task
def guake():
    """Install guake terminal."""
    r1 = env.run("sudo apt-get build-dep -y guake")
    r2 = env.run(SUDO_INSTALL + "guake")
    return r1, r2


@task
def pdfmod():
    """Install pdfmod."""
    r1 = env.run("sudo add-apt-repository ppa:pdfmod-team/ppa -y")
    r2 = env.run(SUDO_UPDATE)
    r3 = env.run(SUDO_INSTALL + "pdfmod")
    return r1, r2, r3


@task
def calibre():
    """Install calibre epub.""" 
    r1 = env.run(SUDO_INSTALL + "calibre")
    return r1


@task
def gimp():
    """Install gimp."""
    r1 = env.run(SUDO_INSTALL + "gimp")
    return r1


@task
def filezilla():
    """Install filezilla."""
    r1 = env.run(SUDO_INSTALL + "filezilla")
    return r1


@task
def googleearth():
    """Install googleearth."""
    r1 = env.run(SUDO_INSTALL + "googleearth")

    return r1


@task
def cheese():
    """Install cheese."""
    r1 = env.run(SUDO_INSTALL + "cheese")
    return r1


@task
def docky():
    """Install docky."""
    r1 = env.run(SUDO_INSTALL + "docky")
    return r1


@task
def playonlinux():
    """Install playonlinux."""
    r1 = env.run(SUDO_INSTALL + "playonlinux")
    return r1


# GNOME EXTENSIONS https://extensions.gnome.org/extension


@task
def gnome_tweak_tool():
    """Install gnome-tweak-tool."""
    r1 = env.run(SUDO_INSTALL + "gnome-tweak-tool")
    return r1


@task
def alternative_status_menu():
    """Install alternative-status-menu extensions for gnome.

    https://github.com/paradoxxxzero/gnome-shell-system-monitor-applet
    """
    r1 = env.run(SUDO_INSTALL + "gir1.2-gtop-2.0 gir1.2-networkmanager-1.0")
    return r1


@task
def system_monitor():
    """Install system-monitor extensions for gnome.

    https://github.com/paradoxxxzero/gnome-shell-system-monitor-applet
    """
    r1 = env.run(SUDO_INSTALL + "gir1.2-gtop-2.0 gir1.2-networkmanager-1.0")
    return r1


@task
def gnome_shell_extensions_user_theme():
    """Install gnome-shell-extensions-user-theme extensions for gnome.

    gnome-shell-extensions-user-theme
    """
    r1 = env.run(SUDO_INSTALL + "gnome-shell-extensions-user-theme")
    return r1


@task
def gnome_shell_extensions_drive_menu():
    """Install gnome-shell-extensions-drive-menu extensions for gnome.

    gnome-shell-extensions-user-theme
    """
    r1 = env.run(SUDO_INSTALL + "gnome-shell-extensions-drive-menu")
    return r1


@task
def gnome_shell_extensions_applications_menu():
    """Install gnome_shell_extensions_applications_menu.

    gnome_shell_extensions_applications_menu
    """
    r1 = env.run(SUDO_INSTALL + "gnome-shell-extensions-applications-menu")
    return r1


@task
def gnome_shell_extensions_drop_down_terminal():
    """Install gnome_shell_extensions_drop_down_terminal.

    gnome_shell_extensions_drop_down_terminal
    """
    r1 = env.run(SUDO_INSTALL + "gnome-shell-extensions-drop-down-terminal")
    return r1


# Finish tasks. Put tasks upper of this function.
# Update system and check dependencies.


@task
def finish_update_upgrade():
    """System update upgrade."""
    r1 = env.run("sudo apt-get update && sudo apt-get upgrade")
    return r1


# Dependencies

@task
def check_dependencies():
    """Verify that there are no broken dependencies."""
    r1 = env.run(SUDO_INSTALL + "check")
    return r1


# Run all tasks.


@task
def software():
    """Main task that execute all (with outh that in ESC_TASK_LIST) from this module
in order of top to buttom.
    
    Status code, http://librairie.immateriel.fr/fr/read_book/9780596515829/ch10
    0
        Success
    1
        General errors
    2
        Misuse of shell built-ins
    126
        Command invoked cannot execute
    127
        Command not found
    128
        Invalid argument to exit
        Fatal error signal 'n'
    130
        100 installed.
    """
    ESC_TASK_LIST = ['localhost', 'install_software']
    module_fab_task_list = sorted(dict(inspect.getmembers(sys.modules[__name__], lambda a: isinstance(a, Task) and a.__name__ not in ESC_TASK_LIST)).values(), key=lambda v: v.func_code.co_firstlineno)
    error_list = []
    for fab_task in module_fab_task_list:
        result = execute(fab_task)
        for error_tuple in result.values():
            if error_tuple:
                for error in error_tuple:
                    if error not in [0, 100, None, '']:
                        error_list.append(error)
                        print(red("Error during instalettion ") + red(str(fab_task.__name__)))
    if error_list:
        print(red(error_list)) 
    else:
        print(green('All is OK!'))
