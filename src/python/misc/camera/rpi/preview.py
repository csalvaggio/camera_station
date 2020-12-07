import picamera
import time

from set_parameters_for_rpi_camera import set_parameters_for_rpi_camera

camera = picamera.PiCamera()

set_parameters_for_rpi_camera(camera)

try:
   print("Starting camera preview ...")
   camera.start_preview()
   print("Started")
   print("<Ctrl-C> to exit preview ...")
   while True:
      time.sleep(1)

except KeyboardInterrupt:
   print("\nStopping camera preview ...")
   camera.stop_preview()
   print("Stopped")
   print("Closing camera ...")
   camera.close()
   print("Closed")
