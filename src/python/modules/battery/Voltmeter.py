import sys
import RPi.GPIO

class Voltmeter(object):
   """
   title::
      Voltmeter

   description::
      A public class used to create a Raspberry Pi voltmeter based on the
      designed created at ...

         https://kookye.com/2017/06/01/design-a-voltmeter-with-the-raspberry
                                                 -pi-board-and-voltage-sensor/

      IMPORTANT:
         The acceptable input analog voltage is 0 to 16.5 [VDC].  Any input
         exceeding this range WILL DAMAGE the Raspberry Pi.

   attributes::
      
   methods::
      analog_input_channel()
      analog_input_channel(mcp3008_analog_input_channel)
         The public getter and setter methods for the input channel used
         on the MCP3008 analog-to-digital converter chip

      read()
         The public method for reading the current voltage

      close()
         The public method to close the voltmeter/clean up the GPIO

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

   def __init__(self, mcp3008_analog_input_channel=0,
                      spi_serial_clock_pin=11,
                      spi_serial_data_out_pin=9,
                      spi_serial_data_in_pin=10,
                      spi_chip_select_shutdown_input_pin=8,
                      calibration_constant=(3.3 / 1024) * 5):

      if mcp3008_analog_input_channel < 0 or mcp3008_analog_input_channel > 7:
         msg = '*** ERROR *** '
         msg += 'Specified MCP3008 analog input channel '
         msg += '({0}) '.format(mcp3008_analog_input_channel)
         msg += 'out of range [0, 7]'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()

      self._mcp3008_analog_input_channel = mcp3008_analog_input_channel

      self._calibration_constant = calibration_constant

      self._spi_serial_clock_pin = \
         spi_serial_clock_pin
      self._spi_serial_data_out_pin = \
         spi_serial_data_out_pin
      self._spi_serial_data_in_pin = \
         spi_serial_data_in_pin
      self._spi_chip_select_shutdown_input_pin = \
         spi_chip_select_shutdown_input_pin

      # Set up GPIO
      RPi.GPIO.setwarnings(False)
      RPi.GPIO.setmode(RPi.GPIO.BCM)

      # Set up the SPI interface pins
      RPi.GPIO.setup(self._spi_serial_data_in_pin, RPi.GPIO.OUT)
      RPi.GPIO.setup(self._spi_serial_data_out_pin, RPi.GPIO.IN)
      RPi.GPIO.setup(self._spi_serial_clock_pin, RPi.GPIO.OUT)
      RPi.GPIO.setup(self._spi_chip_select_shutdown_input_pin, RPi.GPIO.OUT)

   @property
   def analog_input_channel(self):
      return self._mcp3008_analog_input_channel

   @analog_input_channel.setter
   def analog_input_channel(self, mcp3008_analog_input_channel):
      if mcp3008_analog_input_channel < 0 or mcp3008_analog_input_channel > 7:
         msg = '*** ERROR *** '
         msg += 'Specified MCP3008 analog input channel '
         msg += '({0}) '.format(mcp3008_analog_input_channel)
         msg += 'out of range [0, 7]'
         msg += '\n'
         sys.stderr.write(msg)
         sys.stderr.flush()
         sys.exit()

      self._mcp3008_analog_input_channel = mcp3008_analog_input_channel

   def read(self):
      RPi.GPIO.output(self._spi_chip_select_shutdown_input_pin, RPi.GPIO.HIGH)
      RPi.GPIO.output(self._spi_serial_clock_pin, RPi.GPIO.LOW)
      RPi.GPIO.output(self._spi_chip_select_shutdown_input_pin, RPi.GPIO.LOW)

      command = self._mcp3008_analog_input_channel
      command |= 0x18
      command <<= 3
      for i in range(5):
         if (command & 0x80):
            RPi.GPIO.output(self._spi_serial_data_in_pin, RPi.GPIO.HIGH)
         else:
            RPi.GPIO.output(self._spi_serial_data_in_pin, RPi.GPIO.LOW)
         command <<= 1
         RPi.GPIO.output(self._spi_serial_clock_pin, RPi.GPIO.HIGH)
         RPi.GPIO.output(self._spi_serial_clock_pin, RPi.GPIO.LOW)

      adc_output = 0
      for i in range(12):
         RPi.GPIO.output(self._spi_serial_clock_pin, RPi.GPIO.HIGH)
         RPi.GPIO.output(self._spi_serial_clock_pin, RPi.GPIO.LOW)
         adc_output <<= 1
         if (RPi.GPIO.input(self._spi_serial_data_out_pin)):
            adc_output |= 0x1

      RPi.GPIO.output(self._spi_chip_select_shutdown_input_pin, RPi.GPIO.HIGH)

      adc_output >>= 1

      if adc_output == 0:
         return None
      else:
         return self._calibration_constant * adc_output

   def close(self):
      RPi.GPIO.cleanup()



if __name__ == '__main__':

   import sys
   import time

   import battery

   try:
      voltmeters = []
      number_of_channels = 8
      for channel in range(number_of_channels):
         voltmeters.append(battery.Voltmeter(channel))
      time.sleep(2)

      while True:
         msg = 'VOLTAGES'
         msg += '\n'
         for channel in range(number_of_channels):
            voltage = voltmeters[channel].read()
            if voltage:
               msg += 'Channel {0}: {1:.2f} [V]'.format(channel+1, voltage)
               msg += '\n'
            else:
               msg += 'Channel {0}: n/a'.format(channel+1, voltage)
               msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         time.sleep(1)

   except KeyboardInterrupt:
      msg = '\n'
      sys.stdout.write(msg)
      for voltmeter in voltmeters:
         voltmeter.close()
