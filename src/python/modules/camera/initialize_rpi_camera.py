import sys
import time

import picamera

import camera
import database

def initialize_rpi_camera(verbose=False):
   # Pick up the camera parameters from the appropriate database
   if verbose:
      msg = 'Picking up the latest Raspberry Pi camera '
      msg += 'database parameters ...'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
   parameters = database.get_rpi_camera_parameters()

   if parameters:
      # Turn on the Raspberry Pi camera
      if verbose:
         msg = 'Turning on the Raspberry Pi camera ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      try:
         parameters['connection'] = picamera.PiCamera()
      except:
         msg = '*** ERROR *** '
         msg += 'Raspberry Pi camera connection could not be established'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()

      # Configure the Raspberry Pi camera
      if verbose:
         msg = 'Configuring the Raspberry Pi camera ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      camera.set_parameters_for_rpi_camera(parameters)

      # Warmup the Raspberry Pi camera
      for second in range(parameters['secondsToWarmup']):
         time.sleep(1)
         if verbose:
            msg = 'Warming up the Raspberry Pi camera ... '
            msg += '{0} [s]'.format(parameters['secondsToWarmup'] - \
                                                                   second - 1)
            msg += '\r'
            sys.stdout.write(msg)
            sys.stdout.flush()
      if verbose:
         msg = '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      return parameters

   else:
      msg = '... connection to RPi camera parameters database was '
      msg += 'unsuccessful'
      msg += '\n'
      msg = '... exiting'
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()
