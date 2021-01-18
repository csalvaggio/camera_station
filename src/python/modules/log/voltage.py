import os
import os.path
import sys

import clock
import battery
import utils

def voltage(station_parameters,
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
   log_type = 'voltage'
   log_basename = log_type + '_' + station_parameters['stationName'] + '.log'
   log_filename = os.path.join(logs_directory, log_basename)

   if create_new_log or not os.path.isfile(log_filename):
      if verbose:
         msg = 'Creating and initializing voltage log file ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      f = open(log_filename, 'w')
      msg = 'ISO8601 Time String,'
      msg += 'Battery [V],'
      msg += 'Regulator (7.6V) Output [V],'
      msg += 'Regulator (5V) Output [V]'
      msg += '\n'
      f.write(msg)
      f.close()

   # Log the source (battery) voltage
   voltmeter = battery.Voltmeter(0)
   source = voltmeter.read(samples=16)
   voltmeter.close()

   # Log the regulator (7.6V) output voltage
   voltmeter = battery.Voltmeter(1)
   regulator76 = voltmeter.read(samples=16)
   voltmeter.close()

   # Log the regulator (5V) output voltage
   voltmeter = battery.Voltmeter(2)
   regulator5 = voltmeter.read(samples=16)
   voltmeter.close()

   if source or regulator5 or regulator76:
      if verbose:
         msg = 'Power conditions ...'
         msg += '\n'
         msg += '   Battery: '
         msg += '{0:.2f} [V]'.format(source) if source else 'n/a'
         msg += '\n'
         msg += '   Regulator (7.6V) output: '
         msg += '{0:.2f} [V]'.format(regulator76) if regulator76 else 'n/a'
         msg += '\n'
         msg += '   Regulator (5V) output: '
         msg += '{0:.2f} [V]'.format(regulator5) if regulator5 else 'n/a'
         msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      if not iso8601_time_string:
         iso8601_time_string = \
            clock.iso8601_time_string_using_computer_clock()

      msg = iso8601_time_string
      msg += ','
      msg += '{0:.2f}'.format(source) if source else 'n/a'
      msg += ','
      msg += '{0:.2f}'.format(regulator76) if regulator76 else 'n/a'
      msg += ','
      msg += '{0:.2f}'.format(regulator5) if regulator5 else 'n/a'
      msg += '\n'
      if os.path.isfile(log_filename):
         f = open(log_filename, 'a')
         f.write(msg)
         f.close()

      if alert:
         # Send a source (battery) voltage warning SMS (if necessary)
         if source < station_parameters['lowVoltageWarning'] or \
            source > station_parameters['highVoltageWarning']:
            if verbose:
               msg = 'Sending a source (battery) voltage warning SMS ...'
               msg += '\n'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            utils.send_voltage_warning_sms(station_parameters)

   return voltage
