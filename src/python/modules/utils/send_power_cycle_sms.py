import smtplib
import sys

def send_power_cycle_sms(station_parameters):

   # Form the message
   message = 'From: {0}\n'.format(station_parameters['smsSender'])
   if type(station_parameters['smsReceivers']) is list:
      r = str(station_parameters['smsReceivers'])[1:-1]
      r = r.replace("'", "").replace('"', '')
      message += 'To: {0}\n'.format(r)
   else:
      message += 'To: {0}\n'.format(station_parameters['smsReceivers'])
   message += 'Subject: Camera Power Cycle Occurred\n'
   message += '\n'
   message += 'Station name: {0}\n'.format(station_parameters['stationName'])

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
      smtp.sendmail(station_parameters['smsSender'],
                    station_parameters['smsReceivers'],
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
   station_parameters['smsSender'] = 'salvaggio@cis.rit.edu'
   receivers = 'cnspci-sms@cis.rit.edu'
   station_parameters['smsReceivers'] = receivers.split('|')
   station_parameters['smtpServer'] = 'mail.cis.rit.edu'

   utils.send_power_cycle_sms(station_parameters)
