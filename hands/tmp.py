#speak
import speech_recognition as sr
from gtts import gTTS
import os
import apa102
import RPi.GPIO as GPIO
import time
import readchar
#import pwm_motor as motor

Motor_R1_Pin = 16
Motor_R2_Pin = 18
Motor_L1_Pin = 11
Motor_L2_Pin = 13
t = 0.5

dc=70 #

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Motor_R1_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Motor_R2_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Motor_L1_Pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Motor_L2_Pin, GPIO.OUT, initial=GPIO.LOW)

def acc():
   global dc
   dc += 10
   if dc >100:
      dc = 100
      print("current speed" + str(dc))
   forward()

def dec():
   global dc
   dc -= 10
   if dc < 30:
      dc = 30
      print ("car has stopped")
   else:
      print("current speed" + str(dc))
   forward()

def stop():
   GPIO.output(Motor_R1_Pin, False)
   GPIO.output(Motor_R2_Pin, False)
   GPIO.output(Motor_L1_Pin, False)
   GPIO.output(Motor_L2_Pin, False)

def forward():
   global dc
   GPIO.output(Motor_R1_Pin, dc)
   GPIO.output(Motor_R2_Pin, False)
   GPIO.output(Motor_L1_Pin, True)
   GPIO.output(Motor_L2_Pin, False)
   time.sleep(t)
   stop()

def backward():
   GPIO.output(Motor_R1_Pin, False)
   GPIO.output(Motor_R2_Pin, True)
   GPIO.output(Motor_L1_Pin, False)
   GPIO.output(Motor_L2_Pin, True)
   time.sleep(t)
   stop()

def turnRight():
   GPIO.output(Motor_R1_Pin, False)
   GPIO.output(Motor_R2_Pin, False)
   GPIO.output(Motor_L1_Pin, True)
   GPIO.output(Motor_L2_Pin, False)
   time.sleep(t)
   stop()

def turnLeft():
   GPIO.output(Motor_R1_Pin, True)
   GPIO.output(Motor_R2_Pin, False)
   GPIO.output(Motor_L1_Pin, False)
   GPIO.output(Motor_L2_Pin, False)
   time.sleep(t)
   stop()


#

LED_NUM = 3
leds = apa102.APA102(num_led=3)
colors = [[255,0,0],[0,255,0],[0,0,255]] # LED0: R, LED1: G, LED2: B

###
import cv2
from collections import Counter
from module import findnameoflandmark,findpostion,speak
import math

import os
import keyboard
import subprocess

cap = cv2.VideoCapture(0)
tip=[4,8,12,16,20]
tipname=[4,8,12,16,20]
fingers=[]

def gesture():
   while(True):
      global fingers
      ret, frame = cap.read()
      #flipped = cv2.flip(frame, flipCode = -1)
      frame1 = cv2.resize(frame, (640, 480))
      a=findpostion(frame1)
      b=findnameoflandmark(frame1)

      if len(b and a)!=0:  
         fingers=[]
         for id in range(0,5):#0~4
            if a[tip[id]][2:] < a[tip[id]-2][2:]:
               print(b[tipname[id]])
               fingers.append(1) #fingers+=1
            elif a[0][1:] < a[4][1:]: #thumb
               print(b[tipname[id]])
               fingers.append(1) #fingers+=1       
            else:
               fingers.append(0) #finger+=0 

      print(fingers) #[thumb,index,middle,ring,pinky]
      x=fingers# + finger
      c=Counter(x)
      up=c[1]
      down=c[0]
      print(up)
      print(down)
   
      cv2.imshow("Frame", frame1);
      key = cv2.waitKey(1) & 0xFF

      if up == 5:
         print("??????") 
         stop()
      if up == 4:
         print("??????")
         turnRight()    
      if up == 3:  
         print("??????") 
         turnLeft()    
      if up == 2:
         print("??????")
         forward()
      if up == 1:
         print("??????")
         backward()
      if up == 0:
         print("doesnothing")
      #if key == ord("w"):
         #acc()
      #if key == ord("s"):
         #dec()
      if key == ord("q"):
         speak("sir you have"+str(up)+"fingers up  and"+str(down)+"fingers down") 
         print("\nQuit")
         GPIO.cleanup()
         quit()
      if key == ord("s"):
         break 

while True:
   action = ""
   r=sr.Recognizer()
   with sr.Microphone(device_index = 2, sample_rate = 48000) as source:
      print("Please wait. Calibrating microphone...")
      #listen for 1 seconds and create the ambient noise energy level
      r.adjust_for_ambient_noise(source, duration=1)
      r.energy_threshold = 4000
      print("Say something!")
      audio=r.listen(source)
      print("Stop talking.")
    
   try:
      # recognize speech using Google Speech Recognition
      action= r.recognize_google(audio,language='zh-TW')
      print("I thinks you said '" + action + "'")

      if "??????" in action:
         print("????????????")
         #time.sleep(0.5)
         tts = gTTS(text='????????????', lang='zh-TW')
         tts.save('handcontrol.mp3')
         os.system('omxplayer -o local -p handcontrol.mp3 > /dev/null 2>&1')
         gesture()
     
     #5 stop
     #4 turnRight
     #3 turnLeft
     #2 backward
     #1 forward / speed up
     #0 does nothing
   
      elif "??????" in action: 
         acc()
         print("??????")
         #time.sleep(0.5)
         tts = gTTS(text='??????', lang='zh-TW')
         tts.save('speedup.mp3')
         os.system('omxplayer -o local -p speedup.mp3 > /dev/null 2>&1')

      elif "??????" in action: 
         dec()
         print("??????")
         #time.sleep(0.5)
         tts = gTTS(text='??????', lang='zh-TW')
         tts.save('speeddown.mp3')
         os.system('omxplayer -o local -p speeddown.mp3 > /dev/null 2>&1')

      elif "??????" in action: 
         stop()
         print("??????")
         #time.sleep(0.5)
         tts = gTTS(text='??????', lang='zh-TW')
         tts.save('carstop.mp3')
         os.system('omxplayer -o local -p carstop.mp3 > /dev/null 2>&1')

      elif "??????" in action:
         turnRight()    
         print("??????")
         #time.sleep(0.5)
         tts = gTTS(text='????????????', lang='zh-TW')
         tts.save('carturnright.mp3')
         os.system('omxplayer -o local -p carturnright.mp3 > /dev/null 2>&1')	
            
      elif "??????" in action:   
         turnLeft()    
         print("??????")
         #time.sleep(0.5)
         tts = gTTS(text='????????????', lang='zh-TW')
         tts.save('carturnleft.mp3')
         os.system('omxplayer -o local -p carturnleft.mp3 > /dev/null 2>&1')
        
      elif "??????" in action:
         forward()
         print("??????")
         #time.sleep(0.5)
         tts = gTTS(text='????????????', lang='zh-TW')
         tts.save('carforward.mp3')
         os.system('omxplayer -o local -p carforward.mp3 > /dev/null 2>&1')
     
      elif "??????" in action:
         for i in range(LED_NUM):
            leds.set_pixel(i, colors[i][0], colors[i][1], colors[i][2], 10)
            leds.show()
         backward()
         print("??????") 
         #time.sleep(0.5)
         tts = gTTS(text='????????????', lang='zh-TW')
         tts.save('carbackward.mp3')
         os.system('omxplayer -o local -p carbackward.mp3 > /dev/null 2>&1')

      elif "??????" in action:
         for i in range(LED_NUM):
            leds.set_pixel(i, colors[i][0], colors[i][1], colors[i][2], 10)
            leds.clear_strip()
            time.sleep(0.5)
         tts = gTTS(text='????????????', lang='zh-TW')
         tts.save('lightoff.mp3')
         os.system('omxplayer -o local -p lightoff.mp3 > /dev/null 2>&1')

      else:
         print(action)
   except sr.UnknownValueError:  
      print("I could not understand audio")
      action = "(??????????????????)"