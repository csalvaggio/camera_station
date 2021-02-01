import copy
import os.path
import sys
import time

import gphoto2 as gp

def get_camera_config(camera):
   config = camera.get_config()
   config_dictionary = {}
   for category_index in range(config.count_children()):
      category = config.get_child(category_index)
      config_dictionary[category.get_name()] = {}
      for item_index in range(category.count_children()):
         item = category.get_child(item_index)
         config_dictionary[category.get_name()][item.get_name()] = \
            {}
         config_dictionary[category.get_name()][item.get_name()]['label'] = \
            item.get_label()
         config_dictionary[category.get_name()][item.get_name()]['value'] = \
            item.get_value()
   return config_dictionary

def set_camera_config(camera, config_dictionary):
   config = camera.get_config()
   for category in config_dictionary:
      if category == 'other':
         continue
      for item in config_dictionary[category]:
         node = config.get_child_by_name(item)
         if not isinstance(config_dictionary[category][item]['value'],
                           type(None)):
            node.set_value(config_dictionary[category][item]['value'])
   camera.set_config(config)

def print_camera_config(config_dictionary):
   for category in config_dictionary:
      msg = '{0}'.format(category)
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
      for item in config_dictionary[category]:
         msg = '   {0}'.format(item)
         msg += ' {0}:'.format(type(config_dictionary[category][item]['value']))
         msg += '  {0}'.format(config_dictionary[category][item]['value'])
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()



if __name__ == '__main__':

   camera = gp.Camera()
   camera.init()

   separator = 72 * '-' + '\n'

   msg = separator
   msg += 'BEFORE CONFIGURATION UPDATE'
   msg += '\n'
   msg += separator
   sys.stdout.write(msg)
   sys.stdout.flush()
   config_dictionary = get_camera_config(camera)
   original_config_dictionary = copy.deepcopy(config_dictionary)
   print_camera_config(config_dictionary)
   time.sleep(5)

   msg = separator
   msg += 'PERFORMING CONFIGURATION UPDATE'
   msg += '\n'
   msg += separator
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   # imageformat <class 'str'>
   config_dictionary['imgsettings']['imageformat']['value'] = 'Large Fine JPEG'
   # iso <class 'str'>
   config_dictionary['imgsettings']['iso']['value'] = '800'
   # whitebalance <class 'str'>
   config_dictionary['imgsettings']['whitebalance']['value'] = 'Daylight'
   # autoexposuremode <class 'str'>
   config_dictionary['capturesettings']['autoexposuremode']['value'] = 'TV'
   # picturestyle <class 'str'>
   config_dictionary['capturesettings']['picturestyle']['value'] = 'Landscape'
   # aperture <class 'str'>
   config_dictionary['capturesettings']['aperture']['value'] = 'implicit auto'
   # shutterspeed <class 'str'>
   config_dictionary['capturesettings']['shutterspeed']['value'] = '1/400'
   # meteringmode <class 'str'>
   config_dictionary['capturesettings']['meteringmode']['value'] = 'Spot'
   set_camera_config(camera, config_dictionary)
   time.sleep(5)

   msg = separator
   msg += 'AFTER CONFIGURATION UPDATE'
   msg += '\n'
   msg += separator
   sys.stdout.write(msg)
   sys.stdout.flush()
   config_dictionary = get_camera_config(camera)
   print_camera_config(config_dictionary)
   time.sleep(5)

   msg = separator
   msg += 'CAPTURING IMAGE'
   msg += '\n'
   msg += separator
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   camera_filepath = camera.capture(gp.GP_CAPTURE_IMAGE)
   camera_file = camera.file_get(camera_filepath.folder,
                                 camera_filepath.name,
                                 gp.GP_FILE_TYPE_NORMAL)
   extension = os.path.splitext(camera_filepath.name)[1].lower()
   home = os.path.expanduser('~')
   filename = 'image' + extension
   local_filepath = os.path.join(home, filename)
   camera_file.save(local_filepath)
   camera.file_delete(camera_filepath.folder, camera_filepath.name)
   time.sleep(5)

   msg = separator
   msg += 'RESTORING ORIGINAL CONFIGURATION'
   msg += '\n'
   msg += separator
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   # imageformat <class 'str'>
   config_dictionary['imgsettings']['imageformat']['value'] = \
      original_config_dictionary['imgsettings']['imageformat']['value']
   # iso <class 'str'>
   config_dictionary['imgsettings']['iso']['value'] = \
      original_config_dictionary['imgsettings']['iso']['value']
   # whitebalance <class 'str'>
   config_dictionary['imgsettings']['whitebalance']['value'] = \
      original_config_dictionary['imgsettings']['whitebalance']['value']
   # autoexposuremode <class 'str'>
   config_dictionary['capturesettings']['autoexposuremode']['value'] = \
      original_config_dictionary['capturesettings']['autoexposuremode']['value']
   # picturestyle <class 'str'>
   config_dictionary['capturesettings']['picturestyle']['value'] = \
      original_config_dictionary['capturesettings']['picturestyle']['value']
   # aperture <class 'str'>
   config_dictionary['capturesettings']['aperture']['value'] = \
      original_config_dictionary['capturesettings']['aperture']['value']
   # shutterspeed <class 'str'>
   config_dictionary['capturesettings']['shutterspeed']['value'] = \
      original_config_dictionary['capturesettings']['shutterspeed']['value']
   # meteringmode <class 'str'>
   config_dictionary['capturesettings']['meteringmode']['value'] = \
      original_config_dictionary['capturesettings']['meteringmode']['value']
   set_camera_config(camera, config_dictionary)
   time.sleep(5)

   msg = separator
   msg += 'AFTER RESTORING CONFIGURATION'
   msg += '\n'
   msg += separator
   sys.stdout.write(msg)
   sys.stdout.flush()
   config_dictionary = get_camera_config(camera)
   print_camera_config(config_dictionary)

   camera.exit()
