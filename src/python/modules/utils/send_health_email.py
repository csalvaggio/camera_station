import os.path
import smtplib
import socket
import sys

import battery
import clock
import utils

def send_health_email(station_parameters):
   # Get the hostname
   hostname = socket.gethostname()

   # Get the MAC address
   mac_address = utils.get_mac_address()

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
   voltage = voltmeter.read()
   voltmeter.close()

   # Form the message
   message = 'From: {0}\n'.format(station_parameters['healthEmailSender'])
   if type(station_parameters['healthEmailReceivers']) is list:
      r = str(station_parameters['healthEmailReceivers'])[1:-1]
      r = r.replace("'", "").replace('"', '')
      message += 'To: {0}\n'.format(r)
   else:
      message += 'To: {0}\n'.format(station_parameters['healthEmailReceivers'])
   message += 'Subject: Daily Health Message ({0})\n'.format(mac_address)
   message += '\n'
   message += 'Hostname:  {0}\n'.format(hostname)
   message += 'MAC:  {0}\n'.format(mac_address)
   message += 'IP address:  {0}\n'.format(ip_address)
   message += '\n'
   message += 'Battery voltage:  {0:.2f} [V]\n'.format(voltage)
   message += '\n'
   message += 'Sunrise:  {0}\n'.format(sunrise)
   message += 'Sunset:  {0}\n'.format(sunset)
   message += '\n'
   message += 'Number of image files:  {0:,}\n'.format(len(filenames))
   message += 'Storage used:  {0:,} [bytes]\n'.format(bytes_used)

   # Send the message
   try:
      smtp = smtplib.SMTP(station_parameters['smtpServer'])
      smtp.sendmail(station_parameters['healthEmailSender'],
                    station_parameters['healthEmailReceivers'],
                    message)
   except smtplib.SMTPException:
      msg = '*** ERROR *** Unable to send daily health message'
      msg += '\n'
      sys.stderr.write(msg)
      sys.exit()



if __name__ == '__main__':
   import os.path

   import utils

   station_parameters = {}
   station_parameters['longitude'] = -77.6088
   station_parameters['latitude'] = 43.1566
   station_parameters['localDirectory'] = os.path.expanduser('~')
   station_parameters['healthEmailSender'] = 'salvaggio@cis.rit.edu'
   receivers = 'salvaggio@cis.rit.edu|carl.salvaggio@rit.edu'
   station_parameters['healthEmailReceivers'] = receivers.split('|')
   station_parameters['smtpServer'] = 'mail.cis.rit.edu'

   utils.send_health_email(station_parameters)
