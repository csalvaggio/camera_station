import picamera
import time

camera = picamera.PiCamera()

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
