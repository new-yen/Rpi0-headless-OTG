# Rpi0-headless-OTG
Setup for a headless Raspberry Pi Zero 2W

## Install Raspberry Pi OS via Raspberry Pi Imager: 
https://www.raspberrypi.com/software/

- I used Raspberry Pi OS (LEGACY, 32-bit) Lite
- Opening OS Customisation Menu (Ctrl + Shift + X)

Setup:
  - hostname
  - username
  - password
  - Wifi
  - enable SSH

More info: 

https://www.samwestby.com/tutorials/rpi-headless-setup.html
https://www.youtube.com/watch?v=9fEnvDgxwbI&ab_channel=SamWestbyTech


##  Fix Issues

Locale issue/Check status: 
- locale

Execute:
- echo "LC_ALL=en_GB.UTF-8" | sudo tee -a /etc/environment
- echo "en_GB.UTF-8 UTF-8" | sudo tee -a /etc/locale.gen
- echo "LANG=en_GB.UTF-8" | sudo tee -a /etc/locale.conf
- sudo locale-gen en_GB.UTF-8



wiringPi issue:

- cd /tmp
- wget https://project-downloads.drogon.net/wiringpi-latest.deb
- sudo dpkg -i wiringpi-latest.deb


# Additional Setup:

- File Sharing with Samba:
By now, macOS uses Samba as its default network sharing protocol. So you can install it on the Raspberry Pi and macOS will handle it:
  sudo apt update && sudo apt upgrade
  sudo apt install samba samba-common-bin

- By default, Samba allows access to the home folder of the logged in user so no further shares need to be configured if you just want access to your home folder. Again, macOS does not like using standard UNIX accounts for authenticating with Samba, so we need to set a dedicated Samba password.

  To do so:
  sudo smbpasswd -a pi

- Where pi refers to the user account on the Raspberry Pi you want to connect to.

- By default, Samba exposes home folders as read-only. To change that, modify Samba’s main config file smb.conf:
  sudo nano /etc/samba/smb.conf

- In there, scroll down to the [homes] section and set read only = no to make shared home folders writable.

- To share more resources like an external drive, add another section at the end of your smb.conf and make it fully writable:

[homes]
   comment = Home Directories
   browseable = no

By default, the home directories are exported read-only. Change the next parameter to 'no' if you want to be able to write to them.
   read only = no
   public = yes
   writable = yes


After setting a new password and modifying smb.conf, restart the Samba service:
sudo service smbd restart

Open “Finder” on Mac -> Click “Go” and click “Connect to Server . . . “ -> “Connect to Server” dialog, enter “smb://rpi0-1.local (hostname)” into the Server Address, and click “Connect”

