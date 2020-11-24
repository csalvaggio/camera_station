import picamera

camera = picamera.PiCamera()

msg = 'camera.brightness = '
msg += '{0}'.format(camera.brightness)
msg += ' (0 to 100)'
print(msg)

msg = 'camera.sharpness = '
msg += '{0}'.format(camera.sharpness)
msg += ' (-100 to 100)'
print(msg)

msg = 'camera.contrast = '
msg += '{0}'.format(camera.contrast)
msg += ' (-100 to 100)'
print(msg)

msg = 'camera.saturation = '
msg += '{0}'.format(camera.saturation)
msg += ' (-100 to 100)'
print(msg)

msg = 'camera.iso = '
msg += '{0}'.format(camera.iso)
msg += ' (100 to 800) [0 is automatic]'
print(msg)

msg = 'camera.shutter_speed = '
msg += '{0} [ms]'.format(camera.shutter_speed)
msg += ' [0 is automatic]'
print(msg)

msg = 'camera.exposure_compensation = '
msg += '{0}'.format(camera.exposure_compensation)
msg += ' (-25 to 25)'
print(msg)

msg = 'camera.exposure_mode = '
msg += '{0}'.format(camera.exposure_mode)
print(msg)

msg = 'camera.meter_mode = '
msg += '{0}'.format(camera.meter_mode)
print(msg)

msg = 'camera.awb_mode = '
msg += '{0}'.format(camera.awb_mode)
print(msg)

msg = 'camera.rotation = '
msg += '{0}'.format(camera.rotation)
print(msg)

msg = 'camera.hflip = '
msg += '{0}'.format(camera.hflip)
print(msg)

msg = 'camera.vflip = '
msg += '{0}'.format(camera.vflip)
print(msg)

msg = 'camera.crop = '
msg += '{0}'.format(camera.crop)
print(msg)

msg = 'camera.resolution = '
msg += '{0}'.format(camera.resolution)
print(msg)

msg = 'camera.image_effect = '
msg += '{0}'.format(camera.image_effect)
print(msg)

msg = 'camera.color_effects = '
msg += '{0}'.format(camera.color_effects)
print(msg)

msg = 'camera.exif_tags = '
msg += '{0}'.format(camera.exif_tags)
print(msg)

camera.close()
