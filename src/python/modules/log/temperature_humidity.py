import os
import os.path
import sys

import clock
import sensors
import utils

def temperature_humidity(station_parameters,
                         iso8601_time_string=None,
                         create_new_log=False,
                         alert=False,
                         verbose=False):

   # Create log file directory if it does not exist
   logs_directory = \
      os.path.join(station_parameters['localDirectory'], 'logs')
   if not os.path.isdir(logs_directory):
      if verbose:
         msg = 'Creating log file directory ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      os.mkdir(logs_directory)

   # Create log file if a new one has been requested or if it does not
   # currently exist
   log_type = 'temperature_humidity'
   log_basename = log_type + '_' + station_parameters['stationName'] + '.log'
   log_filename = os.path.join(logs_directory, log_basename)

   if create_new_log or not os.path.isfile(log_filename):
      if verbose:
         msg = 'Creating and initializing temperature/humidity log file ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      f = open(log_filename, 'w')
      msg = 'ISO8601 Time String'
      msg += ','
      msg += station_parameters['temperatureLabel']
      msg += ','
      msg += station_parameters['humidityLabel']
      msg += '\n'
      f.write(msg)
      f.close()

   # Log the enclosure's interior temperature and humidity
   readings = \
      sensors.temperature_humidity(temperature_units='f', verbose=verbose)
   if readings:
      temperature, humidity = readings
   else:
      temperature = None
      humidity = None

   if temperature and humidity:
      if verbose:
         msg = 'Enclosure environmental conditions ...'
         msg += '\n'
         msg += '   '
         msg += station_parameters['temperatureLabel']
         msg += ': '
         msg += '{0:.1f}'.format(temperature)
         msg += '\n'
         msg += '   '
         msg += station_parameters['humidityLabel']
         msg += ': '
         msg += '{0:.1f}'.format(humidity)
         msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      if not iso8601_time_string:
         iso8601_time_string = \
            clock.iso8601_time_string_using_computer_clock()

      msg = iso8601_time_string
      msg += ','
      msg += '{0:.1f}'.format(temperature)
      msg += ','
      msg += '{0:.1f}'.format(humidity)
      msg += '\n'
      if os.path.isfile(log_filename):
         f = open(log_filename, 'a')
         f.write(msg)
         f.close()

      if alert:
         # Send a temperature warning SMS (if necessary)
         if temperature < station_parameters['lowTemperatureWarning'] or \
            temperature > station_parameters['highTemperatureWarning']:
            if verbose:
               msg = 'Sending a temperature warning SMS ...'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            if station_parameters['doNotDisturb']:
               if verbose:
                  msg = 'Skipping ... DO NOT DISTURB SETTING IS ACTIVATED'
                  msg += '\n'
                  sys.stdout.write(msg)
                  sys.stdout.flush()
            else:
               utils.send_temperature_warning_sms(station_parameters)

            if verbose:
               msg = '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()

         # Send a humidity warning SMS (if necessary)
         if humidity < station_parameters['lowHumidityWarning'] or \
            humidity > station_parameters['highHumidityWarning']:
            if verbose:
               msg = 'Sending a humidity warning SMS ...'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            if station_parameters['doNotDisturb']:
               if verbose:
                  msg = 'Skipping ... DO NOT DISTURB SETTING IS ACTIVATED'
                  msg += '\n'
                  sys.stdout.write(msg)
                  sys.stdout.flush()
            else:
               utils.send_humidity_warning_sms(station_parameters)

            if verbose:
               msg = '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()

   return temperature, humidity
