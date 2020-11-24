import uuid

def get_mac_address():
   node = hex(uuid.getnode())
   mac_address = '{0}'.format(node[2:14])
   return mac_address
