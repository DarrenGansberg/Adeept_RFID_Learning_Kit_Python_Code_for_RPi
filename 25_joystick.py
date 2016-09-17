#!/usr/bin/env python

import ADC0832
import RPi.GPIO as GPIO
import time

btn = 15	# Define button pin


def setup():
	ADC0832.setup()				# Setup ADC0832
	GPIO.setmode(GPIO.BOARD)	# Numbers GPIOs by physical location
	GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Setup button pin as input an pull it up
	GPIO.add_event_detect(btn, GPIO.FALLING, callback=button_pressed, bouncetime=100)
	global state
	state = ['up', 'down', 'left', 'right']	

def button_pressed(channel):
	print("button pressed")
	
def getResult():	#get joystick result
	x_axis = 0
	y_axis = 1
	x = ADC0832.getResult(x_axis)	
	if x == 0:
		return 4
	elif x == 255: 
		return 3
	y = ADC0832.getResult(y_axis)
	if y == 0:
		return 1
	elif y == 255:
		return 2

	#if ADC0832.getResult(1) == 0:
	#	return 1		#up
	#if ADC0832.getResult(1) == 255:
	#	return 2		#down

	#if ADC0832.getResult(0) == 0:
	#	return 3		#left
	#if ADC0832.getResult(0) == 255:
	#	return 4		#right

	#if GPIO.input(btn) == 1:
	#	print 'Button is pressed!'		# Button pressed

def loop():
	while True:
		tmp = getResult()
		if tmp != None:
			print state[tmp - 1]
		time.sleep(0.1)
def destroy():
	GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
	try:
		setup()
		loop()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
