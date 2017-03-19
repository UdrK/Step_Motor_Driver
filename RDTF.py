# -*- coding: UTF-8 -*-
class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _StepDriver:
		
	def __call__(self, direction, steps, wait_time=10/float(1000)):
		import sys, time, RPi.GPIO as GPIO
		
		GPIO.setmode(GPIO.BCM) # Use BCM GPIO references instead of physical pin numbers
		
		# Define GPIO signals to use
		# Physical pins 11,15,16,18
		# GPIO17,GPIO22,GPIO23,GPIO24
		StepPins = [17,22,23,24]
		
		# Set all pins as output
		for pin in StepPins:
			GPIO.setup(pin,GPIO.OUT)
			GPIO.output(pin, False)
			
		# Define advanced sequence
		# as shown in manufacturers datasheet
		Seq = [[1,0,0,1],
			   [1,0,0,0],
			   [1,1,0,0],
			   [0,1,0,0],
			   [0,1,1,0],
			   [0,0,1,0],
			   [0,0,1,1],
			   [0,0,0,1]]		
		
		StepCount = len(Seq)
		StepDir = direction # Set to 1 or 2 for clockwise Set to -1 or -2 for anti-clockwise
		WaitTime = wait_time #10/float(1000) # Read wait time from command line
		stopit = steps
		StepCounter = 0
		index = 0

		while index<stopit:
		 
			index = index+1
			for pin in range(0,4):
				xpin=StepPins[pin] # Get GPIO
				if Seq[StepCounter][pin]!=0:
					GPIO.output(xpin, True)
				else:
					GPIO.output(xpin, False)

			StepCounter += StepDir

			# If we reach the end of the sequence start again	
			if (StepCounter>=StepCount):
				StepCounter = 0
			if (StepCounter<0):
				StepCounter = StepCount+StepDir
			
			time.sleep(WaitTime) # Wait before moving on

		GPIO.cleanup()
print ""
print " ┌──────────────────────────────┐"
print " │   Step driver v .1           │"  
print " └──────────────────────────────┘"
print " Press 'h' to get an help message"
print " Press 'u' to exit"
print " ────────────────────────────────"

c = ''    
sp = 0
mp = 10
while c != 'u':
	g = _GetchUnix()
	c = g()
	cw = ['q','w','e']
	acw = ['a', 's', 'd']
	spv = ['i', 'o', 'p']
	mpv = ['r', 't', 'y']
	
	if(c=='h'):
		print " Keys 'q', 'w', 'e' are meant to set number of steps to 1, 2 or 5"
		print " Keys 'a', 's', 'd' are meant to set number of steps to -1, -2 or -5"
		print " Keys 'r', 't', 'y' are meant to set multiplier for number of steps to 1, 10 or 100"
		print " Keys 'i', 'o', 'p' are meant to set speed of rotation to slow, normal or fast"
		
	if(c in mpv):
		if(c=='r'):
			mp = 1
			print " Setting multiplier to 1"
		elif(c=='t'):
			mp = 10
			print " Setting multiplier to 10"
		elif(c=='y'):
			mp = 100
			print " Setting multiplier to 100"
			
	if(c in spv):
		if(c=='i'):
			sp = 100/float(1000)
			print " Setting speed to slow"
		elif(c=='o'):
			sp = 10/float(1000)
			print " Setting speed to normal"
		elif(c=='p'):
			sp = 1/float(1000)
			print " Setting speed to fast"
		
	if (c in cw or c in acw):
		
		if (c in cw):
			direction = 1
		else:
			direction = -1
		
		if(c=='q' or c=='a'):
			steps = 1
		elif(c=='w' or c=='s'):
			steps = 2
		elif(c=='e' or c=='d'):
			steps = 5
			
		print " Making "+str(direction*mp*steps)+" steps ..."
			
		sd = _StepDriver()
		if sp != 0:
			sd(direction, mp*steps, sp)
		else:
			sd(direction, mp*steps)
		
		print " ... Done"
