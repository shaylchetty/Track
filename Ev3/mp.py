import socket

# Replace "your_ev3_brick_ip" and 12345 with the IP address and port number of your EV3 brick
EV3_ADDRESS = ("192.168.4.241", 12345)

def send_command(command):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(EV3_ADDRESS)
    client.send(command.encode())
    client.close()
    print("command sent")

# Send a motor control command to the EV3 brick (you can extend this to send different commands based on your requirements)
send_command("start_motors")
