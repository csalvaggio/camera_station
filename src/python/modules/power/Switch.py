import sys
import RPi.GPIO

class Switch(object):
   """
   title::
      Switch

   description::
      A public class used to create a Raspberry Pi-controlled power switch
      using a HiLetgo relay

   attributes::
      control_pin
         The GPIO (BCM) pin number to use as the control [default is 21]
      load_connection
         The terminal on the HiLetgo relay to which the load is
         connected, either normally open ('no') or normally closed ('nc')
         [default is 'no']
      
   methods::
      control_pin()
      control_pin(control_pin)
         The public getter and setter methods for the control pin used
         to command the relay

      load_connection()
      load_connection(load_connection)
         The public getter and setter methods indicating which terminal
         the load is connected to on the relay

      state()
      state(state)
         The public getter and setter methods for the current state
         of the relay (0 is open, 1 is closed)

      position(state)
         The public method to set the current state of the relay (switch
         position) (0 is open, 1 is closed)

      close()
         The public method to close the switch

   associated methods::
      None

   author::
      Carl Salvaggio, Ph.D.

   copyright:
      Copyright (C) 2020, Rochester Institute of Technology

   license::
      GPL

   version::
      1.0.0

   disclaimer::
      This source code is provided "as is" and without warranties as to 
      performance or merchantability. The author and/or distributors of 
      this source code may have made statements about this source code. 
      Any such statements do not constitute warranties and shall not be 
      relied on by the user in deciding whether to use this source code.
      
      This source code is provided without any express or implied warranties 
      whatsoever. Because of the diversity of conditions and hardware under 
      which this source code may be used, no warranty of fitness for a 
      particular purpose is offered. The user is advised to test the source 
      code thoroughly before relying on it. The user must assume the entire 
      risk of using the source code.
   """

   def __init__(self, control_pin=21, load_connection='no'):
      # Set up GPIO
      RPi.GPIO.setwarnings(False)
      RPi.GPIO.setmode(RPi.GPIO.BCM)

      # Set up the input pin
      RPi.GPIO.setup(control_pin, RPi.GPIO.OUT)

      # Define member attributes
      self._control_pin = control_pin
      self.load_connection = load_connection
      if self._load_connection == 'no':
         self._state = 0
      else:
         self._state = 1

   @property
   def control_pin(self):
      return self._control_pin

   @control_pin.setter
   def control_pin(self, control_pin):
      self._control_pin = control_pin

   @property
   def load_connection(self):
      return self._load_connection

   @load_connection.setter
   def load_connection(self, load_connection):
      if load_connection.lower() == 'no' or load_connection.lower() == 'nc':
         self._load_connection = load_connection.lower()
      else:
         msg = '*** ERROR *** '
         msg += 'Specified load connection '
         msg += '({0}) '.format(load_connection)
         msg += 'is invalid [nc, no]'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()

   @property
   def state(self):
      return self._state

   @state.setter
   def state(self, state):
      self._state = state
      if self._load_connection == 'no':
         if self._state:
            RPi.GPIO.output(self._control_pin, RPi.GPIO.HIGH)
         else:
            RPi.GPIO.output(self._control_pin, RPi.GPIO.LOW)
      else:
         if self._state:
            RPi.GPIO.output(self._control_pin, RPi.GPIO.LOW)
         else:
            RPi.GPIO.output(self._control_pin, RPi.GPIO.HIGH)

   def position(self, state):
      self.state = state

   def close(self):
      pass



if __name__ == '__main__':

   import argparse
   import sys
   import time

   import power

   description = 'Switch (on/off) script'
   parser = argparse.ArgumentParser(description=description)

   help_message = 'desired state (ON|OFF) '
   help_message += '[default is ON]'
   parser.add_argument('-s', '--state',
                       dest='desired_state',
                       type=str,
                       default='ON',
                       help=help_message)

   args = parser.parse_args()
   desired_state = args.desired_state.upper()

   if desired_state != 'ON' and desired_state != 'OFF':
      msg = 'Invalid option for desired state: {0}'.format(desired_state)
      msg += '\n'
      msg += 'Exiting ...'
      msg += '\n'
      sys.stdout.write(msg)
      sys.stdout.flush()
      sys.exit()

   msg = 'Creating switch ...'
   msg += '\n'
   sys.stdout.write(msg)
   switch = power.Switch(control_pin=21, load_connection='nc')
   time.sleep(5)

   msg = 'Turning switch {0}'.format(desired_state)
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
   switch.position(1) if desired_state == 'ON' else switch.position(0)
