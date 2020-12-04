import socket

def get_ip_address():
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.connect(("8.8.8.8", 80))
   ip_address = s.getsockname()[0]
   return ip_address