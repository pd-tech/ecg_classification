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
  with open(file, 'w') as output:
    for t, v, m in zip(time, volts, marker):
      output.write(str(t) + ' ' + str(v) + ' ' + str(m) + '\n')
      
def s50hz(time, volts, A):
  noise = []
  if "random" in str(A): A = random.uniform(0.8, 1.9)
  
  for t in time:
    y = A*sin(2*pi*49.9*t) + A*sin(2*pi*50*t) + A*sin(2*pi*50.1*t) + A*sin(2*pi*99.9*t) + A*sin(2*pi*100*t) + A*sin(2*pi*100.1*t)   # pro 49,9 - 50,1 Hz
    noise.append(y)
  #volts_sit = array(noise) + array(volts)
  return noise, [A]

def lin_d(time, volts, k):
  if "random" in str(k): k = random.uniform(1.0, 2.5)
  return k*array(time), [k]

def sin_d(time, volts, A, T):
  if "random" in str(A): A = random.uniform(0.8, 1.9)
  if "random" in str(T): T = random.uniform(10.0, 25.0) # perioda [s]

  drift_sin = A*sin(2*pi*1.0/T*array(time))
  volts_sdrift = drift_sin + array(volts)
  return A*sin(2*pi*1.0/T*array(time)), [A, T]

def abrupt(time, volts, A, k):
  if "random" in str(A): A = random.uniform(0.8, 1.9)
  if "random" in str(k): k = random.uniform(1.0, 2.5)  #[0.7, 1.0, 1.5, 2.0, 2.5]  # rychlost klesani

  return exp(-k*array(time)), [A, k]

def sqr_sig(time, volts, A, tl):
  if "random" in str(A): A = random.uniform(0.8, 1.9)
  if "random" in str(tl): tl = random.uniform(10.0, 25.0)  #tloustka pulzu

  return  A*signal.square(2*pi*tl*array(time)), [A, tl]

def myopotence(time, volts, k, fd, fh):
  if "random" in str(k): k = random.uniform(1.0, 2.5)
  if "random" in str(fd): fd = random.uniform(12.5, 29.9)
  if "random" in str(fh): fh = random.uniform(92.1, 108.9)
  
  freq = arange(20,100,0.1)  # Hz
  y_myop = (k*fh**4*freq**2)/((freq**2+fd**2)*(freq**2+fh**2)**2)

  return y_myop, [k, fd, fh]

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
  amplitude = 1.0
  k = 2.5
  T = 3.0
  tl = 3.5
  fd = 20.0
  fh = 100.0
    
  for parameter in sys.argv:
    if "in=" in parameter: input = parameter.split("=")[1]
    if "out=" in parameter: output = parameter.split("=")[1]
    if "noise=" in parameter: noises = [int(i)-1 for i in parameter.split("=")[1].split(',')]
    if "amp=" in parameter:
        if 'random' not in parameter: amplitude = float(parameter.split("=")[1])
        else: amplitude = parameter.split("=")[1]
    if "k=" in parameter:
        if 'random' not in parameter: k = float(parameter.split("=")[1])
        else: k = parameter.split("=")[1]
    if "T=" in parameter:
        if 'random' not in parameter: T = float(parameter.split("=")[1])
        else: T = parameter.split("=")[1]
    if "tl=" in parameter:
        if 'random' not in parameter: tl = float(parameter.split("=")[1])
        else: tl = parameter.split("=")[1]
    if "fd=" in parameter:
        if 'random' not in parameter: fd = float(parameter.split("=")[1])
        else: fd = parameter.split("=")[1]
    if "fh=" in parameter:
        if 'random' not in parameter: fh = float(parameter.split("=")[1])
        else: fh = parameter.split("=")[1]

  noiseDB = {'s50hz': [['volts'], amplitude], 'lin_d': [['volts'], k], 'sin_d': [['volts'], amplitude, T], 'abrupt': [['volts'], amplitude, k], 'sqr_sig': [['volts'], amplitude, tl], 'myopotence': [['volts'], k, fd, fh], 'GLOBAL': [['time'], ['volts'], ['marker']]}

  if os.path.isfile(input):
    list(noiseDB.values())[-1][0], list(noiseDB.values())[-1][1], list(noiseDB.values())[-1][2] = reader(input) # time, volts, marker = reader(input)
    volts2 = []
    output_fname = ""
    for noise in noises:
      apply_noise = globals()[list(noiseDB.keys())[noise]] # read function name dynamically from DB
      list(noiseDB.values())[noise][0], list(noiseDB.values())[noise][1:] = apply_noise(*(list(noiseDB.values())[-1][:2] + list(noiseDB.values())[noise][1:]))  # volts, optional_params = apply_noise()
      if not len(volts2) > 0: volts2 = array(list(noiseDB.values())[-1][1])
      volts2 = volts2 + array(list(noiseDB.values())[noise][0])
      output_fname += list(noiseDB.keys())[noise] + "=" + str(list(noiseDB.values())[noise][1:]) + "_"
    output_fname += os.path.basename(input) + "_" + output
    writer(output_fname, list(noiseDB.values())[-1][0], volts2, list(noiseDB.values())[-1][2])
  else:
    os.makedirs(output, exist_ok=True)
    for file in os.listdir(input):
      list(noiseDB.values())[-1][0], list(noiseDB.values())[-1][1], list(noiseDB.values())[-1][2] = reader(os.path.join(input, file)) # time, volts, marker = reader(input)
      volts2 = []
      output_fname = output + "/"
      for noise in noises:
        apply_noise = globals()[list(noiseDB.keys())[noise]] # read function name dynamically from DB
        list(noiseDB.values())[noise][0], list(noiseDB.values())[noise][1:] = apply_noise(*(list(noiseDB.values())[-1][:2] + list(noiseDB.values())[noise][1:]))  # volts, optional_params = apply_noise()
        if not len(volts2) > 0: volts2 = array(list(noiseDB.values())[-1][1])
        volts2 = volts2 + array(list(noiseDB.values())[noise][0])
        output_fname += list(noiseDB.keys())[noise] + "=" + str(list(noiseDB.values())[noise][1:]) + "_"
      output_fname += file
      writer(output_fname, list(noiseDB.values())[-1][0], volts2, list(noiseDB.values())[-1][2])


if __name__ == '__main__':
  main()
