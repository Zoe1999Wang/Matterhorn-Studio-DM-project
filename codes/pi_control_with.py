"""
================================================
Zoe Wang 16-Channel PWM Driver code v3
10.08.2023
================================================
"""

import time

from ServoPi_Minimal import PWM

pwm = PWM(0x40)
pwm.set_pwm_freq(1000)
print("PWM Frequency set to 1000Hz")
pwm.output_enable()

from threading import Timer
import time
import numpy as np
import math
import os
import csv
from pickletools import int4

def give_single_channel(i,value):
    value=max(0,value)
    value=min(4095,value)
    i=max(1,i)
    i=min(17,i)
    pwm.set_pwm(i,0,value)

def loop_value(start,end,fluc):
    start = max(0,start)
    start = min(4095,start)
    end = max(0,end)
    end = min(4095,end)
    loop_value = np.array([])
    if start == end:
        loop_value = np.append(loop_value, start)
    if start > end:
        loop_value = np.append(loop_value, start)
        for i in range(1,12):
            val = math.ceil(start/pow(2,i))
            if int(val) <= end:
                loop_value = np.append(loop_value, end)
                return loop_value.astype(int)
            if int(val) == 2:
                loop_value = np.append(loop_value, 2)
                loop_value = np.append(loop_value, 0)
                return loop_value.astype(int)
            loop_value = np.append(loop_value, val)
            val_upfluc = math.ceil(val+fluc*val)
            val_upfluc = min(4095,val_upfluc)
            loop_value = np.append(loop_value, val_upfluc)
            val_downfluc = math.ceil(val-fluc*val)
            val_downfluc = max(0,val_downfluc)
            loop_value = np.append(loop_value, val_downfluc)

    if start < end:
            middle = end
            end = start
            start = middle
            if start < end:
                print('error')
            loop_value = np.append(loop_value, start)
            for i in range(1,12):
                val = math.ceil(start/pow(2,i))
                if int(val) <= end:
                    loop_value = np.append(loop_value, end)
                    loop_value = np.flipud(loop_value)
                    return loop_value.astype(int)
                if int(val) == 2:
                    loop_value = np.append(loop_value, 0)
                    loop_value = np.flipud(loop_value)
                    return loop_value.astype(int)
                loop_value = np.append(loop_value, val)
                val_upfluc = math.ceil(val+fluc*val)
                val_upfluc = min(4095,val_upfluc)
                loop_value = np.append(loop_value, val_upfluc)
                val_downfluc = math.ceil(val-fluc*val)
                val_downfluc = max(0,val_downfluc)
                loop_value = np.append(loop_value, val_downfluc)


def single_channel_loop(i,second,func,loop_value):
    i=max(1,i)
    i=min(17,i)
    for k in range(len(loop_value)):
        timer = Timer(second,func,[i,loop_value[k]])
        timer.start()
        timer.join()

FileName_PWM = 'PWM_test.csv'
FileName_Annealing = 'do_annealing.csv'
last_modified_time_PWM = os.stat(FileName_PWM).st_mtime
last_modified_time_Annealing = os.stat(FileName_Annealing).st_mtime
channel_array = np.array([1,2,3,4,5])
loop_val = loop_value(4095,0,0.3)
while True:
    if last_modified_time_PWM != os.stat(FileName_PWM).st_mtime:
        with open(FileName_PWM, encoding='utf-8') as f:
            i = 0
            for row in csv.reader(f, skipinitialspace=False):
                row = np.array(row, dtype=np.int64)
                give_single_channel(channel_array[i], row) 
                i = i + 1
            last_modified_time_PWM = os.stat(FileName_PWM).st_mtime

    if last_modified_time_Annealing != os.stat(FileName_Annealing).st_mtime:
        with open(FileName_Annealing, encoding='utf-8') as f:
            
            single_channel_loop(1,0.3,give_single_channel,loop_val)
            single_channel_loop(2,0.3,give_single_channel,loop_val)
            single_channel_loop(3,0.3,give_single_channel,loop_val)
            single_channel_loop(4,0.3,give_single_channel,loop_val)
            single_channel_loop(5,0.3,give_single_channel,loop_val)

            last_modified_time_Annealing = os.stat(FileName_Annealing).st_mtime


#single_channel_loop is used to do the annealing process, time for each step in the loop can be changed by dt here
#to use it, for example, type 'single_channel_loop(1,0.3,pwm.set_pwm,loop_value)' to do the annealing on channel 1 with each step=0.3s
