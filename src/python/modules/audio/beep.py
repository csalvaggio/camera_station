import audio
import time

def beep(frequency=440,
         number=1,
         duration=0.5,
         interbeep_pause=0,
         volume=0.1,
         waveform='square'):

   tone = audio.Tone(frequency=frequency, waveform=waveform, volume=volume)
   for beep in range(number):
      tone.play(loops=-1, maxtime=0, fade_ms=0)
      tone.fadeout(int(duration * 1000))
      time.sleep(duration)
      tone.stop()
      time.sleep(interbeep_pause)


if __name__ == '__main__':
   import audio

   audio.beep(440, 3, 0.5, 0.1, 1.0, 'square')
