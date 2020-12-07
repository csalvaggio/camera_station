import sys

def set_parameters_for_rpi_camera(camera):
   if camera:
      # Set the resolution to the camera maximum
      camera.resolution = camera.MAX_RESOLUTION

      # iso [100, 200, 320, 400, 500, 640, 800] (0 <- automatic)
      camera.iso = 0

      # shutter_speed [0 <- auto-exposure] [microseconds]
      camera.shutter_speed = 0

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
      camera.exposure_mode = 'auto'

      # meter_mode
      #    (possible values obtained from PiCamera.METER_MODES attribute)
      #
      #    ['average',
      #     'spot',
      #     'backlit',
      #     'matrix']
      #
      camera.meter_mode = 'average'

      # brightness [0, 100]
      camera.brightness = 50

      # sharpness [-100, 100]
      camera.sharpness = 0

      # contrast [-100, 100]
      camera.contrast = 0

      # saturation [-100, 100]
      camera.saturation = 0

      # exposure_compensation [-25, 25] (each increment is 1/6 stop)
      camera.exposure_compensation = 0

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
      camera.awb_mode = 'auto'

      # rotation [0, 90, 180, 270]
      camera.rotation = 0

      # hflip [False / True]
      camera.hflip = False

      # vflip [False / True]
      camera.vflip = False

      # zoom (x, y, w, h)
      camera.zoom = (0, 0, 1, 1)

   else:
      msg = '*** ERROR *** Raspberry Pi camera object not defined'
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()






