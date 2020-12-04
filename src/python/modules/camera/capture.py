import sys

import camera

def capture(station_parameters, camera_parameters, filepath, verbose=False):
   # Raspberry Pi camera
   if station_parameters['cameraType'] == 'rpi':
      camera.capture_rpi_camera(camera_parameters,
                                filepath,
                                verbose=verbose)
   # gPhoto2 camera
   elif station_parameters['cameraType'] == 'gphoto2':
      camera.capture_gphoto2_camera(camera_parameters,
                                    filepath,
                                    verbose=verbose)
   else:
      msg = '*** ERROR *** Specified camera type not supported: '
      msg += '{0}'.format(station_parameters['cameraType'])
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()