import sys

import gphoto2 as gp

items = \
   [
    'syncdatetimeutc',
    'syncdatetime',
    'reviewtime',
    'autopoweroff',
    'capturetarget',
    'imageformat',
    'iso',
    'whitebalance',
    'autoexposuremode',
    'drivemode',
    'picturestyle',
    'aperture',
    'shutterspeed',
    'meteringmode',
    'focusmode',
    'continuousaf',
    'exposurecompensation',
    'bracketmode'
   ]

separator = 72 * '-'

camera = gp.Camera()
camera.init()
config = camera.get_config()

for item in items:
   msg = separator
   msg += '\n'
   try:
      node = gp.check_result(gp.gp_widget_get_child_by_name(config, item))
      msg += 'Label: {0}'.format(node.get_label())
      msg += '\n'
      msg += 'Item: {0}'.format(item)
      msg += '\n'
      msg += separator
      msg += '\n'
      for idx in range(gp.gp_widget_count_choices(node)):
         choice = gp.check_result(gp.gp_widget_get_choice(node, idx))
         msg += '{0}'.format(choice)
         msg += '\n'
   except:
      msg += 'Label: n/a'
      msg += '\n'
      msg += 'Item: {0}   ***** NOT FOUND ON THIS CAMERA *****'.format(item)
      msg += '\n'
      msg += separator
      msg += '\n'

   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()

camera.exit()
