
#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
import socket
import time

def rotate():
    # Initialize the EV3 Brick
    ev3 = EV3Brick()

    # Create a motor object
    motor = Motor(Port.A)

    # Set the motor to spin at a certain speed
    motor.run(500)
    
    # Stop the motor
    motor.stop()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 12345))  # Replace 12345 with the same port number used in the server code
server.listen(1)

print("Waiting for a connection...")

client_socket, addr = server.accept()
print(f"Accepted connection from {addr}")

# Initialize the motors

# Set the motor speed (values between -100 and 100)
motor_speed = 50

while True:
    data = client_socket.recv(1024).decode()
    if not data:
        break
    if data == "start_motors":
        print("started motors")
        # Rotate motors A and B for 2 seconds
        rotate()


motor.stop()
# Close the client socket and the server
client_socket.close()
server.close()
