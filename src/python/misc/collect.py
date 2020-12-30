import argparse
import os
import os.path
import sys
import time

import pydng.core

import camera
import clock
import database
import utils


# Parse the command-line arguments
description = 'Camera station collection control script'
parser = argparse.ArgumentParser(description=description)

help_message = 'verbose '
help_message += '[default is False]'
parser.add_argument('-v', '--verbose',
                    dest='verbose',
                    action='store_true',
                    default=False,
                    help=help_message)

help_message = 'keep pre-existing files in the output directory '
help_message += '[default is False]'
parser.add_argument('-k', '--keep',
                    dest='keep_pre_existing_files',
                    action='store_true',
                    default=False,
                    help=help_message)

help_message = 'perform a camera station parameter database dump '
help_message += '[default is False]'
parser.add_argument('-d', '--dump-database',
                    dest='dump_station_parameters_database',
                    action='store_true',
                    default=False,
                    help=help_message)

args = parser.parse_args()
verbose = args.verbose
keep_pre_existing_files = args.keep_pre_existing_files
dump_station_parameters_database = args.dump_station_parameters_database

initial_startup = True
upload_successful = False

while True:
   # Pick up the latest parameters from the databases
   if dump_station_parameters_database:
      station_parameters = database.get_station_parameters(verbose=True)
      hourly_parameters = database.get_hourly_parameters(verbose=True)
      hardware_parameters = database.get_hardware_parameters(verbose=True)
      sys.exit()
   else:
      if verbose:
         msg = 'Picking up the latest parameters from the '
         msg += 'configuration databases ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      station_parameters = database.get_station_parameters()
      if station_parameters:
         station_parameters_pickup_successful = True
         previous_station_parameters = station_parameters
      else:
         station_parameters_pickup_successful = False
         if initial_startup:
            msg = '... exiting'
            msg += '\n'
            sys.stderr.write(msg)
            sys.stderr.flush()
            sys.exit()
         else:
            msg = '... using previous station parameters'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
            station_parameters = previous_station_parameters

      hourly_parameters = database.get_hourly_parameters()
      if hourly_parameters:
         hourly_parameters_pickup_successful = True
         previous_hourly_parameters = hourly_parameters
      else:
         hourly_parameters_pickup_successful = False
         if initial_startup:
            msg = '... exiting'
            msg += '\n'
            sys.stderr.write(msg)
            sys.stderr.flush()
            sys.exit()
         else:
            msg = '... using previous hourly parameters'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
            hourly_parameters = previous_hourly_parameters

      hardware_parameters = database.get_hardware_parameters()
      if hardware_parameters:
         hardware_parameters_pickup_successful = True
         previous_hardware_parameters = hardware_parameters
      else:
         hardware_parameters_pickup_successful = False
         if initial_startup:
            msg = '... exiting'
            msg += '\n'
            sys.stderr.write(msg)
            sys.stderr.flush()
            sys.exit()
         else:
            msg = '... using previous hardware parameters'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
            hardware_parameters = previous_hardware_parameters

   # Parse the database boolean parameters that need language-specific
   # interpretation
   if station_parameters['skipEvening'].lower() == 'true':
      station_parameters['skipEvening'] = True
   else:
      station_parameters['skipEvening'] = False

   # Convert e-mail receivers from a string to a list
   receivers = station_parameters['emailReceivers']
   station_parameters['emailReceivers'] = receivers.split('|')

   # Organize hardware information into a device-specific dictionary
   hardware = {}
   mac_address = utils.get_mac_address('-')
   try:
      index = hardware_parameters['macAddress'].index(mac_address)
      hardware['station_name'] = hardware_parameters['stationName'][index]
      hardware['interface_name'] = hardware_parameters['interfaceName'][index]
      hardware['mac_address'] = mac_address
      hardware['ipv4_address'] = hardware_parameters['ipv4Address'][index]
      hardware['dns_name'] = hardware_parameters['dnsName'][index]
      hardware['port_number'] = hardware_parameters['portNumber'][index]
      hardware['phone_number'] = hardware_parameters['phoneNumber'][index]
   except ValueError:
      hardware = {}
      hardware['station_name'] = None
      hardware['interface_name'] = None
      hardware['mac_address'] = mac_address
      hardware['ipv4_address'] = None
      hardware['dns_name'] = None
      hardware['port_number'] = None
      hardware['phone_number'] = None

   # Share the station name with the station parameters' dictionary
   if hardware['station_name']:
      station_parameters['stationName'] = hardware['station_name']
   else:
      station_parameters['stationName'] = 'unknown'

   # Check that the output directory exists and it writable
   if verbose:
      msg = 'Checking that the output directory exists and is writeable ...'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
   if not os.access(station_parameters['localDirectory'], os.W_OK):
      msg = '*** ERROR *** Output directory is not accessible for writing'
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()

   # Initialize the camera
   camera_parameters = camera.initialize(station_parameters, verbose=verbose)

   # Perform startup only actions
   if initial_startup:
      # Remove pre-existing files in the output directory
      local_filenames = \
         utils.get_file_listing(station_parameters['localDirectory'])
      if len(local_filenames) > 0:
         if keep_pre_existing_files:
            if verbose:
               msg = 'Keeping pre-existing files in the output directory ...'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
         else:
            if verbose:
               msg = 'Removing pre-existing files from the output directory ...'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            for local_filename in local_filenames:
               os.remove(local_filename)

      # Send an initial system health e-mail
      if verbose:
         msg = 'Sending an initial system health e-mail ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      utils.send_health_email(station_parameters,
                              station_parameters_pickup_successful,
                              hourly_parameters_pickup_successful,
                              hardware_parameters_pickup_successful)
      if verbose:
         msg = '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      initial_startup = False

   # Repeatedly trigger the camera
   if verbose:
      msg = 'Waiting for first trigger ...'
      msg += '\n'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()

   try:
      while True:
         # Slow down the program to reduce power consumption
         time.sleep(station_parameters['cameraSyncTolerance'])

         # Get current time [s] (UTC)
         iso8601_time_string = \
            clock.iso8601_time_string_using_computer_clock()
         seconds_since_midnight = \
            clock.convert_iso8601_time_string(iso8601_time_string, 's')

         # If it is the scheduled time, break out of the triggering loop
         # to pick up the latest camera station parameters
         update_time = station_parameters['updateHour'] * 3600
         if seconds_since_midnight == update_time:
            if verbose:
               msg = 'Turning off the camera ...'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            camera.close(station_parameters, camera_parameters, verbose=verbose)
            time.sleep(15)
            break

         # If it is the scheduled time, send a system health e-mail
         health_email_time = station_parameters['healthEmailHour'] * 3600
         if seconds_since_midnight == health_email_time:
            if verbose:
               msg = 'Sending a system health e-mail ...'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            utils.send_health_email(station_parameters,
                                    station_parameters_pickup_successful,
                                    hourly_parameters_pickup_successful,
                                    hardware_parameters_pickup_successful,
                                    upload_successful)
            if verbose:
               msg = '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            time.sleep(1)
            continue

         # If it is the scheduled time, upload daily imagery to the server
         upload_time = station_parameters['uploadHour'] * 3600
         if seconds_since_midnight == upload_time:
            if verbose:
               msg = 'Performing the daily imagery upload ...'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            # Create a list of all files to upload
            local_filenames = \
               utils.get_file_listing(station_parameters['localDirectory'])
            # Perform the upload
            if len(local_filenames) > 0:
               upload_successful = \
                  utils.upload_files_to_ftp_server(
                     local_filenames,
                     station_parameters['ftpServer'],
                     station_parameters['ftpDirectory'],
                     verbose=verbose,
                     report_stats=verbose)
               if verbose:
                  msg = '\n'
                  sys.stdout.write(msg)
                  sys.stdout.flush()
            else:
               if verbose:
                  msg = '*** WARNING *** No daily imagery found for upload'
                  msg += '\n'
                  msg += '\n'
                  sys.stdout.write(msg)
                  sys.stdout.flush()
            # Remove the files that were just uploaded
            if len(local_filenames) > 0:
               if upload_successful:
                  if verbose:
                     msg = 'Removing the daily imagery that was just '
                     msg += 'uploaded ...'
                     msg += '\n'
                     msg += '\n'
                     sys.stdout.write(msg)
                     sys.stdout.flush()
                  for local_filename in local_filenames:
                     os.remove(local_filename)
               else:
                  if verbose:
                     msg = 'Daily imagery upload was not successful, leaving '
                     msg += 'imagery in place ...'
                     msg += '\n'
                     msg += '\n'
                     msg += 'Waiting for next trigger ...'
                     msg += '\n'
                     msg += '\n'
                     sys.stdout.write(msg)
                     sys.stdout.flush()
            time.sleep(1)
            continue

         # Determine the current trigger frequency
         hour = seconds_since_midnight // 3600
         trigger_frequency = hourly_parameters['triggerFrequency'][hour]

         # If it is the next triggering time, begin that process
         if seconds_since_midnight % trigger_frequency == 0:
            # Report the trigger time
            if verbose:
               seconds = seconds_since_midnight
               hour = seconds // 3600
               seconds = seconds_since_midnight - hour * 3600
               minute = seconds // 60
               seconds = seconds - minute * 60 
               msg = 'Triggering process started at '
               msg += '{0:02d}:'.format(hour)
               msg += '{0:02d}:'.format(minute)
               msg += '{0:02d}'.format(seconds)
               msg += 'Z'
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()

            # Skip evening imaging if desired
            if station_parameters['skipEvening']:
               if clock.is_evening(iso8601_time_string,
                                   station_parameters['longitude'],
                                   station_parameters['latitude']):
                  if verbose:
                     sunrise, sunset = \
                        clock.sunrise_sunset(iso8601_time_string,
                                             station_parameters['longitude'],
                                             station_parameters['latitude'])
                     msg = '... skipping, resuming at '
                     msg+= '{0}'.format(sunrise[11:19])
                     msg += 'Z'
                     msg += '\n'
                     msg += '\n'
                     sys.stdout.write(msg)
                     sys.stdout.flush()
                  time.sleep(1)
                  continue

            # Form the current basename for saving the image (this is
            # the basename, no extension, the extension is left to the
            # specific capture method)
            basename = iso8601_time_string.replace(':', '-').replace('.', '-')
            basename += '_'
            if hardware['station_name']:
               basename += hardware['station_name']
            else:
               basename += hardware['mac_address']
            local_basename = \
               os.path.join(station_parameters['localDirectory'], basename)

            # Capture image and save it to the local disk
            capture_status = \
               camera.capture(station_parameters,
                              camera_parameters,
                              local_basename,
                              verbose=verbose)

            # Delay execution until the next second
            time.sleep(1)

            # Check the capture status and reset camera if necessary
            if capture_status == 0:
               if verbose:
                  msg = 'Attempting a camera re-initialization ...'
                  msg += '\n'
                  sys.stdout.write(msg)
                  sys.stdout.flush()

               # Close the camera connection
               camera.close(station_parameters,
                            camera_parameters,
                            verbose=verbose)

               # Power cycle the camera
               if verbose:
                  msg = 'Power cycling the camera ...'
                  msg += '\n'
                  sys.stdout.write(msg)
                  sys.stdout.flush()
               camera.power_cycle(station_parameters,
                                  shutdown_duration=15,
                                  startup_duration=15,
                                  verbose=verbose)
               if verbose:
                  msg = '\n'
                  sys.stdout.write(msg)
                  sys.stdout.flush()

               # Re-initialize the camera
               camera_parameters = \
                  camera.initialize(station_parameters, verbose=verbose)

               # Send a power cycle alert e-mail
               if verbose:
                  msg = 'Sending a power cycle alert e-mail ...'
                  msg += '\n'
                  sys.stdout.write(msg)
                  sys.stdout.flush()
               utils.send_power_cycle_email(station_parameters)

               if verbose:
                  msg = '\n'
                  msg += 'Waiting for next trigger ...'
                  msg += '\n'
                  msg += '\n'
                  sys.stdout.write(msg)
                  sys.stdout.flush()

   except KeyboardInterrupt:
      # Close the camera connection
      msg = '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
      if verbose:
         msg = 'Turning off the camera ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      camera.close(station_parameters, camera_parameters, verbose=verbose)

      # Exit the script
      if verbose:
         msg = 'Exiting ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      sys.exit()
