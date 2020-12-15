import sys

import gphoto2 as gp

def set_config(config, parameters, parameter, field_name, error_message):
   node = gp.check_result(gp.gp_widget_get_child_by_name(config, parameter))
   choices = []
   for idx in range(gp.gp_widget_count_choices(node)):
      choice = gp.check_result(gp.gp_widget_get_choice(node, idx))
      choices.append(choice)
   if parameters[field_name] in choices:
      try:
         node.set_value(parameters[field_name])
         parameters['connection'].set_config(config)
      except:
         msg = 'A problem occurred when setting camera configuration: '
         msg += '{0}'.format(parameter)
         raise RuntimeError(msg)
   else:
      raise ValueError(error_message)


##############################   IMPORTANT NOTE   ##############################
#   Parameters that are commented out are available on the Canon EOS Rebel
#   Xsi (450D) but not available on the Canon EOS M100
################################################################################
def set_parameters_for_gphoto2_camera(parameters):
   if parameters['connection']:
      if parameters['configurable']:
         config = parameters['connection'].get_config()

         parameter = 'imageformat'
         field_name = 'imageFormat'
         error_message = \
            'Specified image format is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'iso'
         field_name = 'ISO'
         error_message = \
            'Specified ISO is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         #parameter = 'whitebalance'
         #field_name = 'awbMode'
         #error_message = \
         #   'Specified white balance is not a valid option for this camera'
         #set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'autoexposuremode'
         field_name = 'exposureMode'
         error_message = \
            'Specified auto exposure mode is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         #parameter = 'picturestyle'
         #field_name = 'pictureStyle'
         #error_message = \
         #   'Specified picture style is not a valid option for this camera'
         #set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'aperture'
         field_name = 'aperture'
         error_message = \
            'Specified aperture (F-stop) is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         parameter = 'shutterspeed'
         field_name = 'shutterSpeed'
         error_message = \
            'Specified shutter speed is not a valid option for this camera'
         set_config(config, parameters, parameter, field_name, error_message)

         #parameter = 'meteringmode'
         #field_name = 'meterMode'
         #error_message = \
         #   'Specified metering mode is not a valid option for this camera'
         #set_config(config, parameters, parameter, field_name, error_message)

   else:
      msg = '*** ERROR *** gPhoto2 camera object not defined'
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()
