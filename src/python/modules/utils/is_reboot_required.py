import os
import os.path

def is_reboot_required(station_parameters):
   reboot_required = False

   if station_parameters['imageFileCountToExceedForReboot'] > 0:
      images_directory = \
         os.path.join(station_parameters['localDirectory'], 'images')
      images_directory_listing = sorted(os.listdir(images_directory))
      image_filenames = []
      for image_filename in images_directory_listing:
         image_path = os.path.join(images_directory, image_filename)
         if os.path.isfile(image_path):
            image_filenames.append(image_path)
      if len(image_filenames) > \
            station_parameters['imageFileCountToExceedForReboot']:
         reboot_required = True

   reboot_required_file = '/tmp/reboot_required'
   if reboot_required:
      cmd = 'touch ' + reboot_required_file
      os.system(cmd)
   else:
      cmd = 'rm -f ' + reboot_required_file
      os.system(cmd)

   return reboot_required



if __name__ == '__main__':
   import sys
   import database
   import utils

   # Get database parameters
   station_parameters = database.get_station_parameters()

   # Check if a system reboot is required
   reboot_required = utils.is_reboot_required(station_parameters)

   msg = 'Reboot '
   if reboot_required:
      msg += 'IS '
   else:
      msg += 'IS NOT '
   msg += 'required'
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
