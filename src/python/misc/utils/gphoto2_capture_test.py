import sys

import gphoto2 as gp

import camera
import database

camera_parameters = database.get_gphoto2_camera_parameters()

camera_parameters['connection'] = gp.Camera()

try:
   msg = 'Initializing camera ...'
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   camera_parameters['connection'].init()
except gp.GPhoto2Error as exception:
   if exception.code == gp.GP_ERROR_MODEL_NOT_FOUND:
      msg = '*** ERROR *** '
      msg += 'gPhoto2 camera not found, please connect and switch '
      msg += 'on camera'
      msg += '\n'
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()

try:
   msg = 'Capturing image ...'
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   camera_filepath = \
      camera_parameters['connection'].capture(gp.GP_CAPTURE_IMAGE)
except:
   msg = '*** ERROR *** '
   msg += 'gPhoto2 capture unsuccessful, try power cycling the camera'
   msg += '\n'
   msg += '\n'
   sys.stderr.write(msg)
   sys.stderr.flush()
   sys.exit()

msg = 'Camera folder: {0}'.format(camera_filepath.folder)
msg += '\n'
msg += 'Camera filename: {0}'.format(camera_filepath.name)
msg += '\n'
sys.stdout.write(msg)
sys.stdout.flush()

msg = 'Deleting image from camera\'s SD card ...'
msg += '\n'
sys.stdout.write(msg)
sys.stdout.flush()
camera_parameters['connection'].file_delete(camera_filepath.folder,
                                            camera_filepath.name)

camera_parameters['connection'].exit()
msg = 'gPhoto2 camera connection is closed ...'
msg += '\n'
sys.stdout.write(msg)
sys.stdout.flush()
