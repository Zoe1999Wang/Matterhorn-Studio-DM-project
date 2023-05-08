"""
================================================
Zoe Wang 16-Channel PWM Driver test code v2
25.06.2022
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

def turn_channels_on():
    for i in range (1,17,1):
        pwm.set_pwm(i,0,4095)
    

def turn_channels_off():
    for i in range (1,17,1):
        pwm.set_pwm(i,0,0)
        
def give_all_channels(value): 
    value=max(0,value)
    value=min(4095,value)
    for i in range (1,17,1):
        pwm.set_pwm(i,0,value)
        
def give_single_channel(i,value):
    value=max(0,value)
    value=min(4095,value)
    i=max(1,i)
    i=min(17,i)
    pwm.set_pwm(i,0,value)
    
def test(i):
    i=max(1,i)
    i=min(17,i)
    for i in range (1,17,1):
        pwm.set_pwm(i,0,0)
        time.sleep(1)
        pwm.set_pwm(i,0,4095)
        time.sleep(1)
        pwm.set_pwm(i,0,0)
        time.sleep(1)
        pwm.set_pwm(i,0,4095)
        time.sleep(1)
        pwm.set_pwm(i,0,0)
import numpy as np
import math

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

# 0 < fluc < 1  example fluc = 0.1 means the fluctuation is 10%
#this loop value is to find the values to change while in the annealing process
#to use it, for example, type 'loop_value=loop_value(4095,0,0.1)', this will give the values from 4095 to 0 with 0.1 fluctuation.

from ServoPi_Minimal import PWM
pwm = PWM(0x40)
def single_channel_loop(i,dt,loop_value):
    i=max(1,i)
    i=min(17,i)
    for k in range(len(loop_value)):
        pwm.set_pwm(i,0,loop_value[k])

#single_channel_loop is used to do the annealing process, time for each step in the loop can be changed by dt here
#to use it, for example, type 'single_channel_loop(1,0.3,pwm.set_pwm,loop_value)' to do the annealing on channel 1 with each step=0.3s

from ServoPi_Minimal import PWM
from threading import Timer
import time
pwm = PWM(0x40)
def single_channel_loop(i,second,func,loop_value):
    i=max(1,i)
    i=min(17,i)
    for k in range(len(loop_value)):
        timer = Timer(second,func,[i,0,loop_value[k]])
        timer.start()
        timer.join()

A = np.random.randint(low=0,high=1000,size=(5,1), dtype=np.int64)
give_single_channel(1,A[0])
give_single_channel(2,A[1])
give_single_channel(3,A[2])
give_single_channel(4,A[3])
give_single_channel(5,A[4])

#can also give the fixed values we want to one DM to add the aberration to the system

import csv
import numpy as np
pwm_value = np.array([])
with open('PWM_test.csv', encoding='utf-8') as f:
    for row in csv.reader(f, skipinitialspace=True):
        row=np.array(row)
        row=row.astype(np.int64)
        pwm_value = np.append(pwm_value,row)
        pwm_value = pwm_value.astype(int)

import csv
from pickletools import int4
import numpy as np
import os
import time
FileName=r'PWM_test.csv'
last_modified_time = os.stat(FileName).st_mtime
channel_array = np.array([1,2,3,4,5])
#channel_array = np.array([6,7,9,11,13]) for another 5-actuator DM
#channel_array = np.array([6,7,8,9,10,11,12,13,14]) for another 9-actuator DM

while True:
    if last_modified_time!=os.stat(FileName).st_mtime:
        with open('PWM_test.csv', encoding='utf-8') as f:
            i = 0
            for row in csv.reader(f, skipinitialspace=False):
                row=np.array(row,dtype=np.int64)
                give_single_channel(channel_array[i],row)
                i = i+1
            last_modified_time= os.stat(FileName).st_mtime
#detect if there is new file on laptop then decide to change the voltage on DM, this code must be running with WinSCP software on pi together.
