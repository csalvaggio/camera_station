def close(station_parameters, camera_parameters):
   if station_parameters['cameraType'] == 'rpi':
      # Raspberry Pi camera
      camera_parameters['connection'].close()
   elif station_parameters['cameraType'] == 'gPhoto2':
      # gPhoto2 camera
      camera_parameters['connection'].exit()
