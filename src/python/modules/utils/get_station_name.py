import sys

import database
import utils

def get_station_name():
   hardware_parameters = database.get_hardware_parameters()
   mac_address = utils.get_mac_address('-')

   idx = hardware_parameters['macAddress'].index(mac_address)
   station_name = hardware_parameters['stationName'][idx]

   return station_name



if __name__ == '__main__':
   import sys

   import utils

   station_name = utils.get_station_name()

   msg = station_name
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
