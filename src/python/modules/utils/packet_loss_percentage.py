import subprocess

def packet_loss_percentage(hostname='8.8.8.8', count=10):
   process = \
      subprocess.Popen(['ping', '-c', str(count), hostname],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
   stdout, stderr = process.communicate()

   packet_loss_percentage = \
      float([x for x in stdout.decode('utf-8').split('\n') \
            if x.find('packet loss') != -1][0].split('%')[0].split(' ')[-1])

   return packet_loss_percentage



if __name__ == '__main__':
   import sys
   import utils

   packet_loss_percentage = utils.packet_loss_percentage()

   msg = 'Packet loss is {0}%'.format(packet_loss_percentage)
   msg += '\n'
   sys.stdout.write(msg)
   sys.stdout.flush()
