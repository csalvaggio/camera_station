import sys

import database
import utils

hardware_parameters = database.get_hardware_parameters()
mac_address = utils.get_mac_address('-')

idx = hardware_parameters['macAddress'].index(mac_address)
station_name = hardware_parameters['stationName'][idx]

msg = station_name
msg += '\n'
sys.stdout.write(msg)
sys.stdout.flush()
