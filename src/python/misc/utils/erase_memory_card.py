import os
import os.path

def get_full_paths(camera, top_level_directory='/'):
   full_paths = []

   # Construct the full filepath for each file in the top-level directory
   # and add to the list of full paths
   for filename, value in camera.folder_list_files(top_level_directory):
      fullpath = os.path.join(top_level_directory, filename)
      full_paths.append(fullpath)

   # Get the subdirectory names in the top-level directory
   subdirectories = []
   for subdirectory, value in camera.folder_list_folders(top_level_directory):
      subdirectories.append(subdirectory)

   # Recurse over subdirectories and extend the list of full paths
   for subdirectory in subdirectories:
      full_paths.extend(get_full_paths(camera,
                                       os.path.join(top_level_directory,
                                                    subdirectory)))

   return full_paths



if __name__ == "__main__":
   import sys

   import gphoto2

   camera = gphoto2.Camera()
   camera.init()

   full_paths = get_full_paths(camera)

   separator = '----------' * 8
   msg = separator
   msg += '\n'
   msg += 'FILES FOUND ON CAMERA\'S MEMORY CARD'
   msg += '\n'
   msg += separator
   msg += '\n'
   if not full_paths:
      msg += 'No files found'
      msg += '\n'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
      camera.exit()
      sys.exit()

   for full_path in full_paths:
      msg += full_path
      msg += '\n'
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()

   msg = 'Would you like to erase ALL of these files (Y/n)? '
   answer = input(msg)

   if answer == 'Y':
      msg = '\n'
      msg += '... deleting ALL files from the camera\'s memory card'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()

      for full_path in full_paths:
         directory, filename = os.path.split(full_path)
         camera.file_delete(directory, filename)

   else:
      msg = '\n'
      msg += '... no files were deleted'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()

   camera.exit()

   msg = '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
