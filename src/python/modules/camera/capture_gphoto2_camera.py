import os
import sys

import gphoto2 as gp

def capture_gphoto2_camera(camera_parameters, filepath, verbose=False):
   """
   IMPORTANT NOTE:

   When using this capture method, the camera must be set to capture RAW or
   JPG only, NOT BOTH

   DATABASE "imageExtension" FIELD MUST MATCH CAMERA FILE EXTENSION

   """
   # Capture image from gPhoto2 camera
   if verbose:
      msg = '... triggering camera'
      msg +=  '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
   camera_filepath = \
      camera_parameters['connection'].capture(gp.GP_CAPTURE_IMAGE)

   # Extract image from the camera's SD card and save to local disk
   if verbose:
      msg = '... extracting image from camera\'s SD to '
      msg += '\n'
      msg += '       {0}'.format(filepath)
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
   camera_file = \
      camera_parameters['connection'].file_get(camera_filepath.folder,
                                               camera_filepath.name,
                                               gp.GP_FILE_TYPE_NORMAL)
   camera_file.save(filepath)
   if verbose:
      msg = '... completed'
      msg += '\n'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()

   # Clean up memory
   del camera_file
   del camera_filepath
