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

   # Read the voltage(s)
   fieldNames = \
      ['voltmeter1Label',
       'voltmeter2Label',
       'voltmeter3Label',
       'voltmeter4Label',
       'voltmeter5Label',
       'voltmeter6Label',
       'voltmeter7Label',
       'voltmeter8Label']
   voltmeterLabels = []
   voltages = []
   for fieldName in fieldNames:
      if len(station_parameters[fieldName]):
         voltmeterLabels.append(station_parameters[fieldName])
      else:
         voltmeterLabels.append(None)
      voltmeter = battery.Voltmeter(fieldNames.index(fieldName))
      voltages.append(voltmeter.read(samples=16))
      voltmeter.close()

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
      msg = 'ISO8601 Time String'
      for voltmeterLabel in voltmeterLabels:
         if voltmeterLabel:
            msg += ','
            msg += voltmeterLabel
      msg += '\n'
      f.write(msg)
      f.close()

   if any(voltmeterLabels):
      # Display the voltage(s) to the standard output if desired
      if verbose:
         msg = 'Power conditions ...'
         msg += '\n'
         for voltmeterLabel in voltmeterLabels:
            if voltmeterLabel:
               msg += '   '
               msg += voltmeterLabel
               msg += ': '
               v = voltages[voltmeterLabels.index(voltmeterLabel)]
               msg += '{0:.2f}'.format(v) if v else '0.00'
               msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      # Write the current voltages to the log file
      if not iso8601_time_string:
         iso8601_time_string = \
            clock.iso8601_time_string_using_computer_clock()

      msg = iso8601_time_string
      for voltmeterLabel in voltmeterLabels:
         if voltmeterLabel:
            v = voltages[voltmeterLabels.index(voltmeterLabel)]
            msg += ','
            msg += '{0:.2f}'.format(v) if v else '0.00'
      msg += '\n'
      if os.path.isfile(log_filename):
         f = open(log_filename, 'a')
         f.write(msg)
         f.close()

      # Send a voltage warning SMS (if necessary) based on the first
      # voltage channel's value
      if alert:
         v = voltages[station_parameters['voltageWarningChannel'] - 1]
         if v < station_parameters['lowVoltageWarning'] or \
            v > station_parameters['highVoltageWarning']:   
            if verbose:   
               msg = 'Sending a voltage warning SMS ...'   
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
               utils.send_voltage_warning_sms(station_parameters)

            if verbose:
               msg = '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()

   return voltages
