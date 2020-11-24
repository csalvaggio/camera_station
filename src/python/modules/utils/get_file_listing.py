import os
import os.path

def get_file_listing(directory):
   directory_listing = sorted(os.listdir(directory))
   filenames = []
   for filename in directory_listing:
      path = os.path.join(directory, filename)
      if os.path.isfile(path):
         filenames.append(path)

   return filenames

if __name__ == '__main__':
   import os.path

   import utils

   directory = os.path.expanduser('~')
   filenames = utils.get_file_listing(directory)

   if len(filenames) > 0:
      for filename in filenames:
         print(filename)
   else:
      msg = 'No filenames returned'
      print(msg)
