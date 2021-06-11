import os
import os.path

reboot_required_file = '/tmp/reboot_required'

if os.path.isfile(reboot_required_file):
   cmd = 'sudo rm ' + reboot_required_file
   os.system(cmd)
   cmd = 'sudo shutdown -r now'
   os.system(cmd)
