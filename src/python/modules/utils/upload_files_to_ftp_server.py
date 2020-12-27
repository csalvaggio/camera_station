import ftplib
import os.path
import sys
import time

def upload_files_to_ftp_server(local_filenames,
                               target_host,
                               target_directory,
                               verbose=False,
                               report_stats=False):

   files_uploaded = 0
   bytes_uploaded = 0
   start_time = time.perf_counter()
   for local_filename in local_filenames:
      if verbose:
         msg = 'Uploading {0} ... '.format(local_filename)
         sys.stdout.write(msg)
         sys.stdout.flush()

      try:
         ftp = ftplib.FTP(target_host)
      except:
         msg = '*** WARNING *** Connection to FTP server could not be made'
         msg += '\n'
         msg += '... aborting upload'
         msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         return False

      ftp.login()

      try:
         ftp.cwd(target_directory)
      except:
         msg = '*** WARNING *** Could not change to target directory on the '
         msg += 'FTP server'
         msg += '\n'
         msg += '... aborting upload'
         msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         ftp.close()
         return False

      try:
         target_filename = os.path.basename(local_filename)
         f = open(local_filename, 'rb')
         ftp.storbinary('STOR ' + target_filename, f)
         f.close()
         files_uploaded += 1
         bytes_uploaded += os.path.getsize(local_filename)
      except ftplib.error_perm:
         msg = '\n'
         msg += '*** WARNING *** A file with the same name already exists '
         msg += 'on the server'
         msg += '\n'
         msg += '... moving on to the next file'
         msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         ftp.close()
         del ftp
         continue
      except:
         msg = '\n'
         msg += '*** WARNING *** An unspecified error occurred during upload'
         msg += '\n'
         msg += '... aborting upload'
         msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         ftp.close()
         return False

      if verbose:
         msg = 'completed'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      ftp.close()
      del ftp

   if report_stats:
      elapsed_time = time.perf_counter() - start_time
      msg = '-----------------------------------'
      msg += '\n'
      msg += 'Transferred: {0:,} files'.format(files_uploaded)
      msg += '\n'
      msg += 'Transferred: {0:,} bytes'.format(bytes_uploaded)
      msg += '\n'
      msg += 'Elapsed time: {0:.6f} [s]'.format(elapsed_time)
      msg += '\n'
      msg += 'Transfer rate: '
      msg += '{0:.3f} Mbps'.format(bytes_uploaded * 8 / 1000 / 1000 / \
                                   elapsed_time)
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()

   return True



if __name__ == '__main__':
   import os
   import utils

   target_host = 'ftp.cis.rit.edu'
   target_directory = 'dirs/cnspci/incoming/doe/srnl/mdct2/jasper/images'

   local_directory = '.'

   local_directory_listing = sorted(os.listdir(local_directory))
   local_filenames = []
   for local_filename in local_directory_listing:
      local_path = os.path.join(local_directory, local_filename)
      if os.path.isfile(local_path):
         local_filenames.append(local_path)

   utils.upload_files_to_ftp_server(local_filenames,
                                    target_host,
                                    target_directory,
                                    verbose=True,
                                    report_stats=True)
