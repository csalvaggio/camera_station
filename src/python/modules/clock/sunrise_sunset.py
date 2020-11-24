import astral
import astral.sun
import datetime

def sunrise_sunset(iso8601_time_string, longitude, latitude):
   """
   title::
      sunrise_sunset

   description::
      This method will determine the sunrise/sunset times for the date
      in the provided time string at the longitude and latitude speciied.

   attributes::
      iso8601_time_string
         An ISO8601-formatted time string containing the date for which 
         the sunrise and sunset times will be determined.  The time string
         has the form 2020-11-15T00:19:49.511Z in UTC.
      longitude
         The longitude (decimal format) for the location at which to
         determine the sunrise and sunset times.  Longitude is specified
         in the range [-180, 180] (Eastern longitudes are positive).
      latitude
         The latitude (decimal format) for the location at which to
         determine the sunrise and sunset times.  Latitude is specified
         in the range [-90, 90] (Northern latitudes are positive).

   returns::
      A two-element tuple containing the ISO8601 time strings representing
      the sunrise and sunset times, respectively [UTC].

   author::
      Carl Salvaggio

   copyright::
      Copyright (C) 2020, Rochester Institute of Technology

   license::
      GPL

   version::
      1.0.0

   disclaimer::
      This source code is provided "as is" and without warranties as to 
      performance or merchantability. The author and/or distributors of 
      this source code may have made statements about this source code. 
      Any such statements do not constitute warranties and shall not be 
      relied on by the user in deciding whether to use this source code.
      
      This source code is provided without any express or implied warranties 
      whatsoever. Because of the diversity of conditions and hardware under 
      which this source code may be used, no warranty of fitness for a 
      particular purpose is offered. The user is advised to test the source 
      code thoroughly before relying on it. The user must assume the entire 
      risk of using the source code.
   """

   # Parse the required values from the ISO8601 time string
   Y = int(iso8601_time_string[0:4])
   M = int(iso8601_time_string[5:7])
   D = int(iso8601_time_string[8:10])

   # Specify the Astral location information object
   location = \
      astral.LocationInfo(None,
                          None,
                          None,
                          latitude,
                          longitude)

   # Compute the solar positional parameters for the specified date/location
   solar_parameters = \
      astral.sun.sun(location.observer, date=datetime.date(Y, M, D))

   sunrise = str(solar_parameters["sunrise"])[0:23]
   sunset = str(solar_parameters["sunset"])[0:23]
   sunrise = sunrise[:10] + 'T' + sunrise[11:] + 'Z'
   sunset = sunset[:10] + 'T' + sunset[11:] + 'Z'

   return sunrise, sunset



if __name__ == '__main__':
   import clock

   iso8601_time_string = \
      clock.iso8601_time_string_using_computer_clock()

   # Rochester, NY, USA
   longitude = -77.6088
   latitude = 43.1566
   sunrise, sunset = \
      clock.sunrise_sunset(iso8601_time_string, longitude, latitude)

   msg = 'Current time: {0}'.format(iso8601_time_string)
   print(msg)
   msg = 'Sunrise:      {0}'.format(sunrise)
   print(msg)
   msg = 'Sunset:       {0}'.format(sunset)
   print(msg)
