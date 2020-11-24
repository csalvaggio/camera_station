import datetime

def is_between(iso8601_time_string, iso8601_time_string1, iso8601_time_string2):
   Y = int(iso8601_time_string[0:4])
   M = int(iso8601_time_string[5:7])
   D = int(iso8601_time_string[8:10])
   h = int(iso8601_time_string[11:13])
   m = int(iso8601_time_string[14:16])
   s = int(iso8601_time_string[17:19])
   S = int(iso8601_time_string[20:23]) * 1000
   d = datetime.datetime(Y, M, D, h, m, s, S)

   Y = int(iso8601_time_string1[0:4])
   M = int(iso8601_time_string1[5:7])
   D = int(iso8601_time_string1[8:10])
   h = int(iso8601_time_string1[11:13])
   m = int(iso8601_time_string1[14:16])
   s = int(iso8601_time_string1[17:19])
   S = int(iso8601_time_string1[20:23]) * 1000
   d1 = datetime.datetime(Y, M, D, h, m, s, S)

   Y = int(iso8601_time_string2[0:4])
   M = int(iso8601_time_string2[5:7])
   D = int(iso8601_time_string2[8:10])
   h = int(iso8601_time_string2[11:13])
   m = int(iso8601_time_string2[14:16])
   s = int(iso8601_time_string2[17:19])
   S = int(iso8601_time_string2[20:23]) * 1000
   d2 = datetime.datetime(Y, M, D, h, m, s, S)

   return d1 < d and d < d2



if __name__ == '__main__':
   import clock

   time_string  = '2020-12-31T23:52:37.119Z'
   time_string1 = '2020-12-31T22:10:15.372Z'
   time_string2 = '2021-01-01T07:13:38.710Z'

   msg = 'time_string:  {0}'.format(time_string)
   print(msg)
   msg = 'time_string1: {0}'.format(time_string1)
   print(msg)
   msg = 'time_string2: {0}'.format(time_string2)
   print(msg)
   msg = ''
   print(msg)

   if clock.is_between(time_string, time_string1, time_string2):
      msg = 'Specified time string IS between the two boundaries'
      print(msg)
   else:
      msg = 'Specified time string IS NOT between the two boundaries'
      print(msg)
