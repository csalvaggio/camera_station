# CAMERA STATION

## INTRODUCTION
This repository contains the ``/home/pi`` folder for the Raspberry Pi appliance developed to run the camera station developed for the DOE SRNL MDCT2 project.   

## HARDWARE REQUIRED
* [Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
* [Raspberry Pi High Quality Camera](https://www.raspberrypi.org/products/raspberry-pi-high-quality-camera/)
* [GPhoto2 Compatible Camera](http://www.gphoto.org/proj/libgphoto2/support.php)
* RIT-designed Raspberry Pi Voltmeter Board

## DEPENDENCIES
* NumPy
* OpenCV 4
* picamera
* [GPhoto2](http://www.gphoto.org)
* [PyDNG](https://github.com/schoolpost/PyDNG)

## INSTALLATION
* Install the **Raspberry Pi OS Full** operating system on an SD card using one of the recommended methods
    * [Raspberry Pi Imager for Windows](https://downloads.raspberrypi.org/imager/imager.exe)
    * [Raspberry Pi Imager for macOS](https://downloads.raspberrypi.org/imager/imager.dmg)
    * [Raspberry Pi Imager for Ubuntu](https://downloads.raspberrypi.org/imager/imager_amd64.deb)

* Perform headless configuration (on your setup machine)

    * Wireless networking

        Define a wpa_supplicant.conf file for your particular wireless network. Put this file in the ``/boot`` partition, and when the Pi first boots, it will copy that file into the correct location in the Linux root file system and use those settings to start up wireless networking.

        *wpa_supplicant.conf*

            ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
            update_config=1
            country=US

            network={
            	ssid="<insert your SSID here>"
            	psk="<insert your network's WPA passphrase here>"
            	key_mgmt=WPA-PSK
            }

    * Enable SSH

        For headless setup, SSH can be enabled by placing an empty file named ``ssh``, without any extension, onto the ``/boot`` partition of the SD card. When the Pi boots, it looks for the ``ssh`` file. If it is found, SSH is enabled and the file is deleted.

    * Change the hostname

        Using a macOS computer equipped with [Paragon Software's extFS](https://www.paragon-software.com/home/extfs-mac/) application. Insert the Raspberry Pi's SD card in the Mac. You will notice that two partitions are mounted; ``boot`` and ``rootfs``. The ``rootfs`` partition is the Raspberry Pi's main filesystem. The hostname (*e.g.* ``raspberrypi``) needs to be changed in two places on that filesystem

        */etc/hostname*

            srnlcamera

        and in

        */etc/hosts*

            127.0.0.1	localhost
            ::1			localhost ip6-localhost ip6-loopback
            ff02::1		ip6-allnodes
            ff02::2		ip6-allrouters

            127.0.1.1	srnlcamera0

        This can be done manually using your favorite editor (*e.g.* vi, nano, emacs, or Xcode).

    * Configure VNC

        Make the following modifications in ``/boot/config.txt``

            # uncomment to force a console size. By default it will be display's
            # size minus overscan.
            framebuffer_width=1920
            framebuffer_height=1080

            # uncomment if hdmi display is not detected and composite is being output
            hdmi_force_hotplug=1

            # uncomment to force a specific HDMI mode (this will force VGA)
            hdmi_group=2
            hdmi_mode=82

        >**NOTE:**
        
        >After booting the computer, if the display in "VNC Viewer" is not the proper/desired size, configure as follows

        >* Pi > Preferences > Screen Configuration
        
        >In the *Screen Layout Editor* ...
        
        >* Configure > Screens > HDMI-1 > Resolution > 1920x1080
        >* Configure > Apply

        >for the new resolution to take effect immediately.

        If it is still mounted, eject your SD card making sure you eject all partitions (under macOS you may use the ``diskutil`` command, *e.g.* ``diskutil umountDisk /dev/disk2`` where ``/dev/disk2`` is the name for the mounted volume)
        
* Insert SD card, and boot the Raspberry Pi

* Enable Raspberry Pi camera

        sudo raspi-config
    
    * Interface Options > Pi Camera > Yes

   Press "Ok", "Finish", and reboot the Raspberry Pi.

* Install these remaining packages

        sudo apt-get install vim
        sudo apt-get install dcraw
        sudo apt-get install udhcpd

* Clean up the ``/home/pi`` directory

        rm -fr Bookshelf Desktop Documents Downloads Music Pictures Public Templates Videos

* In the ``/home/pi`` directory, checkout this repository

        cd /home/pi
        git init
        git remote add origin git@github.com:csalvaggio/camera_station.git
        git fetch
        git checkout -f master

* Log out and log back in

* Clone the PyDNG repository

        cd /home/pi
        mkdir --parent /home/pi/src/python/pkg
        cd /home/pi/src/python/pkg
        git clone https://github.com/schoolpost/PyDNG.git
        cd PyDNG
        sudo pip3 install src/.

* Install ftp

        sudo apt-get install ftp

* Prioritize the order of precedence for the network interfaces (THIS MAY NOT BE NECESSARY IF THE WIFI INTERFACE IS DISABLED AS DESCRIBED BELOW)

    Edit ``/etc/dhcpcd.conf`` and add these lines, the lower the number, the higher prioity that is given to that interface

        interface wlan0
        metric 200

        inteface eth1
        metric 201

        inteface eth0
        metric 202

    then reboot the Pi.

* Configure and test gphoto2 by installing the following

        sudo apt-get install gphoto2 libgphoto2-6 libgphoto2-dev libgphoto2-dev-doc libgphoto2-l10n libgphoto2-port12 python-gphoto2-doc python-gphoto2cffi python-piggyphoto python3-gphoto2 python3-gphoto2cffi

    With a GPhoto2-compatible DSLR connected to the Raspberry Pi via a USB cable, check where gphoto2 is saving images on the camera

        gphoto2 --get-config capturetarget
           Label: Capture Target
           Readonly: 0
           Type: RADIO
           Current: Internal RAM    <--------
           Choice: 0 Internal RAM
           Choice: 1 Memory card
           END

    If gphoto2 indicates that it is currently saving to the Internal RAM as above, then configure gphoto2 so that captured images are saved to the SD card on the camera

        gphoto2 --set-config capturetarget=1
        gphoto2 --get-config capturetarget
           Label: Capture Target
           Readonly: 0
           Type: RADIO
           Current: Memory card     <---------
           Choice: 0 Internal RAM
           Choice: 1 Memory card
           END

    Configure maintenance cron jobs by typing ``crontab -e`` and inserting the following at the end of the crontab file

        * * * * * pkill -f gvfs-gphoto2-volume-monitor
        * * * * * pkill -f gvfsd-gphoto2




* If the Verizon Wireless USB730L modem is available, plug it in, and disable the onboard WiFi interface by editing the ``/boot/config.txt`` file and adding (or uncommenting) the following line

        # Uncomment this to disable the onboard WiFi
        dtoverlay=disable-wifi

    This is necessary to allow the USB730L modem to respond in a timely fashion to permit an incoming ssh or VNC connection when a WiFi network is also available.  This may not be necessary when the device is in the field.