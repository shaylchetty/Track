#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
# Initialize the EV3 brick.
ev3 = EV3Brick()
# Initialize a motor at port B.
test_motor = Motor(Port.B)
# Play a sound.
ev3.speaker.beep()
# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
test_motor.run_target(500, 90)
# Play another beep sound.
ev3.speaker.beep(1000, 500)

from pybricks.tools import wait

# ... (previous code)

# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
test_motor.run_target(500, 90)

# Wait for a moment to allow the motor movement to complete.
wait(1000)  # This will wait for 1 second.

# Play another beep sound.
ev3.speaker.beep(1000, 500)

# ... (rest of the code)
