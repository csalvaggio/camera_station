import os
import os.path
import sys

import clock
import battery
import utils

def battery_voltage(station_parameters,
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
   log_type = 'battery_voltage'
   log_basename = log_type + '_' + station_parameters['stationName'] + '.log'
   log_filename = os.path.join(log_directory, log_basename)

   if create_new_log or not os.path.isfile(log_filename):
      if verbose:
         msg = 'Creating and initializing battery voltage log file ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      f = open(log_filename, 'w')
      msg = 'ISO8601 Time String,'
      msg += 'Battery Voltage [V]'
      msg += '\n'
      f.write(msg)
      f.close()

   # Log the battery voltage
   voltmeter = battery.Voltmeter(0)
   voltage = voltmeter.read(samples=16)
   voltmeter.close()

   if voltage:
      if verbose:
         msg = 'Power conditions: '
         msg += '\n'
         msg += '   Battery voltage: {0:.2f} [V]'.format(voltage)
         msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      if not iso8601_time_string:
         iso8601_time_string = \
            clock.iso8601_time_string_using_computer_clock()

      msg = iso8601_time_string
      msg += ','
      msg += '{0:.2f}'.format(voltage)
      msg += '\n'
      if os.path.isfile(log_filename):
         f = open(log_filename, 'a')
         f.write(msg)
         f.close()

      if alert:
         # Send a battery voltage warning SMS (if necessary)
         if voltage < station_parameters['lowVoltageWarning'] or \
            voltage > station_parameters['highVoltageWarning']:
            if verbose:
               msg = 'Sending a battery voltage warning SMS ...'
               msg += '\n'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            utils.send_battery_voltage_warning_sms(station_parameters)

   return voltage
