alias rm='rm --interactive'

# Camera station specific utilities
alias camera_off='/usr/bin/python3 /home/pi/src/python/modules/power/Switch.py --state off'
alias camera_on='/usr/bin/python3 /home/pi/src/python/modules/power/Switch.py --state on'
alias collect='/usr/bin/python3 /home/pi/src/python/misc/collect.py --verbose --keep'
alias dump='/usr/bin/python3 /home/pi/src/python/misc/collect.py --dump-database'
alias flash='/usr/bin/python3 /home/pi/src/python/misc/collect.py --flash-camera-settings'
alias gphoto2_capture_test='/usr/bin/python3 /home/pi/src/python/misc/utils/gphoto2_capture_test.py'
alias humidity='/usr/bin/python3 /home/pi/src/python/modules/sensors/temperature_humidity.py'
alias station_name='/usr/bin/python3 /home/pi/src/python/misc/utils/station_name.py'
alias temperature='/usr/bin/python3 /home/pi/src/python/modules/sensors/temperature_humidity.py'
alias upload='/usr/bin/python3 /home/pi/src/python/modules/utils/upload_files_to_ftp_server.py --verbose --report --local-directory /media/pi/STORAGE'
alias upload_and_delete='/usr/bin/python3 /home/pi/src/python/modules/utils/upload_files_to_ftp_server.py --verbose --report --local-directory /media/pi/STORAGE'
alias voltmeter='/usr/bin/python3 /home/pi/src/python/modules/battery/Voltmeter.py'
