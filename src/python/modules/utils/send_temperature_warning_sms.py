import smtplib
import sys

import sensors

def send_temperature_warning_sms(station_parameters):
   readings = sensors.temperature_humidity(temperature_units='f')
   if readings:
      temperature, _ = readings
   else:
      temperature = None

   # Form the message
   message = 'From: {0}\n'.format(station_parameters['smsSender'])
   if type(station_parameters['smsReceivers']) is list:
      r = str(station_parameters['smsReceivers'])[1:-1]
      r = r.replace("'", "").replace('"', '')
      message += 'To: {0}\n'.format(r)
   else:
      message += 'To: {0}\n'.format(station_parameters['smsReceivers'])
   message += 'Subject: Temperature Warning\n'
   message += '\n'
   message += 'Station name: {0}, '.format(station_parameters['stationName'])
   message += station_parameters['temperatureLabel']
   message += ': '
   message += '{0:.1f}'.format(temperature)
   message += '\n'

   # Truncate message to meet SMS standards (160 characters)
   message = message[:160]

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
      msg = '*** WARNING *** Unable to connect to SMTP server to send '
      msg += 'temperature warning message'
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
      msg = '*** WARNING *** Unable to send temperature warning message'
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
   station_parameters['smsReceivers'] = \
      station_parameters['smsReceivers'].split('|')

   utils.send_temperature_warning_sms(station_parameters)
