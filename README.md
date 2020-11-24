# CAMERA STATION

## INTRODUCTION
This repository contains the ``/home/pi`` folder for the Raspberry Pi appliance developed to run the camera station developed for the DOE SRNL MDCT2 project.

## HARDWARE REQUIRED
* [Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
* [Raspberry Pi High Quality Camera](https://www.raspberrypi.org/products/raspberry-pi-high-quality-camera/)

## DEPENDENCIES
* NumPy
* OpenCV 4
* picamera
* [PyDNG](https://github.com/schoolpost/PyDNG)

## INSTALLATION
* Clone the PyDNG repository

        cd /home/pi
        mkdir --parent /home/pi/src/python/pkg
        cd /home/pi/src/python/pkg
        git clone https://github.com/schoolpost/PyDNG.git
        cd PyDNG
        sudo pip3 install src/.
