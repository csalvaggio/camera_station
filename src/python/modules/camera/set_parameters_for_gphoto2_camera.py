import sys

import gphoto2 as gp

def set_parameters_for_gphoto2_camera(station_parameters, parameters):
   if parameters['connection']:
      # THE FOLLOWING HAS NOT BEEN TESTED
      ## Burst number
      #config = parameters['connection'].get_config(context)
      #node = config.get_child_by_name("burstnumber")
      #node.set_value(5)
      #parameters['connection'].set_config(config, context)
      #
      # Use "gphoto2 --list-config" with a camera attached to get a list
      # of configurable parameters?????
      #
      pass
   else:
      msg = '*** ERROR *** gPhoto2 camera object not defined'
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()
