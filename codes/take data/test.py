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
# 0 < fluc < 1  example fluc = 0.1 means the flucturation is 10%
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


from ServoPi_Minimal import PWM
pwm = PWM(0x40)
def single_channel_loop(i,dt,loop_value):
    i=max(1,i)
    i=min(17,i)
    for k in range(len(loop_value)):
        pwm.set_pwm(i,0,loop_value[k])


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

import csv
import numpy as np
pwm_value = np.array([])
with open('PWM_test.csv', encoding='utf-8') as f:
    for row in csv.reader(f, skipinitialspace=True):
        row=np.array(row)
        row=row.astype(np.int64)
        pwm_value = np.append(pwm_value,row)
        pwm_value = pwm_value.astype(int)

print(pwm_value)
give_single_channel(1,pwm_value[0])
give_single_channel(2,pwm_value[1])
give_single_channel(4,pwm_value[2])
give_single_channel(6,pwm_value[3])
give_single_channel(8,pwm_value[4])

