import sys
import time

import power

def power_off_gphoto2_camera(shutdown_duration=15,
                             verbose=False):
   try:
      # Instantiate a switch
      switch = power.Switch(control_pin=21, load_connection='no')

      # Physically power off the camera
      if verbose:
         msg = '... powering OFF the gPhoto2 camera'
         msg += '\n'
         sys.stdout.write(msg)
      switch.position(0)

      # Keep the camera powered off for the specified amount of time
      for second in range(shutdown_duration):
         time.sleep(1)
         if verbose:
            msg = '... waiting '
            msg += '{0:2d} [s]'.format(shutdown_duration - second - 1)
            msg += '\r'
            sys.stdout.write(msg)
            sys.stdout.flush()
      if verbose:
         msg = '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      # Discard the switch
      switch.close()

   except KeyboardInterrupt:
      switch.close()
      if verbose:
         msg = '\n'
         msg += '\n'
         msg += 'Exiting ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      sys.exit()
