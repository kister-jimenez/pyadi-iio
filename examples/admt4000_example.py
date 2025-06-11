# Copyright (C) 2020 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD

from calendar import c
from msilib.schema import Directory
from typing import List

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from time import sleep

from adi.tmc5240 import tmc5240
from adi.admt4000 import admt4000
from adi.context_manager import context_manager
import csv

class eval_admt4000(admt4000, tmc5240, context_manager):
    """ADMT4000 True power-on multiturn sensor with TMC5240 stepper motor driver"""

    _device_name = "eval_admt4000"
    def __init__(self, uri=""):
        """eval_admt4000 class constructor."""
        context_manager.__init__(self, uri, self._device_name)
        admt4000.__init__(self)
        tmc5240.__init__(self)

# Set up ADMT4000. Use correct URI.

# Use this with Raspberry Pi from a computer on the same network
# and make sure to use the correct IP of the  RPI.
# cal_setup = adi.admt4000(uri="ip:192.168.50.10")
iio_context = "serial:COM8,230400,8n1"

# Set enable_plot to True if you want to plot in real-time
enable_plot = True

full_turn = 360 #degrees

# Motor Driver Parameters
full_step_angle = 0.9
usteps_per_full_step = 256.0
amax = 131072
dmax = int(amax / 2) #3000 
vmax = 127438 * 2

# ADMT4000 Calibration Parameters
samples_size = 256
turns = 11
starting_turn = 15 #
starting_angle = 0 # degrees

################################################################################
# Use this with MCUs running tinyiiod and make sure to use the correct com port.
cal_setup = eval_admt4000(uri=iio_context)

angle_scale = cal_setup.angle.scale
temp_scale = cal_setup.temp.scale
temp_offset = cal_setup.temp.offset

curr_angle_raw = cal_setup.angle.raw
curr_angle = (curr_angle_raw) * angle_scale
curr_temp_raw = cal_setup.temp.raw
curr_temp = (curr_temp_raw + temp_offset) * temp_scale / 1000
print("ADMT4000 Current Readings")
print("Turn count: " + str(cal_setup.count.raw))
print("Angle: " + str(curr_angle_raw) + " (" + str(curr_angle) + " degrees)")
print("Temperature: " + str(curr_temp) + " C")

cal_setup.amax = amax
cal_setup.vmax = vmax
cal_setup.dmax = dmax

direction = - 1
cal_setup.usteps = usteps_per_full_step
cal_setup.full_step = full_step_angle
cal_setup.motor_direction = direction

full_turn_usteps = usteps_per_full_step * full_turn / full_step_angle
total_steps = turns * full_turn / full_step_angle
total_usteps = total_steps * usteps_per_full_step

u_steps = int(direction * total_usteps / samples_size)
print("Microsteps per sample: " + str(u_steps))


curr_abs_usteps = int(cal_setup.current_pos)
print("Current position in microsteps: " + str(curr_abs_usteps))

#ADMT4000 Angle represented as uSteps for reference offset calculation
angle_u_steps = (cal_setup.count.raw * full_turn + curr_angle) * usteps_per_full_step / full_step_angle
ref_u_steps_offset = angle_u_steps - direction * curr_abs_usteps
cal_setup.usteps_offset = ref_u_steps_offset  # offset for usteps
print("Microsteps to offset: " + str(curr_abs_usteps))
print("Current motor angle(0-360): " + str(cal_setup.current_angle_rot) + "°")
print("")
print("Positioning motor to starting position...")

target_starting_angle = starting_angle + starting_turn * full_turn
curr_angle_raw = cal_setup.angle.raw
curr_angle = (curr_angle_raw) * angle_scale + cal_setup.count.raw * full_turn
print("Current Motor Angle: " + str(cal_setup.current_angle) + "°")
print("Current ADMT4000 Angle: " + str(curr_angle) + "°")
print("Target starting angle: " + str(target_starting_angle) + "°")
cal_setup.target_angle = target_starting_angle
approx_delay = abs(cal_setup.target_pos - cal_setup.current_pos)*2 / cal_setup.vmax
print("Approximate delay for positioning: " + str(approx_delay) + " seconds")
sleep(approx_delay)
cal_setup.stop()
curr_angle_raw = cal_setup.angle.raw
curr_angle = (curr_angle_raw) * angle_scale + cal_setup.count.raw * full_turn
print("Current Motor Angle: " + str(cal_setup.current_angle) + "°")
print("Current ADMT4000 Angle: " + str(curr_angle) + "°")
print("Target starting angle: " + str(target_starting_angle) + "°")
data = []
angles = []
motor_angles = []

# Set up harmonic correction parameters
cal_setup.h8_mag_corr = 0
cal_setup.h8_phase_corr = 0
cal_setup.h8_corr_source = "user"

step_delay = abs(u_steps)*4 / vmax
curr_abs_usteps = int(cal_setup.current_pos)
print("Current position in microsteps: " + str(curr_abs_usteps))
print("Calibration Start...")
print("")
print("")

for i in range(256):
    curr_abs_usteps_corr =  ref_u_steps_offset + direction * curr_abs_usteps
    # curr_motor_angle = (curr_abs_usteps_corr % full_turn_usteps) * full_step_angle / usteps_per_full_step
    cal_setup.target_pos = curr_abs_usteps
    sleep(step_delay)
    curr_angle_raw = cal_setup.angle.raw
    curr_angle = (curr_angle_raw) * angle_scale
    print("")
    print("-------------------------------------------")
    print("Sample #" + str(i) + ":")
    print("Current microsteps: " + str(curr_abs_usteps))
    print("Current microsteps with offset: " + str(curr_abs_usteps_corr))
    print("Turn count: " + str(cal_setup.count.raw))
    print("ADMT4000 Raw Angle measurement: " + str(curr_angle_raw))
    print("ADMT4000 Angle measurement: " + str(curr_angle) + "°")
    # print("Current motor angle: " + str(curr_motor_angle) + "°")
    curr_motor_angle = cal_setup.current_angle_rot
    print("Current motor angle: " +  str(curr_motor_angle) + "°")
    
    angles.append(curr_angle)
    motor_angles.append(curr_motor_angle)

    data.append((curr_angle, curr_motor_angle))
    curr_abs_usteps += u_steps

# Record data in a CSV file
with open('calibration_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['PANG (degrees)', 'Ideal Angle'])  # Header

    for row in data:
        angle, motor_angle  = row
        writer.writerow([angle, motor_angle ])

# Plotting the data
import admt4000_cal

primary_angles = np.array(angles)
ref_angles = np.array(motor_angles)
scaled_harmonic_errors, harmonic_errors, angle_error, error_mag = admt4000_cal.admt4000_calibration(primary_angles, ref_angles)
corrected_angle_error, corrected_error_mag = admt4000_cal.calculate_corrections(angle_error, harmonic_errors, ref_angles)

print("Harmonic Errors (raw):", harmonic_errors)
print("Scaled Harmonic Errors:", scaled_harmonic_errors)

if enable_plot:
    admt4000_cal.print_cal_plots(primary_angles, angle_error, error_mag, corrected_angle_error, corrected_error_mag)

del cal_setup
