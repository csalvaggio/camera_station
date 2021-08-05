import os
import os.path
import time

import utils

reboot_required = False

delay = 5

max_attempts = 10
attempt = 0

while attempt < max_attempts:
   if utils.network_available():
      reboot_required = False
      break
   else:
      reboot_required = True

   attempt += 1

   time.sleep(delay)

if reboot_required:
   cmd = 'sudo shutdown -r now'
   os.system(cmd)
