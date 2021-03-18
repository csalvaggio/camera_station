import mysql.connector
import sys

def db_connect():
   databaseServer = 'dirsapps.cis.rit.edu'
   databaseServerIpAddress = '129.21.57.5'
   try:
      db = mysql.connector.connect(
         host=databaseServer,
         user='mdct2',
         password='cab1sehecan2mnad',
         database='mdct2'
      )
      return db
   except:
      try:
         db = mysql.connector.connect(
            host=databaseServerIpAddress,
            user='mdct2',
            password='cab1sehecan2mnad',
            database='mdct2'
         )
         return db
      except:
         msg = '*** WARNING *** Database connection could not be established'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         return None
