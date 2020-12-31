import smtplib
import socket
import sys

import clock
import utils

def send_power_cycle_email(station_parameters):

   # Get the hostname
   hostname = socket.gethostname()

   # Get the MAC address
   mac_address = utils.get_mac_address('-')

   # Get the IP address
   ip_address = utils.get_ip_address()

   # Get the current universal coordinated time (UTC)
   iso8601_time_string = clock.iso8601_time_string_using_computer_clock()

   # Form the message
   message = 'From: {0}\n'.format(station_parameters['emailSender'])
   if type(station_parameters['emailReceivers']) is list:
      r = str(station_parameters['emailReceivers'])[1:-1]
      r = r.replace("'", "").replace('"', '')
      message += 'To: {0}\n'.format(r)
   else:
      message += 'To: {0}\n'.format(station_parameters['emailReceivers'])
   message += 'Subject: *** IMPORTANT *** Camera Power Cycle Occurred '
   message += '({0}) '.format(mac_address)
   message += '[{0}]\n'.format(station_parameters['stationName'])
   message += '\n'
   message += 'Hostname:  {0}\n'.format(hostname)
   message += 'Station name:  {0}\n'.format(station_parameters['stationName'])
   message += 'MAC:  {0}\n'.format(mac_address)
   message += 'IP address:  {0}\n'.format(ip_address)
   message += '\n'
   message += 'Time:  {0}\n'.format(iso8601_time_string)
   message += '\n'
   message += 'A power cycle was just completed on the camera attached to '
   message += 'this station.  You should check the operations log to make '
   message += 'sure that normal operations have resumed.\n'
   message += '\n'
   message += 'If normal operations have not resumed, you may want to '
   message += 'consider:\n'
   message += '\n'
   message += '   1) Terminating and restarting the collection script\n'
   message += '   2) Power cycling the camera again manually\n'
   message += '   3) Rebooting the controlling computer\n'

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
      msg += 'power cycle message'
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
      msg = '*** WARNING *** Unable to send power cycle message'
      msg += '\n'
      msg += '... aborting attempt'
      msg += '\n'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
      return



if __name__ == '__main__':

   import utils

   station_parameters = {}
   station_parameters['stationName'] = 'cameraXXX'
   station_parameters['emailSender'] = 'salvaggio@cis.rit.edu'
   receivers = 'salvaggio@cis.rit.edu|carl.salvaggio@rit.edu'
   station_parameters['emailReceivers'] = receivers.split('|')
   station_parameters['smtpServer'] = 'mail.cis.rit.edu'

   utils.send_power_cycle_email(station_parameters)
