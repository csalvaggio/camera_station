import mysql.connector
import sys

import database

def get_hardware_parameters(verbose=False):
   # Establish the database connection
   db = database.db_connect()

   # If database connection was not made, return a null response
   if db is None:
      return None

   if db.is_connected:
      # Establish the list of fields to query
      fields = ('ID',
                'stationName',
                'interfaceName',
                'macAddress',
                'imei',
                'iccid',
                'ipv4Address',
                'dnsName',
                'portNumber',
                'phoneNumber')

      # Build the query
      query = 'SELECT '
      for field in fields:
         query += field
         query += ', '
      query = query[0:-2] + ' '
      query += 'FROM hardware_parameters'

      #Establish the database record cursor/pointer
      cursor = db.cursor()

      # Execute the query
      cursor.execute(query)

      # Fetch all retrieved records into a list
      rows = cursor.fetchall()

      # Load the records/rows into lists in parameters dictionary
      if len(rows) > 0:
         parameters = {}
         # Initialize lists for each parameter
         idx = 0
         for field in fields:
            parameters[field] = []
            idx += 1
         # Append each records/rows values to lists in parameters dictionary
         for row in rows:
            idx = 0
            for field in fields:
               parameters[field].append(row[idx])
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
