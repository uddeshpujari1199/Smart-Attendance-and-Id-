#C:\Users\uddes\AppData\Local\Programs\Python\Python36\Scripts

import cv2
import sys
import pyttsx3
import pymysql
from datetime import datetime
import MySQLdb
import base64
from PIL import Image
import io


connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='test',
)


engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[-1].id)

Time=datetime.now()
date=Time.strftime("%d/%m/%Y")
time=Time.strftime("%H:%M:%S")

employee=[]
if datetime.now().hour==20:
    employee.clear()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    global hour
    hour=int(datetime.now().hour)
    if hour>=0 and hour<12:
        speak("good morning")
    elif hour>=12 and hour<18:
        speak("good afternoon")
    else:
        speak("good evening")

def video_reader():
    cam = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cam.read()
        ID, bbox, _ = detector.detectAndDecode(img)
        if ID:
            print("QR Code detected-->", ID)
            speak("ID detected")
            U_ID=ID
            if datetime.now().hour<11:
                employee.append(U_ID)
            with connection.cursor() as cursor:
                sql="SELECT name FROM pydata WHERE ID = %s"
                cursor.execute(sql,(ID,))
                result=cursor.fetchall()
                for row in result:
                    name=row[0]


                wish()
                print(name)
                speak(name)    
                if datetime.now().hour>11:
                    if U_ID not in employee:
                        print(employee)
                        speak(" sorry you are late")

                else:
                    entry=time
                    out_time=" "
                    sql2="INSERT INTO attendance (ID, name, date, entry, out_time) VALUES (%s, %s, %s, %s, %s)"
                    result2=cursor.execute(sql2,(ID,name,date,entry,out_time))
                    print(result2)

                if U_ID in employee:
                    
            
                    out_time=time
                    sql3="UPDATE attendance SET out_time=%s WHERE ID=%s"
                    result3=cursor.execute(sql3,(out_time, ID))
                    print(result3)
                    
                
                connection.commit()
                connection.close()
                sys.exit()

if __name__=="__main__":
    video_reader()
