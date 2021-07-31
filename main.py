import socket
import select
import errno
import sys
import machine
led=machine.Pin(14,machine.Pin.OUT)
HEADER_LENGTH=10

IP="192.168.43.243"
PORT=5050
def f(a,b):
    a = str(a)
    return a + (b-len(a))*' '

my_username="LED1"
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username=my_username.encode("utf-8")
username_header = f(len(username),HEADER_LENGTH).encode('utf-8')
client_socket.send(username_header+username)

while True:
    try:
        while True:
            
            username_header=client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()
            username_length=int(username_header.decode("utf-8").strip())
            username=client_socket.recv(username_length).decode("utf-8")

            message_header=client_socket.recv(HEADER_LENGTH)
            message_length=int(message_header.decode("utf-8").strip())
            message=client_socket.recv(message_length).decode("utf-8")
            if message =="LED on":
                led.on()
            if message=="LED off":
                led.off()
                
    except:
        continue
    
