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
   images_directory = \
      os.path.join(station_parameters['localDirectory'], 'images')
   filenames = utils.get_file_listing(images_directory)
   bytes_used = 0
   for filename in filenames:
      bytes_used += os.path.getsize(filename)

   # Get the source (battery) voltage
   voltmeter = battery.Voltmeter(0)
   source = voltmeter.read(samples=16)
   voltmeter.close()

   # Get the regulator (7.6V) output voltage
   voltmeter = battery.Voltmeter(1)
   regulator76 = voltmeter.read(samples=16)
   voltmeter.close()

   # Get the regulator (5V) output voltage
   voltmeter = battery.Voltmeter(2)
   regulator5 = voltmeter.read(samples=16)
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
   message += 'Battery:  '
   message += '{0:.2f} [V]\n'.format(source) if source else 'n/a\n'
   message += 'Regulator (7.6V) output:  '
   message += '{0:.2f} [V]\n'.format(regulator76) if regulator76 else 'n/a\n'
   message += 'Regulator (5V) output:  '
   message += '{0:.2f} [V]\n'.format(regulator5) if regulator5 else 'n/a\n'
   message += '\n'
   message += 'Temperature:  '
   message += '{0:.1f} [F]\n'.format(temperature) if temperature else 'n/a\n'
   message += 'Humidity:  '
   message += '{0:.1f} [%]\n'.format(humidity) if humidity else 'n/a\n'
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
   station_parameters['localDirectory'] = '/media/pi/STORAGE'
   station_parameters['updateHour'] = 8
   station_parameters['uploadHour'] = 3
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
