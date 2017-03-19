<h1> Step_Motor_Driver </h1>
<h3> Raspberry Driven Telescope Focuser (RDTF) </h3>

This code is meant to let you control a 28BYJ-48 step motor via ULN2003.<br> In my case i use the motor to smoothly focus my telescope.<br><br>

The code has 2 classes and a main flow.
* _GetchUnix is meant to resamble the getch() function in C. I need this to quickly control the motor.
* _StepDriver is meant to make a number of steps in a given direction with some time between each steps.

Both classes are adaptation from StackOverflow's solutions.<br>
The main flow just get the number of steps, multiplies it for a multiplier and makes the motor turn.<br>
An help command can be issued by typing "h" and it will return which key does what.<br>
* "q","w","e" and "a","s","d" keys are meant to determine the number of steps the motor will make 
( 1, 2, 5 and -1, -2, -5 where positive numbers rappresent clockwise rotation and negative numbers anti clockwise rotation )
* "r", "t", "y" keys are meant to set the multiplier to 1, 10 or 100. Once selected the multiplier remains the same until changed again
* "i", "o", "p" keys are meant to change the time between each step. "i" makes the rotation slow, "o" makes it normal, "p" fast.

Default values of multiplier and speed are respectively 10 and normal.<br>
Once you press one of the "steps" keys the motor will start turning.<br> 
The string "... Done" will actually appear when the motor ended its number of steps.<br>
During that period of time you can only end the program via ctrl+c.<br>
<h4> NOTE </h4>
This will leave a <b>GPIO session open</b>, which will cause the <b>use of current by the motor even if it stopped turning</b> causing heating over time.<br>
<u>You can prevent this in 2 simple ways:</u><br><br>
<ol>
<li> By opening once again the program and selecting fast speed and make 10 steps, this will issue a warning cause a GPIO session is already open (nothing to worry about) the motor will then make his 10 steps and end the GPIO session.</li> 
<li> By disconnecting the power supply to the motor. This has the advantage that no other steps will be made. </li>
</ol>
