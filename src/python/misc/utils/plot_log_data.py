import argparse
import datetime
import numpy
import sys

import graphics


# Set default values for parameters
plot_filename = None
column_selected = None
start_date = None
end_date = None
minimum_dependent = None
maximum_dependent = None

# Parse command line arguments
description = 'Plot log data collected from the RIT/SRNL camera stations'
parser = argparse.ArgumentParser(description=description)

help_message = 'log filename'
parser.add_argument('log_filename', 
                    help=help_message)

help_message = 'column from log file to plot '
help_message += '[default is {0} '.format(column_selected)
help_message += '(user will interactively select from menu)]'
parser.add_argument('-c', '--column',
                    dest='column_selected',
                    type=int,
                    default=column_selected,
                    help=help_message)

help_message = 'start date for plot (YYYY-MM-DD) '
help_message += '[default is {0} '.format(start_date)
help_message += '(start at first date in log file)]'
parser.add_argument('-s', '--start-date',
                    dest='start_date',
                    type=str,
                    default=start_date,
                    help=help_message)

help_message = 'end date for plot (YYYY-MM-DD) '
help_message += '[default is {0} '.format(end_date)
help_message += '(end at last date in log file)]'
parser.add_argument('-e', '--end-date',
                    dest='end_date',
                    type=str,
                    default=end_date,
                    help=help_message)

help_message = 'minimum value for dependent variable axis '
help_message += '[default is {0} (auto scale)]'.format(minimum_dependent)
parser.add_argument('-min', '--minimum-dependent-value',
                    dest='minimum_dependent',
                    type=float,
                    default=minimum_dependent,
                    help=help_message)

help_message = 'maximum value for dependent variable axis '
help_message += '[default is {0} (auto scale)]'.format(maximum_dependent)
parser.add_argument('-max', '--maximum-dependent-value',
                    dest='maximum_dependent',
                    type=float,
                    default=maximum_dependent,
                    help=help_message)

help_message = 'filename to store plot to (extension defines file format) '
help_message += '[default is {0} '.format(plot_filename)
help_message += '(no file is written)]'
parser.add_argument('-o', '--output-plot-filename',
                    dest='plot_filename',
                    type=str,
                    default=plot_filename,
                    help=help_message)

args = parser.parse_args()
log_filename = args.log_filename
column_selected = args.column_selected
start_date = args.start_date
end_date = args.end_date
minimum_dependent = args.minimum_dependent
maximum_dependent = args.maximum_dependent
plot_filename = args.plot_filename

# Read logged data from the provided file
f = open(log_filename, 'r')

line = f.readline()
headers = line[:-1].split(',')

data = []
while True:
   line = f.readline()
   if line:
      data.append(line[:-1].split(','))
   else:
      break

f.close()

# Find the starting and ending indices for the date range specified
if start_date is None:
   start_idx = 1
else:
   start_idx = 1
   while start_date != data[start_idx][0][0:10]:
      start_idx += 1
      if start_idx >= len(data):
         msg = 'Specified start date not found in log file, check value '
         msg += 'and format, exiting ...'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()

if end_date is None:
   end_idx = len(data)
else:
   end_idx = len(data) - 1
   while end_date != data[end_idx][0][0:10]:
      end_idx -= 1
      if end_idx <= 1:
         msg = 'Specified end date not found in log file, check value '
         msg += 'and format, exiting ...'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()
   end_idx += 1

# If column to plot not provided, present headers to the user for selection
if column_selected is None:
   msg = 'Parameters available to plot:'
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   for column in range(1, len(headers)):
      msg = '   {0}) {1}'.format(column, headers[column])
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
   while True:
      column_selected = int(input('Selection: '))
      if column_selected < 1 or column_selected > len(headers)-1:
         continue
      else:
         break

# Parse timestamps from the first column of the logged data
days = numpy.empty(0, dtype=numpy.float64)
for idx in range(start_idx, end_idx):
   dt = \
      datetime.datetime.strptime(data[idx][0][0:10] + ' ' + data[idx][0][11:-1],
                                 '%Y-%m-%d %H:%M:%S.%f')
   day = \
      (dt.toordinal() - datetime.date(dt.year, 1, 1).toordinal() + 1) + \
      dt.hour/24 + \
      dt.minute/(24*60) + \
      dt.second/(24*60*60)
   days = numpy.append(days, day)

# Parse dependent data from the selected column of the logged data
dependent = numpy.empty(0, dtype=numpy.float64)
for idx in range(start_idx, end_idx):
   dependent = numpy.append(dependent, float(data[idx][column_selected]))

# Plot the specified dependent data as a function of time
if minimum_dependent is None or maximum_dependent is None:
   y_limits = None
else:
   y_limits = [minimum_dependent, maximum_dependent]

graphics.plot(days,
              dependent,
              xlabel = 'Day Number [UTC]',
              ylabel = headers[column_selected],
              ylim = y_limits,
              saveFilename = plot_filename)
