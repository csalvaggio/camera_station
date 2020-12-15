import sys

import picamera

def set_parameters_for_rpi_camera(parameters):
   if parameters['connection']:
      # brightness [0, 100]
      if parameters['brightness'] < 0 or parameters['brightness'] > 100:
         msg = 'Camera brightness setting out of range'
         raise ValueError(msg)
      parameters['connection'].brightness = parameters['brightness']

      # sharpness [-100, 100]
      if parameters['sharpness'] < -100 or parameters['sharpness'] > 100:
         msg = 'Camera sharpness setting out of range'
         raise ValueError(msg)
      parameters['connection'].sharpness = parameters['sharpness']

      # contrast [-100, 100]
      if parameters['contrast'] < -100 or parameters['contrast'] > 100:
         msg = 'Camera contrast setting out of range'
         raise ValueError(msg)
      parameters['connection'].contrast = parameters['contrast']

      # saturation [-100, 100]
      if parameters['saturation'] < -100 or parameters['saturation'] > 100:
         msg = 'Camera saturation setting out of range'
         raise ValueError(msg)
      parameters['connection'].saturation = parameters['saturation']

      # iso [100, 200, 320, 400, 500, 640, 800] (0 <- automatic)
      if parameters['ISO'] in [0, 100, 200, 320, 400, 500, 640, 800]:
         parameters['connection'].iso = parameters['ISO']
      else:
         msg = 'Camera ISO is not a valid value'
         raise ValueError(msg)

      # shutter_speed [0 <- auto-exposure] [microseconds]
      if parameters['shutterSpeed'] < 0:
         msg = 'Camera shutter speed must be a positive value'
         raise ValueError(msg)
      parameters['connection'].shutter_speed = parameters['shutterSpeed']

      # exposure_compensation [-25, 25] (each increment is 1/6 stop)
      if parameters['exposureCompensation'] < -25 or \
                    parameters['exposureCompensation'] > 25:
         msg = 'Camera exposure compensation setting out of range'
         raise ValueError(msg)
      parameters['connection'].exposure_compensation = \
         parameters['exposureCompensation']

      # exposure_mode
      #    (possible values obtained from PiCamera.EXPOSURE_MODES attribute)
      #
      #    ['off',
      #     'auto',
      #     'night',
      #     'nightpreview',
      #     'backlight',
      #     'spotlight',
      #     'sports',
      #     'snow',
      #     'beach',
      #     'verylong',
      #     'fixedfps',
      #     'antishake',
      #     'fireworks']
      #
      if parameters['exposureMode'] in picamera.PiCamera.EXPOSURE_MODES.keys():
         parameters['connection'].exposure_mode = parameters['exposureMode']
      else:
         msg = 'Camera exposure mode is not a valid value'
         raise ValueError(msg)

      # meter_mode
      #    (possible values obtained from PiCamera.METER_MODES attribute)
      #
      #    ['average',
      #     'spot',
      #     'backlit',
      #     'matrix']
      #
      if parameters['meterMode'] in picamera.PiCamera.METER_MODES.keys():
         parameters['connection'].meter_mode = parameters['meterMode']
      else:
         msg = 'Camera meter mode is not a valid value'
         raise ValueError(msg)

      # awb_mode
      #    (possible values obtained from PiCamera.AWB_MODES attribute)
      #
      #    ['off'.
      #     'auto',
      #     'sunlight',
      #     'cloudy',
      #     'shade',
      #     'tungsten',
      #     'fluorescent',
      #     'incandescent',
      #     'flash',
      #     'horizon']
      #
      if parameters['awbMode'] in picamera.PiCamera.AWB_MODES.keys():
         parameters['connection'].awb_mode = parameters['awbMode']
      else:
         msg = 'Camera AWB mode is not a valid value'
         raise ValueError(msg)

      # rotation [0, 90, 180, 270]
      if parameters['rotation'] in [0, 90, 180, 270]:
         parameters['connection'].rotation = parameters['rotation']
      else:
         msg = 'Camera rotation is not a valid value'
         raise ValueError(msg)

      # hflip [False / True]
      parameters['connection'].hflip = True if parameters['hFlip'] else False

      # vflip [False / True]
      parameters['connection'].vflip = True if parameters['vFlip'] else False

      # zoom (x, y, w, h)
      if (parameters['cropNormalizedULRow'] < 0 or \
          parameters['cropNormalizedULRow'] > 1):
         msg = 'Camera crop/zoom value for UL row is out of range'
         raise ValueError(msg)
      if (parameters['cropNormalizedULColumn'] < 0 or \
          parameters['cropNormalizedULColumn'] > 1):
         msg = 'Camera crop/zoom value for UL column is out of range'
         raise ValueError(msg)
      if (parameters['cropNormalizedWidth'] < 0 or \
          parameters['cropNormalizedWidth'] > 1):
         msg = 'Camera crop/zoom value for width is out of range'
         raise ValueError(msg)
      if (parameters['cropNormalizedHeight'] < 0 or \
          parameters['cropNormalizedHeight'] > 1):
         msg = 'Camera crop/zoom value for height is out of range'
         raise ValueError(msg)
      parameters['connection'].zoom = (parameters['cropNormalizedULRow'],
                                       parameters['cropNormalizedULColumn'],
                                       parameters['cropNormalizedWidth'],
                                       parameters['cropNormalizedHeight'])

      # resolution (w, h)
      parameters['connection'].resolution = (parameters['resolutionColumns'],
                                             parameters['resolutionRows'])

   else:
      msg = '*** ERROR *** Raspberry Pi camera object not defined'
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()
