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

help_message = 'perform a camera station parameter database dump '
help_message += '[default is False]'
parser.add_argument('-d', '--dump-database',
                    dest='dump_station_parameters_database',
                    action='store_true',
                    default=False,
                    help=help_message)

args = parser.parse_args()
verbose = args.verbose
dump_station_parameters_database = args.dump_station_parameters_database

initial_startup = True
upload_successful = False

while True:
   # Pick up the latest parameters from the databases
   if dump_station_parameters_database:
      station_parameters = database.get_station_parameters(verbose=True)
      hourly_parameters = database.get_hourly_parameters(verbose=True)
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
         previous_hourly_parameters = hourly_paramaters
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

   # Parse the database boolean parameters that need language-specific
   # interpretation
   if station_parameters['skipEvening'] == 'true':
      station_parameters['skipEvening'] = True
   else:
      station_parameters['skipEvening'] = False

   # Convert health e-mail receivers from a string to a list
   receivers = station_parameters['healthEmailReceivers']
   station_parameters['healthEmailReceivers'] = receivers.split('|')

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
                              hourly_parameters_pickup_successful)
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
               msg += '\n'
               sys.stdout.write(msg)
               sys.stdout.flush()
            camera.close(station_parameters, camera_parameters)
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

            # Form the current filename for saving the image
            basename = iso8601_time_string.replace(':', '-').replace('.', '-')
            basename += '_'
            basename += '{0}'.format(utils.get_mac_address('-'))
            basename += '.{0}'.format(camera_parameters['imageExtension'])
            local_filename = \
               os.path.join(station_parameters['localDirectory'], basename)

            # Capture image and save it to the local disk
            camera.capture(station_parameters,
                           camera_parameters,
                           local_filename,
                           verbose=verbose)

            # Delay execution until the next second
            time.sleep(1)

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
      camera.close(station_parameters, camera_parameters)

      # Exit the script
      if verbose:
         msg = 'Exiting ...'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
      sys.exit()
