import sys

import camera

def power_on(station_parameters,
             startup_duration=15,
             verbose=False):
   # Raspberry Pi camera
   if station_parameters['cameraType'].lower() == 'rpi':
      camera.power_on_rpi_camera(startup_duration=startup_duration,
                                 verbose=verbose)
   # gPhoto2 camera
   elif station_parameters['cameraType'].lower() == 'gphoto2':
      camera.power_on_gphoto2_camera(startup_duration=startup_duration,
                                     verbose=verbose)
   else:
      msg = '*** ERROR *** Specified camera type not supported: '
      msg += '{0}'.format(station_parameters['cameraType'])
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()
