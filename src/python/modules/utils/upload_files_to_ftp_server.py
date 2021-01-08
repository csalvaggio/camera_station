import ftplib
import os.path
import sys
import time

def upload_files_to_ftp_server(local_filenames,
                               target_host,
                               target_directory,
                               verbose=False,
                               delete_after_upload=False,
                               report_stats=False):

   try:
      ftp = ftplib.FTP(target_host)
   except:
      msg += '\n'
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
      msg += '\n'
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

   files_uploaded = 0
   bytes_uploaded = 0
   start_time = time.perf_counter()
   for local_filename in local_filenames:
      if verbose:
         msg = 'Uploading {0} ... '.format(local_filename)
         sys.stdout.write(msg)
         sys.stdout.flush()

      try:
         target_filename = os.path.basename(local_filename)
         f = open(local_filename, 'rb')
         ftp.storbinary('STOR ' + target_filename, f)
         f.close()
         files_uploaded += 1
         bytes_uploaded += os.path.getsize(local_filename)
      except ftplib.error_perm:
         msg = '\n'
         msg += '*** WARNING *** Permission error encountered'
         msg += '\n'
         msg += 'A file with the same name as the target may already exists or '
         msg += 'you may not have permission to write to the target directory'
         msg += '\n'
         msg += '... moving on to the next file'
         msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         continue
      except KeyboardInterrupt:
         msg = '\n'
         msg += '*** WARNING *** User initiated interrupt detected'
         msg += '\n'
         msg += '... aborting upload'
         msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()
         ftp.close()
         return False
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

      if delete_after_upload:
         if verbose:
            msg = '... deleting uploaded file'
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         os.remove(local_filename)

   ftp.close()

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
   import argparse
   import os
   import utils

   # Defaults
   target_host = 'ftp.cis.rit.edu'
   target_directory = 'dirs/cnspci/incoming/doe/srnl/mdct2/jasper/images'
   local_directory = '.'

   # Parse the command-line arguments
   description = 'Upload files in a local directory to server using '
   description += 'anonymous FTP'
   parser = argparse.ArgumentParser(description=description)

   help_message = 'verbose '
   help_message += '[default is False]'
   parser.add_argument('-v', '--verbose',
                       dest='verbose',
                       action='store_true',
                       default=False,
                       help=help_message)

   help_message = 'delete local files after upload '
   help_message += '[default is False]'
   parser.add_argument('-d', '--delete',
                       dest='delete_after_upload',
                       action='store_true',
                       default=False,
                       help=help_message)

   help_message = 'report upload statistics upon completion '
   help_message += '[default is False]'
   parser.add_argument('-r', '--report',
                       dest='report_stats',
                       action='store_true',
                       default=False,
                       help=help_message)

   help_message = 'target host '
   help_message += '[default is {0}]'.format(target_host)
   parser.add_argument('-th', '--target-host',
                       dest='target_host',
                       type=str,
                       default=target_host,
                       help=help_message)

   help_message = 'target directory '
   help_message += '[default is {0}]'.format(target_directory)
   parser.add_argument('-td', '--target-directory',
                       dest='target_directory',
                       type=str,
                       default=target_directory,
                       help=help_message)

   help_message = 'local directory '
   help_message += '[default is {0}]'.format(local_directory)
   parser.add_argument('-ld', '--local-directory',
                       dest='local_directory',
                       type=str,
                       default=local_directory,
                       help=help_message)

   args = parser.parse_args()
   verbose = args.verbose
   delete_after_upload = args.delete_after_upload
   report_stats = args.report_stats
   target_host = args.target_host
   target_directory = args.target_directory
   local_directory = args.local_directory

   local_directory_listing = sorted(os.listdir(local_directory))
   local_filenames = []
   for local_filename in local_directory_listing:
      local_path = os.path.join(local_directory, local_filename)
      if os.path.isfile(local_path):
         local_filenames.append(local_path)

   utils.upload_files_to_ftp_server(local_filenames,
                                    target_host,
                                    target_directory,
                                    verbose=verbose,
                                    delete_after_upload=delete_after_upload,
                                    report_stats=report_stats)
