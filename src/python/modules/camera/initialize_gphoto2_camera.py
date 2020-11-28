import sys
import time

import gphoto2 as gp

import camera
import database

def initialize_gphoto2_camera(station_parameters, verbose=False):
   # Pick up the camera parameters from the appropriate database
   if verbose:
      msg = 'Picking up the latest gPhoto2 camera '
      msg += 'database parameters ...'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
   parameters = database.get_gphoto2_camera_parameters()

   if parameters:
      # Connect to and initialize the gPhoto2 camera
      if verbose:
         msg = 'Connecting to the gPhoto2 camera ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      parameters['connection'] = gp.Camera()

      if verbose:
         msg = 'Initializing the gPhoto2 camera ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      while True:
         try:
            parameters['connection'].init()
         except gp.GPhoto2Error as exception:
            if exception.code == gp.GP_ERROR_MODEL_NOT_FOUND:
               msg = '*** WARNING *** '
               msg += 'gPhoto2 camera not found, please connect and switch '
               msg += 'on camera\n'
               sys.stderr.write(msg)
               sys.stderr.flush()
               try:
                  time.sleep(2)
               except KeyboardInterrupt:
                  msg = '\n'
                  msg += 'Exiting ...'
                  msg += '\n'
                  sys.stdout.write(msg)
                  sys.stderr.flush()
                  sys.exit()
               continue
            raise
         break

      # Configure the gPhoto2 camera
      if verbose:
         msg = 'Configuring the gPhoto2 camera ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      camera.set_parameters_for_gphoto2_camera(station_parameters, parameters)

      return parameters

   else:
      msg = '... connection to gphoto2 camera parameters database was '
      msg += 'unsuccessful'
      msg += '\n'
      msg = '... exiting'
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()
