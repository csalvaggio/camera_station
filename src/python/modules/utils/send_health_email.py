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
                      files_uploaded=0,
                      captures_failed=0):

   # Get the hostname
   hostname = socket.gethostname()

   # Get the MAC address
   mac_address = utils.get_mac_address('-')

   # Get the IP address
   ip_address = utils.get_ip_address()
   if ip_address is None:
      ip_address = 'n/a'

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

   # Get the voltage(s)
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

   # Get the enclosure's interior environmental paramaters
   readings = sensors.temperature_humidity(temperature_units='f')
   if readings:
      temperature, humidity = readings
   else:
      temperature = None
      humidity = None

   packet_loss_percentage = \
      utils.packet_loss_percentage('pegasus.cis.rit.edu', 10)

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
   if any(voltmeterLabels):
      for voltmeterLabel in voltmeterLabels:
         if voltmeterLabel:
            message += voltmeterLabel
            message += ': '
            v = voltages[voltmeterLabels.index(voltmeterLabel)]
            message += '{0:.2f}'.format(v) if v else '0.00'
            message += '\n'
      message += '\n'
   message += station_parameters['temperatureLabel']
   message += ':  '
   message += '{0:.1f}\n'.format(temperature) if temperature else 'n/a\n'
   message += station_parameters['humidityLabel']
   message += ':  '
   message += '{0:.1f}\n'.format(humidity) if humidity else 'n/a\n'
   message += '\n'
   message += 'Current packet loss: {0}%\n'.format(packet_loss_percentage)
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
   message += '\n'
   message += 'Number of image captures that were unsuccessful: '
   message += '{0}\n'.format(captures_failed)

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
   import utils
   import database

   station_parameters = database.get_station_parameters()
   station_parameters['stationName'] = 'cameraXXX'
   station_parameters['emailReceivers'] = \
      station_parameters['emailReceivers'].split('|')

   utils.send_health_email(station_parameters,
                           True,
                           True,
                           True,
                           True,
                           10,
                           0)
