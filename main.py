import socket
import select
import errno
import sys
import machine
M1_T1=machine.Pin(14,machine.Pin.OUT)
M1_T2=machine.Pin(12,machine.Pin.OUT)
M2_T1=machine.Pin(16,machine.Pin.OUT)
M2_T2=machine.Pin(5,machine.Pin.OUT)
HEADER_LENGTH=10
M1_T1.off()
M1_T2.off()
M2_T1.off()
M2_T2.off()

IP="192.168.43.243"
PORT=5050
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
               
               M1_T1.off()
               M1_T2.on()
               M2_T1.off()
               M2_T2.on()
               
            
            
               
                
                
            if message=="R1 BACKWARD":
                
                M1_T1.on()
                M1_T2.off()
                M2_T1.on()
                M2_T2.off()
                
                
            if message=="R1 LEFT":
                
                M1_T1.off()
                M1_T2.off()
                M2_T1.off()
                M2_T2.on()
                
            if message=="R1 RIGHT":
                
                M1_T1.off()
                M1_T2.on()
                M2_T1.off()
                M2_T2.off()
            
            if message=="R1 STOP":
                M1_T1.off()
                M1_T2.off()
                M2_T1.off()
                M2_T2.off()
                
    except:
        continue
    


