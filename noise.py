#!/usr/bin/env python3

import os
import sys
import csv
import matplotlib.pyplot as plt
from numpy import *
from scipy import signal
import random
#import numpy as np
#%pylab inline


def reader(file):
  time = []
  volts = []
  marker = []
  
  with open(file, newline='') as csvfile:
    print("Reading file " + file)
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        time.append(float(row[0]))
        volts.append(float(row[1]))
        marker.append(int(row[2]))
  return time, volts, marker
  
def writer(file, time, volts, marker):
  print("Writing file " + file)
  with open(file, 'a') as output:
    for t, v, m in zip(time, volts, marker):
      output.write(str(t) + ' ' + str(v) + ' ' + str(m) + '\n')
      
def sit(input, output, A):
  noise = []
  A = random.uniform(0.8, 1.9)
  
  time, volts, marker = reader(input)
  
  for t in time:
    y = A*sin(2*pi*49.9*t) + A*sin(2*pi*50*t) + A*sin(2*pi*50.1*t) + A*sin(2*pi*99.9*t) + A*sin(2*pi*100*t) + A*sin(2*pi*100.1*t)   # pro 49,9 - 50,1 Hz
    noise.append(y)
  volts_sit = array(noise) + array(volts)
  
  #fig, ax = plt.subplots()
  #ax.plot(time[0:len(time)], volts2[0:len(time)])
  #plt.show()
  
  writer(output, time, volts_sit, marker)

def lin_d(input, output, k):
  k = random.uniform(1.0, 2.5)

  time, volts, marker = reader(input)

  volts_ldrift = k*array(time) + array(volts)

  writer(output, time, volts_ldrift, marker)

def sin_d(input, output, A):
  time, volts, marker = reader(input)
  A = random.uniform(0.8, 1.9)

  T = random.uniform(2.1, 3.8) # perioda [s]

  drift_sin = A*sin(2*pi*1.0/T*array(time))
  volts_sdrift = drift_sin + array(volts)
  writer(output, time, volts_sdrift, marker)

def abrupt(input, output, A):
  time, volts, marker = reader(input)
  
  A = random.uniform(0.8, 1.9)
  k = random.uniform(0.7, 2.5)  #[0.7, 1.0, 1.5, 2.0, 2.5]  # rychlost klesani

  abr = exp(-k*array(time))
  volts_exp = volts + abr

  writer(output, time, volts_exp, marker)

def sqr_sig(input, output, A):
  time, volts, marker = reader(input)

  A = random.uniform(0.8, 1.9)
  tl = random.uniform(3.5, 6.0)  #tloustka pulzu

  y_obd = A*signal.square(2*pi*tl*array(time))
  volts_obd = y_obd + volts

  writer(output, time, volts_obd, marker)

def myopotence(input, output):#???
  time, volts, marker = reader(input)

  freq = arange(20,100,0.1)  # Hz
  k = 2.5   #volitelné
  fd = 20.0    # volitelné
  fh = 100.0  #volitelné 
  y_myop = (k*fh**4*freq**2)/((freq**2+fd**2)*(freq**2+fh**2)**2) # ???

def main():
  if len(sys.argv) <= 1:
    print("""Pouziti: {0} in=[vstupni soubor/slozka] out=[vystupni soubor/slozka] noise=[typ sumu] amp=[rozkmit]
          
          Volitelne parametry: out, amp
          
          Typy sumu:
          1) Sitovy
          2) Linearni drift
          3) Sinusovy drift
          4) Abrupt
          5) Obdelnikovy signal
          6) Myopotencial
          
          Priklad: noise=1""".format(sys.argv[0]))
    return
    
  output = ""
  amplitude = 1
    
  for parameter in sys.argv:
    if "in=" in parameter:
      print(parameter.split("=")[1])
      input = parameter.split("=")[1]
    if "out=" in parameter:
      output = parameter.split("=")[1]
    if "noise=" in parameter:
      noise = int(parameter.split("=")[1])
    if "amp=" in parameter:
      amplitude = int(parameter.split("=")[1])
        
  if noise == 1:
    if os.path.isfile(input):
      sit(input, output, amplitude)
    else:
      os.makedirs(output, exist_ok=True)
      for file in os.listdir(input):
        sit(input + "/" + file, output + "/" + str(noise) + "_" + file, amplitude)
    
  if noise == 2:
    if os.path.isfile(input):
      lin_d(input, output, amplitude)
    else:
      os.makedirs(output, exist_ok=True)
      for file in os.listdir(input):
        lin_d(input + "/" + file, output + "/" + str(noise) + "_" + file, amplitude)
          
  if noise == 3:
    if os.path.isfile(input):
      sin_d(input, output, amplitude)
    else:
      os.makedirs(output, exist_ok=True)
      for file in os.listdir(input):
        sin_d(input + "/" + file, output + "/" + str(noise) + "_" + file, amplitude)

  if noise == 4:
    if os.path.isfile(input):
      abrupt(input, output, amplitude)
    else:
      os.makedirs(output, exist_ok=True)
      for file in os.listdir(input):
        abrupt(input + "/" + file, output + "/" + str(noise) + "_" + file, amplitude)
          
  if noise == 5:
    if os.path.isfile(input):
      sqr_sig(input, output, amplitude)
    else:
      os.makedirs(output, exist_ok=True)
      for file in os.listdir(input):
        sqr_sig(input + "/" + file, output + "/" + str(noise) + "_" + file, amplitude)

if __name__ == '__main__':
  main()