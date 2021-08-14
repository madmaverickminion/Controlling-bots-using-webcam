import socket
import select
import errno
import sys
import machine
import time
M1_T1=machine.Pin(14,machine.Pin.OUT)
M1_T2=machine.Pin(12,machine.Pin.OUT)
M2_T1=machine.Pin(16,machine.Pin.OUT)
M2_T2=machine.Pin(5,machine.Pin.OUT)

en1 =machine.Pin(4,machine.Pin.OUT)
en2=machine.Pin(13,machine.Pin.OUT)

pwm1=machine.PWM(en1)
pwm2=machine.PWM(en2)

pwm1.init()
pwm2.init()
pwm1.duty(300)
pwm2.duty(300)

HEADER_LENGTH=10
M1_T1.off()
M1_T2.off()
M2_T1.off()
M2_T2.off()

IP="192.168.43.243"
PORT=5050
def forward():

    M1_T1.off()
    M1_T2.on()
    M2_T1.off()
    M2_T2.on()

def backward():
    M1_T1.on()
    M1_T2.off()
    M2_T1.on()
    M2_T2.off()
def stop():
    M1_T1.off()
    M1_T2.off()
    M2_T1.off()
    M2_T2.off()

stop()

def f(a,b):
    a = str(a)
    return a + (b-len(a))*' '

my_username="TOTO_1"
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
            
           
           
            if message =="R1 FORWARD":
                forward()

            if message=="R1 BACKWARD":
                backward()
                
            if message=="R1 LEFT":
                stop()
                time.sleep(1)

                M1_T1.off()
                M1_T2.off()
                M2_T1.off()
                M2_T2.on()
                time.sleep(0.70)
                forward()

            if message=="R1 RIGHT":
                stop()
                time.sleep(1)

                M1_T1.off()
                M1_T2.on()
                M2_T1.off()
                M2_T2.off()
                time.sleep(0.70)
                forward()

            
            if message=="R1 STOP":
                stop()
            if message=="R1 UNLOAD":
                stop()
                time.sleep(2)
                backward()
            if message=="R1 LEFTb":
                stop()
                time.sleep(2)
                
                M1_T1.off()
                M1_T2.off()
                M2_T1.on()
                M2_T2.off()
                time.sleep(0.70)
                backward()

            if message=="R1 STOP":
                stop()



                
    except:
        continue
    


