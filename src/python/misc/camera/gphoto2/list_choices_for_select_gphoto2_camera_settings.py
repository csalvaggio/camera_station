import sys

import gphoto2 as gp

items = \
   ['syncdatetime',
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
    'meteringmode']

camera = gp.Camera()
camera.init()
config = camera.get_config()

for item in items:
   node = \
      gp.check_result(gp.gp_widget_get_child_by_name(config, item))
   msg = 72 * '-'
   msg += '\n'
   msg += 'Label: {0}'.format(node.get_label())
   msg += '\n'
   msg += 'Item: {0}'.format(item)
   msg += '\n'
   msg += 72 * '-'
   msg += '\n'
   for idx in range(gp.gp_widget_count_choices(node)):
      choice = gp.check_result(gp.gp_widget_get_choice(node, idx))
      msg += '{0}'.format(choice)
      msg += '\n'
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()

camera.exit()
