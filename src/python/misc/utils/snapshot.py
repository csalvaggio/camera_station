import argparse
import cv2
import os
import os.path
import sys

import rawpy

import camera
import clock
import database
import utils


raw_extensions = \
   ['.3fr',
    '.ari',
    '.arw',
    '.bay',
    '.braw',
    '.crw',
    '.cr2',
    '.cr3',
    '.cap',
    '.data',
    '.dcs',
    '.dcr',
    '.dng',
    '.drf',
    '.eip',
    '.erf',
    '.fff',
    '.gpr',
    '.iiq',
    '.k25',
    '.kdc',
    '.mdc',
    '.mef',
    '.mos',
    '.mrw',
    '.nef',
    '.nrw',
    '.obm',
    '.orf',
    '.pef',
    '.ptx',
    '.pxn',
    '.r3d',
    '.raf',
    '.raw',
    '.rwl',
    '.rw2',
    '.rwz',
    '.sr2',
    '.srf',
    '.srw',
    '.x3f']


# Parse the command-line arguments
description = 'Snapshot utility to grab images on-demand from the '
description += 'connected camera'
parser = argparse.ArgumentParser(description=description)

help_message = 'view each captured image on the display '
help_message += '[default is False]'
parser.add_argument('-d', '--display',
                    dest='display_captured_images',
                    action='store_true',
                    default=False,
                    help=help_message)

help_message = 'image scaling factor for display '
help_message += '[default is 0.25]'
parser.add_argument('-s', '--scaling-factor',
                    dest='scaling_factor',
                    type=float,
                    default=0.25,
                    help=help_message)

args = parser.parse_args()
display_captured_images = args.display_captured_images
scaling_factor = args.scaling_factor

# Pick up the latest parameters from the databases
msg = 'Picking up the latest settings from the station parameters database ...'
msg += '\n'
sys.stdout.write(msg)
sys.stdout.flush()
station_parameters = database.get_station_parameters()
station_parameters['stationName'] = utils.get_station_name()

# Check that the output directory exists and it writable
msg = 'Checking that the output directory exists and is writeable ...'
msg += '\n'
sys.stdout.write(msg)
sys.stdout.flush()
if not os.access(station_parameters['localDirectory'], os.W_OK):
   msg = '*** ERROR *** Output directory is not accessible for writing'
   msg += '\n'
   sys.stderr.write(msg)
   sys.stderr.flush()
   sys.exit()

# Form the output directory path
images_directory = \
   os.path.join(station_parameters['localDirectory'], 'snapshots')

# If it does not exist, create the output directory
if not os.path.isdir(images_directory):
   msg = 'Creating output directory ...'
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   os.mkdir(images_directory)

# Initialize the camera
camera_parameters = camera.initialize(station_parameters, verbose=True)

msg = '\n'
sys.stdout.write(msg)
sys.stdout.flush()

try:
   while True:
      # Wait for the user to press the RETURN key
      msg = 'Press <RETURN> to capture image | <Ctrl-C> to exit '
      k = input(msg)

      # Get current time [s] (UTC)
      iso8601_time_string = clock.iso8601_time_string_using_computer_clock()

      # Form the current basename for saving the image (this is
      # the basename, no extension, the extension is left to the
      # specific capture method)
      basename = iso8601_time_string.replace(':', '-').replace('.', '-')
      basename += '_'
      basename += station_parameters['stationName']
      local_basename = os.path.join(images_directory, basename)

      # Capture image and save it to the local disk
      capture_filepath = \
         camera.capture(station_parameters,
                        camera_parameters,
                        local_basename,
                        verbose=True)

      # If the capture was not successful, exit the script
      if capture_filepath == None:
         msg = 'Capture unsuccessful ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

         msg = '\n'
         msg += 'Turning off the camera ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         camera.close(station_parameters, camera_parameters, verbose=False)

         msg = 'Exiting ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         sys.exit()

      # Display captured image to the screen if desired
      if display_captured_images:
         extension = os.path.splitext(capture_filepath)[1].lower()

         # Check if the file is a known RAW file
         if extension in raw_extensions:
            msg = '... reading RAW image data'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
            raw = rawpy.imread(capture_filepath)

            msg = '... performing CFA interpolation'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
            rgb = raw.postprocess()
            im = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
         else:
            msg = '... reading common image data'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
            im = cv2.imread(capture_filepath)

         msg = '... scaling image for display'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         (height, width) = im.shape[:2]
         desired_dimensions = \
            (int(width * scaling_factor), int(height * scaling_factor))
         resized = cv2.resize(im, desired_dimensions)

         msg = '... displaying image'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         cv2.imshow(os.path.basename(capture_filepath), resized)

         msg = '\n'
         msg += 'Press <ESC> to continue'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         while True:
            k = cv2.waitKey(100)
            if (k & 0xff) == 27:   # <ESC> pressed
               cv2.destroyWindow(os.path.basename(capture_filepath))
               break

         msg = '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      continue

except KeyboardInterrupt:
   # Close the camera connection and power off the camera
   msg = '\n'
   msg += '\n'
   msg += 'Turning off the camera ...'
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   camera.close(station_parameters, camera_parameters, verbose=False)

   msg = 'Exiting ...'
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   sys.exit()
