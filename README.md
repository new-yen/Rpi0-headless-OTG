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
- echo "LC_ALL=en_US.UTF-8" | sudo tee -a /etc/environment
- echo "en_US.UTF-8 UTF-8" | sudo tee -a /etc/locale.gen
- echo "LANG=en_US.UTF-8" | sudo tee -a /etc/locale.conf
- sudo locale-gen en_US.UTF-8


wiringPi issue:

- cd /tmp
- wget https://project-downloads.drogon.net/wiringpi-latest.deb
- sudo dpkg -i wiringpi-latest.deb

