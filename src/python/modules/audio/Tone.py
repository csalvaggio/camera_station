import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.mixer

import math
import numpy

class Tone(pygame.mixer.Sound):
   def __init__(self, frequency, waveform="square", volume=0.1):
      self.frequency = frequency
      self.waveform = waveform

      pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
      pygame.init()
      pygame.mixer.Sound.__init__(self, array=self.signal())

      self.set_volume(volume)

   def signal(self):
      # Compute the period ... sampling frequency / tone frequency
      period = int(round(pygame.mixer.get_init()[0] / self.frequency))

      # Compute the signal amplitude ... 2**(|size|-1) - 1
      amplitude = 2**(abs(pygame.mixer.get_init()[1])-1) - 1

      # Set up the 2-channel (stereo) signal array
      signal = numpy.zeros(period, dtype=numpy.int16)

      # Fill the 2-channel (stereo) signal array with the desired waveform
      if self.waveform == "square":
         for time in range(period):
            if time < period/2:
               signal[time] = amplitude
            else:
               signal[time] = -amplitude
      elif self.waveform == "sine":
         for time in range(period):
            angle = (time/period) * (2*math.pi)
            signal[time] = math.sin(angle) * amplitude
      else:
         msg = "Unsupported waveform: {0}".format(self.waveform)
         raise ValueError(msg)

      return signal


if __name__ == '__main__':
   import audio
   import time

   duration = 0.5 # [s]
   frequency = 440 # [Hz]
   tone = audio.Tone(frequency=frequency, waveform="square", volume=0.1)
   tone.play(loops=-1, maxtime=0, fade_ms=0)
   tone.fadeout(int(duration * 1000))
   time.sleep(duration)
   tone.stop()
