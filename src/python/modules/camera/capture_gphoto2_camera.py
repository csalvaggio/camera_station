import os
import os.path
import sys

import gphoto2 as gp

def capture_gphoto2_camera(camera_parameters, basename, verbose=False):
   """
   IMPORTANT NOTE:

   When using this capture method, the camera must be set to capture RAW or
   JPG only, NOT BOTH

   """
   # Capture image from gPhoto2 camera
   if verbose:
      msg = '... triggering camera'
      msg +=  '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
   try:
      camera_filepath = \
         camera_parameters['connection'].capture(gp.GP_CAPTURE_IMAGE)
   except:
      msg = '... gPhoto2 capture unsuccessful, try power cycling the camera'
      msg += '\n'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
      return None

   # Add extension to the basename to match the image file on the
   # camera's SD card
   extension = os.path.splitext(camera_filepath.name)[1].lower()
   filepath = basename + extension

   # Extract image from the camera's SD card and save to local disk
   if verbose:
      msg = '... extracting image from camera\'s SD card to'
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

   # Delete image from the camera's SD card
   if verbose:
      msg = '... deleting image from camera\'s SD card'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
   camera_parameters['connection'].file_delete(camera_filepath.folder,
                                               camera_filepath.name)

   if verbose:
      msg = '... completed'
      msg += '\n'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()

   # Clean up memory
   del camera_file
   del camera_filepath

   return filepath
