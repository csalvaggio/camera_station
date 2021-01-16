import sys
import time

import sensors.adafruit

def temperature_humidity(data_pin=14,
                         temperature_units='k',
                         timeout=10,
                         error_is_terminal=False,
                         verbose=False):
   try:
      dht = sensors.adafruit.adafruit_dht.DHT22(data_pin, use_pulseio=True)
   except:
      if error_is_terminal:
         msg = '*** ERROR *** '
         msg += 'Could not create DHT22 (temperature/humidity sensor) object'
         msg += '\n'
         msg += 'Exiting ...'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()
      else:
         if verbose:
            msg = '*** WARNING *** '
            msg += 'Could not create DHT22 (temperature/humidity sensor) object'
            msg += '\n'
            msg += 'Aborting ...'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         return None

   start_time = time.perf_counter()
   while True:
      if time.perf_counter() - start_time > timeout:
         if verbose:
            msg = '*** WARNING *** '
            msg += 'Failed to acquire temperature/humidity'
            msg += '\n'
            msg += '... aborting attempt'
            msg += '\n'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         dht.exit()
         return None
      try:
         temperature_c = dht.temperature
         humidity = dht.humidity
         break
      except RuntimeError:
         if verbose:
            msg = '*** WARNING *** '
            msg += 'Failed to acquire temperature/humidity, retrying ...'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         time.sleep(2)
         continue
      except Exception:
         if verbose:
            msg = '*** WARNING *** '
            msg += 'An unspecified error occurred acquiring '
            msg += 'temperature/humidity'
            msg += '\n'
            msg += '... aborting attempt'
            msg += '\n'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         dht.exit()
         return None

   dht.exit()

   if temperature_units.lower() == 'c':
      temperature = temperature_c
   elif temperature_units.lower() == 'f':
      temperature = temperature_c * (9/5) + 32
   elif temperature_units.lower() == 'k':
      temperature = temperature_c + 273.15
   else:
      if error_is_terminal:
         msg = '*** ERROR *** '
         msg += 'Invalid temperature units specified: '
         msg += '{0}'.format(temperature_units.lower())
         msg += '\n'
         msg += 'Exiting ...'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()
      else:
         if verbose:
            msg = '*** ERROR *** '
            msg += 'Invalid temperature units specified: '
            msg += '{0}'.format(temperature_units.lower())
            msg += '\n'
            msg += 'Aborting ...'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         return None

   return temperature, humidity



if __name__ == '__main__':

   import sys
   import time

   import sensors

   data_pin = 14
   temperature_units = 'f'
   timeout = 10
   error_is_terminal = True
   verbose = True

   readings = sensors.temperature_humidity(data_pin=data_pin,
                                           temperature_units=temperature_units,
                                           timeout=timeout,
                                           error_is_terminal=error_is_terminal,
                                           verbose=verbose)

   if readings:
      temperature, humidity = readings
      msg = 'Temperature: {0:.1f} '.format(temperature) 
      msg += '[{0}]'.format(temperature_units.upper())
      msg += '\n'
      msg += 'Humidity: {0:.1f} '.format(humidity) 
      msg += '[%]'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
   else:
      msg = 'Temperature: n/a'
      msg += '\n'
      msg += 'Humidity: n/a'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
