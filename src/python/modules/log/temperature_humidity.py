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
   log_directory = \
      os.path.join(station_parameters['localDirectory'], 'logs')
   if not os.path.isdir(log_directory):
      if verbose:
         msg = 'Creating log file directory ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      os.mkdir(log_directory)

   # Create log file if a new one has been requested or if it does not
   # currently exist
   log_type = 'temperature_humidity'
   log_basename = log_type + '_' + station_parameters['stationName'] + '.log'
   log_filename = os.path.join(log_directory, log_basename)

   if create_new_log or not os.path.isfile(log_filename):
      if verbose:
         msg = 'Creating and initializing temperature/humidity log file ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      f = open(log_filename, 'w')
      msg = 'ISO8601 Time String,'
      msg += 'Temperature [F],'
      msg += 'Relative Humidity [%]'
      msg += '\n'
      f.write(msg)
      f.close()

   # Log the enclosure's interior temperature and relative humidity
   readings = \
      sensors.temperature_humidity(temperature_units='f', verbose=verbose)
   if readings:
      temperature, humidity = readings
   else:
      temperature = None
      humidity = None

   if temperature and humidity:
      if verbose:
         msg = 'Enclosure\'s environmental conditions: '
         msg += '\n'
         msg += '   Temperature: {0:.1f} [F]'.format(temperature)
         msg += '\n'
         msg += '   Humidity: {0:.1f} [%]'.format(humidity)
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
      if os.path.isfile(temperature_humidity_log_filename):
         f = open(temperature_humidity_log_filename, 'a')
         f.write(msg)
         f.close()

      if alert:
         # Send a temperature warning SMS (if necessary)
         if temperature < station_parameters['lowTemperatureWarning'] or \
            temperature > station_parameters['highTemperatureWarning']:
            if verbose:
               msg = 'Sending a temperature warning SMS ...'
               msg += '\n'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            utils.send_temperature_warning_sms(station_parameters)

         # Send a humidity warning SMS (if necessary)
         if humidity < station_parameters['lowHumidityWarning'] or \
            humidity > station_parameters['highHumidityWarning']:
            if verbose:
               msg = 'Sending a humidity warning SMS ...'
               msg += '\n'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            utils.send_humidity_warning_sms(station_parameters)

   return temperature, humidity
