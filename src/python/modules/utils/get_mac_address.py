import uuid

def get_mac_address(delimiter=''):
   mac_address = hex(uuid.getnode())[2:14]

   if len(mac_address) < 12:
      mac_address = (12 - len(mac_address)) * '0' + mac_address

   mac_address = \
      mac_address[0:2] + delimiter + \
      mac_address[2:4] + delimiter + \
      mac_address[4:6] + delimiter + \
      mac_address[6:8] + delimiter + \
      mac_address[8:10] + delimiter + \
      mac_address[10:12]

   return mac_address
