import mysql.connector
import sys

import database

def get_rpi_camera_parameters(verbose=False):
   # Establish the database connection
   db = database.db_connect()

   if db.is_connected:
      # Establish the list of fields to query
      fields = ('ID',
                'imageExtension',
                'secondsToWarmup',
                'useLosslessJpegCompression',
                'brightness',
                'sharpness',
                'contrast',
                'saturation',
                'ISO',
                'shutterSpeed',
                'exposureCompensation',
                'exposureMode',
                'meterMode',
                'awbMode',
                'rotation',
                'hFlip',
                'vFlip',
                'cropNormalizedULRow',
                'cropNormalizedULColumn',
                'cropNormalizedWidth',
                'cropNormalizedHeight',
                'resolutionColumns',
                'resolutionRows')

      # Build the query
      query = 'SELECT '
      for field in fields:
         query += field
         query += ', '
      query = query[0:-2] + ' '
      query += 'FROM rpi_camera_parameters'

      #Establish the database record cursor/pointer
      cursor = db.cursor()

      # Execute the query
      cursor.execute(query)

      # Fetch all retrieved records into a list
      rows = cursor.fetchall()

      # Load the last record/row into the parameters dictionary
      if len(rows) > 0:
         for row in rows:
            parameters = {}
            idx = 0
            for field in fields:
               parameters[field] = row[idx]
               idx += 1
      else:
         msg = '*** ERROR *** Query produced no results'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()

      # Close the cursor and disconnect from the database
      cursor.close()
      db.close()

      # Report out the parameters dictionary
      if verbose:
         for parameter in parameters:
            msg = '{0}: {1}'.format(parameter, parameters[parameter])
            msg += '\n'
            sys.stdout.write(msg)
            sys.stdout.flush()
         msg = '\n'
         sys.stdout.write(msg)
         sys.stdout.flush()

      return parameters
