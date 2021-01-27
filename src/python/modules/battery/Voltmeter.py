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

      read(samples)
         The public method for reading the current voltage (the current
         voltage is an average of n samples specified by the calling
         method [default is samples=1])

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

   # Maximum Voltage 16.5 [V]
   R1 = 30000  # [Ohms]
   R2 = 7500   # [Ohms]

   # Maximum Voltage 26.4 [V]
   R1 = 33000  # [Ohms]
   R2 = 4700   # [Ohms]

   # Minimum reportable voltage
   MINIMUM_VOLTAGE = 2  # [V]

   # For the Raspberry Pi (3.3V) and Microchip Technology MCP3008 (10-bit)
   VOLTS_PER_COUNT = 3.3 / 1024  # [V/count]

   # Calibration for voltage divider circuit
   CALIBRATION_CONSTANT = VOLTS_PER_COUNT * (R1/R2 + 1)  # [V/count]


   def __init__(self, mcp3008_analog_input_channel=0,
                      spi_serial_clock_pin=11,
                      spi_serial_data_out_pin=9,
                      spi_serial_data_in_pin=10,
                      spi_chip_select_shutdown_input_pin=8,
                      calibration_constant=CALIBRATION_CONSTANT,
                      minimum_voltage=MINIMUM_VOLTAGE):

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
      self._minimum_voltage = minimum_voltage

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

   def read(self, samples=1):
      accumulated_adc_output = 0
      for sample in range(samples):
         RPi.GPIO.output(self._spi_chip_select_shutdown_input_pin,
                         RPi.GPIO.HIGH)
         RPi.GPIO.output(self._spi_serial_clock_pin,
                         RPi.GPIO.LOW)
         RPi.GPIO.output(self._spi_chip_select_shutdown_input_pin,
                         RPi.GPIO.LOW)

         command = self._mcp3008_analog_input_channel
         command |= 0x18
         command <<= 3
         for i in range(5):
            if (command & 0x80):
               RPi.GPIO.output(self._spi_serial_data_in_pin,
                               RPi.GPIO.HIGH)
            else:
               RPi.GPIO.output(self._spi_serial_data_in_pin,
                               RPi.GPIO.LOW)
            command <<= 1
            RPi.GPIO.output(self._spi_serial_clock_pin,
                            RPi.GPIO.HIGH)
            RPi.GPIO.output(self._spi_serial_clock_pin,
                            RPi.GPIO.LOW)

         adc_output = 0
         for i in range(12):
            RPi.GPIO.output(self._spi_serial_clock_pin,
                            RPi.GPIO.HIGH)
            RPi.GPIO.output(self._spi_serial_clock_pin,
                            RPi.GPIO.LOW)
            adc_output <<= 1
            if (RPi.GPIO.input(self._spi_serial_data_out_pin)):
               adc_output |= 0x1

         RPi.GPIO.output(self._spi_chip_select_shutdown_input_pin,
                         RPi.GPIO.HIGH)

         adc_output >>= 1

         accumulated_adc_output += adc_output

      voltage = self._calibration_constant * accumulated_adc_output / samples

      if voltage < self._minimum_voltage:
         return None
      else:
         return voltage

   def close(self):
      # Cleaning up/resetting the GPIO pins to some default state has
      # unforeseen consequences on other devices, so to avoid this,
      # even though it seems prudent to do this when dicarding the
      # voltmeter object, do not call the GPIO clenup routine at this
      # point in the process
      #RPi.GPIO.cleanup()
      pass



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
            voltage = voltmeters[channel].read(samples=16)
            if voltage:
               msg += 'Channel {0}: {1:.2f} [V]'.format(channel+1, voltage)
               msg += '\n'
            else:
               msg += 'Channel {0}: n/a'.format(channel+1, voltage)
               msg += '\n'
         msg += '\n'
         sys.stdout.write(msg)
         time.sleep(5)

   except KeyboardInterrupt:
      msg = '\n'
      sys.stdout.write(msg)
      for voltmeter in voltmeters:
         voltmeter.close()
