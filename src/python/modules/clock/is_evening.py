import clock
import datetime

def is_evening(iso8601_time_string, longitude, latitude):
   sunrise, sunset = \
      clock.sunrise_sunset(iso8601_time_string, longitude, latitude)

   Y = int(sunrise[0:4])
   M = int(sunrise[5:7])
   D = int(sunrise[8:10])
   h = int(sunrise[11:13])
   m = int(sunrise[14:16])
   s = int(sunrise[17:19])
   S = int(sunrise[20:23]) * 1000
   sunup = datetime.datetime(Y, M, D, h, m, s, S)

   Y = int(sunset[0:4])
   M = int(sunset[5:7])
   D = int(sunset[8:10])
   h = int(sunset[11:13])
   m = int(sunset[14:16])
   s = int(sunset[17:19])
   S = int(sunset[20:23]) * 1000
   sundown = datetime.datetime(Y, M, D, h, m, s, S)

   Y = int(iso8601_time_string[0:4])
   M = int(iso8601_time_string[5:7])
   D = int(iso8601_time_string[8:10])
   h = int(iso8601_time_string[11:13])
   m = int(iso8601_time_string[14:16])
   s = int(iso8601_time_string[17:19])
   S = int(iso8601_time_string[20:23]) * 1000
   current = datetime.datetime(Y, M, D, h, m, s, S)

   # If the evening spans midnight
   if sundown > sunup:
      # and the current time is before midnight
      if current > sundown:
         # then sunrise is on the next day
         sunup += datetime.timedelta(days=1)
      elif current < sunup:
         # then sunset is on the previous day
         sundown -= datetime.timedelta(days=1)

   return sundown < current and current < sunup



if __name__ == '__main__':
   import clock

   iso8601_time_string  = clock.iso8601_time_string_using_computer_clock()

   # Rochester, NY, USA
   longitude = -77.6088
   latitude = 43.1566

   msg = 'Current time: {0}'.format(iso8601_time_string)
   print(msg)
   msg = 'Latitude: {0}'.format(latitude)
   print(msg)
   msg = 'Longitude: {0}'.format(longitude)
   print(msg)
   msg = ''
   print(msg)

   sunrise, sunset = \
      clock.sunrise_sunset(iso8601_time_string, longitude, latitude)

   msg = 'Sunrise: {0}'.format(sunrise)
   print(msg)
   msg = 'Sunset: {0}'.format(sunset)
   print(msg)
   msg = ''
   print(msg)

   if clock.is_evening(iso8601_time_string, longitude, latitude):
      msg = 'Current time IS the evening'
      print(msg)
   else:
      msg = 'Current time IS NOT the evening'
      print(msg)
