import cv2
import io
import numpy
import picamera
import time

stream = io.BytesIO()

camera = picamera.PiCamera()

camera.resolution = camera.MAX_RESOLUTION

time.sleep(5)
camera.capture(stream, format='jpeg')
#data = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
data = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)
im = cv2.imdecode(data, 1)

print('Image Size: {0}'.format(im.shape))

cv2.imshow('Captured Image', im)
cv2.waitKey(0)
