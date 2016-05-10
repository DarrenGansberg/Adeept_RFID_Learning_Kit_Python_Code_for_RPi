#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

BZRPin = 12

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
	GPIO.setup(BZRPin, GPIO.OUT)   # Set pin mode as output
	GPIO.output(BZRPin, GPIO.LOW)

def loop():	
	while True:
		for f in range(100, 2000, 100):
			p.ChangeFrequency(f)
			time.sleep(0.2)
		for f in range(2000, 100, -100):
			p.ChangeFrequency(f)
			time.sleep(0.2)
	
if __name__ == '__main__': #Program starts here
	print 'Press Ctrl+C to end program' 
	setup()
	p = GPIO.PWM(BZRPin, 50) #init frequency: 50Hz
	p.start(50)
	try:
		loop()
	except KeyboardInterrupt:
		p.stop()
		GPIO.cleanup()
