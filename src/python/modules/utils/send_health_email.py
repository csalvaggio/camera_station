import os.path
import smtplib
import socket
import sys

import battery
import clock
import sensors
import utils

def send_health_email(station_parameters,
                      station_parameters_pickup_successful=False,
                      hourly_parameters_pickup_successful=False,
                      hardware_parameters_pickup_successful=False,
                      upload_successful=False,
                      files_uploaded=0):

   # Get the hostname
   hostname = socket.gethostname()

   # Get the MAC address
   mac_address = utils.get_mac_address('-')

   # Get the IP address
   ip_address = utils.get_ip_address()

   # Get the sunrise and sunset times for the current day
   iso8601_time_string = clock.iso8601_time_string_using_computer_clock()
   sunrise, sunset = clock.sunrise_sunset(iso8601_time_string,
                                          station_parameters['longitude'],
                                          station_parameters['latitude'])

   # Get the storage statistics
   filenames = utils.get_file_listing(station_parameters['localDirectory'])
   bytes_used = 0
   for filename in filenames:
      bytes_used += os.path.getsize(filename)

   # Get the battery voltage
   voltmeter = battery.Voltmeter()
   voltage = voltmeter.read(samples=16)
   voltmeter.close()

   # Get the enclosure's interior environmental paramaters
   readings = sensors.temperature_humidity(temperature_units='f')
   if readings:
      temperature, humidity = readings
   else:
      temperature = None
      humidity = None

   # Form the message
   message = 'From: {0}\n'.format(station_parameters['emailSender'])
   if type(station_parameters['emailReceivers']) is list:
      r = str(station_parameters['emailReceivers'])[1:-1]
      r = r.replace("'", "").replace('"', '')
      message += 'To: {0}\n'.format(r)
   else:
      message += 'To: {0}\n'.format(station_parameters['emailReceivers'])
   message += 'Subject: Daily Health Message '
   message += '({0}) '.format(mac_address)
   message += '[{0}]\n'.format(station_parameters['stationName'])
   message += '\n'
   message += 'Hostname:  {0}\n'.format(hostname)
   message += 'Station name:  {0}\n'.format(station_parameters['stationName'])
   message += 'MAC:  {0}\n'.format(mac_address)
   message += 'IP address:  {0}\n'.format(ip_address)
   message += '\n'
   message += 'Time:  {0}\n'.format(iso8601_time_string)
   message += 'Sunrise:  {0}\n'.format(sunrise)
   message += 'Sunset:  {0}\n'.format(sunset)
   message += '\n'
   if voltage:
      message += 'Battery voltage:  {0:.2f} [V]\n'.format(voltage)
   else:
      message += 'Battery voltage:  n/a\n'
   message += '\n'
   if temperature:
      message += 'Temperature:  {0:.1f} [F]\n'.format(temperature)
   else:
      message += 'Temperature:  n/a\n'
   if humidity:
      message += 'Humidity:  {0:.1f} [%]\n'.format(humidity)
   else:
      message += 'Humidity:  n/a\n'
   if station_parameters['updateHour'] >= 0:
      message += '\n'
      message += 'Most recent station parameters update:  '
      message += \
         'SUCCESS\n' if station_parameters_pickup_successful else 'FAILED\n'
      message += 'Most recent hourly parameters update:  '
      message += \
         'SUCCESS\n' if hourly_parameters_pickup_successful else 'FAILED\n'
      message += 'Most recent hardware parameters update:  '
      message += \
         'SUCCESS\n' if hardware_parameters_pickup_successful else 'FAILED\n'
   if station_parameters['uploadHour'] >= 0:
      message += '\n'
      message += 'Most recent file upload attempt:  '
      message += \
         'SUCCESS ({0} files uploaded)\n'.format(files_uploaded) \
         if upload_successful else 'FAILED\n'
      message += '\n'
      message += 'Number of images currently held on station\'s local storage: '
      message += '{0:,}\n'.format(len(filenames))
      message += 'Local storage currently used:  '
      message += '{0:,} [bytes]\n'.format(bytes_used)

   # Send the message
   smtp = smtplib.SMTP()
   try:
      smtp.connect(station_parameters['smtpServer'])
   except socket.gaierror:
      msg = '*** ERROR *** SMTP server address is invalid or could not be '
      msg += 'resolved'
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()
   except:
      msg = '*** WARNING *** Unable to connect to SMTP server to send'
      msg += 'daily health message'
      msg += '\n'
      msg += '... aborting attempt'
      msg += '\n'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
      return

   try:
      smtp.sendmail(station_parameters['emailSender'],
                    station_parameters['emailReceivers'],
                    message)
   except smtplib.SMTPException:
      msg = '*** WARNING *** Unable to send daily health message'
      msg += '\n'
      msg += '... aborting attempt'
      msg += '\n'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
      return



if __name__ == '__main__':
   import os.path

   import utils

   station_parameters = {}
   station_parameters['stationName'] = 'cameraXXX'
   station_parameters['longitude'] = -77.6088
   station_parameters['latitude'] = 43.1566
   station_parameters['localDirectory'] = os.path.expanduser('~')
   station_parameters['emailSender'] = 'salvaggio@cis.rit.edu'
   receivers = 'salvaggio@cis.rit.edu|carl.salvaggio@rit.edu'
   station_parameters['emailReceivers'] = receivers.split('|')
   station_parameters['smtpServer'] = 'mail.cis.rit.edu'

   utils.send_health_email(station_parameters,
                           True,
                           True,
                           True,
                           True,
                           10)
