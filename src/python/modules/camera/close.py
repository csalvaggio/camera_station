import sys

def close(station_parameters, camera_parameters, verbose=False):
   if station_parameters['cameraType'].lower() == 'rpi':
      # Raspberry Pi camera
      camera_parameters['connection'].close()
      if verbose:
         msg = 'Raspberry Pi camera connection is closed ...'
         msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
   elif station_parameters['cameraType'].lower() == 'gphoto2':
      # gPhoto2 camera
      camera_parameters['connection'].exit()
      if verbose:
         msg = 'gPhoto2 camera connection is closed ...'
         msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

   del camera_parameters['connection']
