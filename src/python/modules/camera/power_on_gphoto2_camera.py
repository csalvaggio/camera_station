import sys
import time

import power

def power_on_gphoto2_camera(startup_duration=15,
                            verbose=False):
   try:
      # Instantiate a switch
      switch = power.Switch(control_pin=21, load_connection='no')

      # Physically power on the camera
      if verbose:
         msg = '... powering ON the gPhoto2 camera'
         msg += '\n'
         sys.stdout.write(msg)
      switch.position(1)

      # Delay for the specified amount of time while camera goes through
      # its' boot sequence
      if startup_duration:
         for second in range(startup_duration):
            time.sleep(1)
            if verbose:
               msg = '... waiting '
               msg += '{0:2d} [s]'.format(startup_duration - second - 1)
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
