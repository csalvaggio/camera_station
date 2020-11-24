import sys

import camera

def initialize(station_parameters, verbose=False):
   if station_parameters['cameraType'] == 'rpi':
      # Raspberry Pi camera
      parameters = \
         camera.initialize_rpi_camera(station_parameters, verbose=verbose)
   elif station_parameters['cameraType'] == 'gphoto2':
      # gPhoto2 camera
      parameters = \
         camera.initialize_gphoto2_camera(station_parameters, verbose=verbose)
   else:
      msg = '*** ERROR *** Specified camera type not supported: '
      msg += '{0}'.format(station_parameters['cameraType'])
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()

   return parameters



if __name__ == '__main__':
   import camera

   station_parameters = {}
   station_parameters['cameraType'] = 'rpi'

   camera_parameters = camera.initialize(station_parameters, verbose=True)

   camera.close(station_parameters, camera_parameters)
