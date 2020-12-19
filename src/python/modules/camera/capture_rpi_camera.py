import os
import sys

import pydng.core

def capture_rpi_camera(camera_parameters, basename, verbose=False):
   # Add extension to the basename for storing the JPEG + RAW file
   filepath = basename + '.jpg'

   # Capture image from Raspberry Pi camera
   if verbose:
      msg = '... acquiring image and saving to '
      msg += '\n'
      msg += '       {0}'.format(filepath)
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
   camera_parameters['connection'].capture(filepath, format='jpeg', bayer=True)

   # Extract the raw Bayer image from the JPEG metadata and save it to
   # a digital negative (DNG) file
   if verbose:
      msg = '... extracting digital negative (DNG) image from '
      msg += '\n'
      msg += '       {0}'.format(filepath)
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
   d = pydng.core.RPICAM2DNG()
   d.convert(filepath, compress=camera_parameters['useLosslessJpegCompression'])
   os.remove(filepath)
   if verbose:
      msg = '... completed'
      msg += '\n'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()

   return 1
