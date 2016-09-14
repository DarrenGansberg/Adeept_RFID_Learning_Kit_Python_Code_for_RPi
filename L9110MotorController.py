#!/usr/bin/env python

#########################################
# L9110 Motor Controller Driver
#
# Description: 
# The L9110MotorController class defined
# in this file can be used to control 
# a motor attached to a L9110 motor drive
# controller IC on a Raspberry Pi (RPi). 
#
# To use create instance of the class passing
# the input pin A and B connected from RPi 
# to chip, and start speed (should be 0.0 to 100.0) 
# a step value for speed changes (between 0.0 and 100.0)
# and the initial direction for the motor (0 = fwd, 1 = backwards)
#
#
# Copyright (C) 2016, Darren Gansberg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the folowing conditions are met:
#
# 1. Redistribution of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this 
# list of conditions and the following disclaimer in the documentation
# and/or other materals provided with the distribution. 
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTIONS "AS IS" AND 
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTIONS BE LIABILE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL OR EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORS (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



import RPi.GPIO as GPIO
import time

class L9110MotorController(object):
	DIRECTION_FWD = 0
	DIRECTION_BWD = 1
	STATUS_RUNNING = 1
	STATUS_STOPPED = 0
	def __init__(self, input_a, input_b, start_speed = 100.0, speed_change = 10.0, start_direction = 0):
		#if speed_change < 0.0 or speed_change > 100.0:
			#raise ValueError("Speed change must be between 0.0 and 100.0")
		GPIO.setmode(GPIO.BOARD)
		self._input_a_original = GPIO.gpio_function(input_a)
		self._input_b_original = GPIO.gpio_function(input_b)
		self._input_a = input_a
		self._input_b = input_b
		GPIO.setup(self._input_a, GPIO.OUT)
		GPIO.setup(self._input_b, GPIO.OUT)
		self._direction = start_direction
		self._pwm = None
		self._pwm_duty_cycle = 100.0 - start_speed
		self._pwm_duty_cycle_step = speed_change
		self._status = L9110MotorController.STATUS_STOPPED

	def Start(self):
		if self._status == L9110MotorController.STATUS_STOPPED:
			if self._direction == L9110MotorController.DIRECTION_FWD:
				#to go fwd input_a must be high. PWM is used 
				#to control motor speed. By flipping input b for a 
				#period of time input a goes low. by cutting power, speed 
				#is reduced. 
				GPIO.output(self._input_a, GPIO.HIGH)
				GPIO.output(self._input_b, GPIO.LOW)
				time.sleep(0.1)
				self._pwm = GPIO.PWM(self._input_b, 2000)	
			elif self._direction == L9110MotorController.DIRECTION_BWD:
				GPIO.output(self._input_b, GPIO.HIGH)
				GPIO.output(self._input_a, GPIO.LOW)				
				time.sleep(0.1)
				self._pwm = GPIO.PWM(self._input_a, 2000)								
			self._pwm.start(self._pwm_duty_cycle)
			self._status = L9110MotorController.STATUS_RUNNING

				
	def IncreaseSpeed(self):
		#to increase the speed reduce the pulse width per cycle used for 
		#controlling the speed. By reducing the pulse width of the pin 
		#used to control speed, the pin that supplies the movement voltage/current
		#is HIGH longer, meaning that the motor goes faster.
		#Full speed reached when pulse width of speed control pin is 0.
		if self._pwm_duty_cycle > 0.0:
			self._pwm_duty_cycle -= self._pwm_duty_cycle_step
			if self._status == L9110MotorController.STATUS_RUNNING:
				self._pwm.ChangeDutyCycle(self._pwm_duty_cycle)
	
	def DecreaseSpeed(self):
		if self._pwm_duty_cycle < 100.0:
			self._pwm_duty_cycle += self._pwm_duty_cycle_step
		if self._status == L9110MotorController.STATUS_RUNNING:
			self._pwm.ChangeDutyCycle(self._pwm_duty_cycle)

	def ChangeDirection(self):
		self.Stop()
		time.sleep(0.1)
		if self._direction == L9110MotorController.DIRECTION_FWD:
			self._direction = L9110MotorController.DIRECTION_BWD
		elif self._direction == L9110MotorController.DIRECTION_BWD:
			self._direction = L9110MotorController.DIRECTION_FWD
		self.Start()
	
	def Stop(self):
		if self._status == L9110MotorController.STATUS_RUNNING:
			self._pwm.stop()
			GPIO.output(self._input_a, GPIO.LOW)
			GPIO.output(self._input_b, GPIO.LOW)
			self._status = L9110MotorController.STATUS_STOPPED
		else:
			pass #do nothing if not running.	

	def Shutdown(self):
		GPIO.output(self._input_a, self._input_a_original)
                GPIO.output(self._input_b, self._input_b_original)
      
def destroy():
	GPIO.cleanup()             # Release resource

if __name__ == '__main__':     # Program start from here
	try:
		motor_controller = L9110MotorController(16,18,100.0,2.0, L9110MotorController.DIRECTION_FWD)
		motor_controller.Start()
		
		while True:		
			time.sleep(5.0)
			motor_controller.ChangeDirection()
			
	except KeyboardInterrupt:
		motor_controller.Shutdown()
		destroy()

