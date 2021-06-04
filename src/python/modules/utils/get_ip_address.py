import socket

def get_ip_address():
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.connect(("8.8.8.8", 80))
      ip_address = s.getsockname()[0]
   except:
      ip_address = None
   return ip_address
