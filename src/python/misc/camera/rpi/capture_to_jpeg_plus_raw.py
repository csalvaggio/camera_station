import picamera
import pydng.core
import time

filename = '/home/pi/image.jpg'
use_lossless_jpeg_compression = True

camera = picamera.PiCamera()

camera.resolution = camera.MAX_RESOLUTION

time.sleep(5)

# Capture an image and save it to a JPEG file with the raw Bayer image in
# the JPEG metadata
camera.capture(filename, format='jpeg', bayer=True)
camera.close()

# Extract the raw Bayer image from the JPEG metadata and save it to a
# digital negative (DNG) file
d = pydng.core.RPICAM2DNG()
d.convert(filename, compress=use_lossless_jpeg_compression)
