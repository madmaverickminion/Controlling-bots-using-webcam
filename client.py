import socket
import select
import errno
import sys
import cv2 as cv
import numpy as np
import requests
# global message
HEADER_LENGTH=10

IP="192.168.43.243"
PORT=5050

my_username="head"

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username=my_username.encode("utf-8")
username_header=f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)
#################################################################################################################
#ip webcam live streaming link
url='http://192.168.43.1:8080/shot.jpg'
image_browser=requests.get(url)
img_arr=np.array(bytearray(image_browser.content), dtype=np.uint8)
img1=cv.imdecode(img_arr,-1)
frame1=cv.resize(img1,(int(img1.shape[1]*0.55),int(img1.shape[0]*0.55)),interpolation=cv.INTER_AREA)
image_browser=requests.get(url)
img_arr=np.array(bytearray(image_browser.content), dtype=np.uint8)
img2=cv.imdecode(img_arr,-1)
frame2=cv.resize(img2,(int(img2.shape[1]*0.55),int(img2.shape[0]*0.55)),interpolation=cv.INTER_AREA)



while True:
    # message=input(f"{my_username} > ")
    diff=cv.absdiff(frame1,frame2)
    gray=cv.cvtColor(diff,cv.COLOR_BGR2GRAY)
    blur=cv.GaussianBlur(gray,(7,7),1)
    _,thres=cv.threshold(blur,20,255,cv.THRESH_BINARY)
    dilated=cv.dilate(thres,None,iterations=3)
    

    contours,_=cv.findContours(dilated,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x,y,w,h)=cv.boundingRect(contour)
        if cv.contourArea(contour)<1300:
            continue
        cv.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
#############################################################################################        
        #Main Algorithm for robot control(TO BE CONTINUED.......)
        if((x,y)==(450,405)):

            #check count of each and return accordingly
            message = "MOVE LEFT"
            message_header=f"{len(message) :< {HEADER_LENGTH}}"
            # message_header.encode("utf-8")
            final_message=(message_header+message).encode("utf-8")

            client_socket.send(final_message)
#############################################################################################
    cv.imshow('Live Stream',frame1)
    frame1=frame2
    
    image_browser=requests.get(url)
    img_arr=np.array(bytearray(image_browser.content), dtype=np.uint8)
    img=cv.imdecode(img_arr,-1)
    frame2=cv.resize(img,(int(img.shape[1]*0.55),int(img.shape[0]*0.55)),interpolation=cv.INTER_AREA)


    if cv.waitKey(40) & 0xFF==ord('d'):
        break


    