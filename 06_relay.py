#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

switch_pin = 12    # pin12

def setup():
	GPIO.setmode(GPIO.BOARD)         # Numbers pins by physical location
	GPIO.setup(switch_pin, GPIO.OUT)   # Set pin mode as output
	GPIO.output(switch_pin, GPIO.LOW) #turn off the switch to relay.

def loop():
	while True:
		print '...close'
		GPIO.output(switch_pin, GPIO.HIGH) #close switch to relay, relay closes it's switch.
		time.sleep(0.5)
		print 'open...' #open switch to relay, relay opens its switch.
		GPIO.output(switch_pin, GPIO.LOW)
		time.sleep(0.5)

def destroy():
	GPIO.output(switch_pin, GPIO.LOW)
	GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

