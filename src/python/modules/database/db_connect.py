import mysql.connector
import sys

def db_connect():
   try:
      db = mysql.connector.connect(
         host='dirsapps.cis.rit.edu',
         user='mdct2',
         password='cab1sehecan2mnad',
         database='mdct2'
      )
      return db
   except:
      msg = '*** ERROR *** Database connection could not be established'
      msg += '\n'
      sys.stderr.write(msg)
      sys.stderr.flush()
      sys.exit()
