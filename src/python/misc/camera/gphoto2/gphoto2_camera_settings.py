import copy
import os.path
import sys

import gphoto2 as gp

def get_camera_config(camera):
   config = camera.get_config()
   d = {}
   for category_index in range(config.count_children()):
      category = config.get_child(category_index)
      d[category.get_name()] = {}
      for item_index in range(category.count_children()):
         item = category.get_child(item_index)
         d[category.get_name()][item.get_name()] = {}
         d[category.get_name()][item.get_name()]['label'] = item.get_label()
         d[category.get_name()][item.get_name()]['value'] = item.get_value()
   return d

def set_camera_config(camera, config):
   c = camera.get_config()
   for category in config:
      if category == 'other':
         continue
      for item in config[category]:
         node = c.get_child_by_name(item)
         if not isinstance(config[category][item]['value'], type(None)):
            node.set_value(config[category][item]['value'])
   camera.set_config(c)

def print_camera_config(config):
   for category in config:
      msg = '{0}'.format(category)
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
      for item in config[category]:
         msg = '   {0} '.format(item)
         msg += '{0}:  '.format(type(config[category][item]['value']))
         msg += '{0}'.format(config[category][item]['value'])
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
   config = get_camera_config(camera)
   print_camera_config(config)

   msg = separator
   msg += 'PERFORMING CONFIGURATION UPDATE'
   msg += '\n'
   msg += separator
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   # imageformat <class 'str'>
   config['imgsettings']['imageformat']['value'] = 'Large Fine JPEG'
   # iso <class 'str'>
   config['imgsettings']['iso']['value'] = '800'
   # whitebalance <class 'str'>
   #config['imgsettings']['whitebalance']['value'] = 'Daylight'
   # autoexposuremode <class 'str'>
   config['capturesettings']['autoexposuremode']['value'] = 'Manual'
   # picturestyle <class 'str'>
   #config['capturesettings']['picturestyle']['value'] = 'Landscape'
   # aperture <class 'str'>
   config['capturesettings']['aperture']['value'] = '8'
   # shutterspeed <class 'str'>
   config['capturesettings']['shutterspeed']['value'] = '1/350'
   # meteringmode <class 'str'>
   #config['capturesettings']['meteringmode']['value'] = 'Spot'
   set_camera_config(camera, config)

   msg = separator
   msg += 'AFTER CONFIGURATION UPDATE'
   msg += '\n'
   msg += separator
   sys.stdout.write(msg)
   sys.stdout.flush()
   config = get_camera_config(camera)
   print_camera_config(config)

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

   msg = separator
   msg += 'RESTORING ORIGINAL CONFIGURATION'
   msg += '\n'
   msg += separator
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   # imageformat <class 'str'>
   config['imgsettings']['imageformat']['value'] = 'RAW'
   # iso <class 'str'>
   config['imgsettings']['iso']['value'] = '100'
   # whitebalance <class 'str'>
   #config['imgsettings']['whitebalance']['value'] = 'Auto'
   # autoexposuremode <class 'str'>
   config['capturesettings']['autoexposuremode']['value'] = 'AV'
   # picturestyle <class 'str'>
   #config['capturesettings']['picturestyle']['value'] = 'Standard'
   # aperture <class 'str'>
   config['capturesettings']['aperture']['value'] = '4'
   # shutterspeed <class 'str'>
   config['capturesettings']['shutterspeed']['value'] = 'auto'
   # meteringmode <class 'str'>
   #config['capturesettings']['meteringmode']['value'] = 'Evaluative'
   set_camera_config(camera, config)

   msg = separator
   msg += 'AFTER RESTORING CONFIGURATION'
   msg += '\n'
   msg += separator
   sys.stdout.write(msg)
   sys.stdout.flush()
   config = get_camera_config(camera)
   print_camera_config(config)

   camera.exit()
