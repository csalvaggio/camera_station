import urllib.request

def network_available(test_url='http://google.com'):
   try:
      urllib.request.urlopen(test_url)
      return True
   except:
      return False


if __name__ == '__main__':
   import utils

   if utils.network_available():
      print('Network IS available')
   else:
      print('Network IS NOT available')
