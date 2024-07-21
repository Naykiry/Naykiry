import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import requests
from PIL import Image


prom =""

url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Api-Key AQVNxldCl8ZRc1QAWq6k8CPfx2U_1MJWV0Y1y-1G"
}


cap = cv2.VideoCapture(0)
cap.set(propId = 3, value = 1280)
cap.set(propId=4, value = 720)

    # Initialize the HandDetector class with the given parameters
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)

def getHandInfo(img):
    hands, img = detector.findHands(img, draw=True, flipType=True)

        # Check if any hands are detected
    if hands:
            # Information for the first hand detected
        hand1 = hands[0]  # Get the first hand detected
        lmList1 = hand1["lmList"]  # List of 21 landmarks for the first h
        if len(hands) == 2:
                # Information for the second hand
                hand2 = hands[1]
                lmList2 = hand2["lmList"]
                hh=1

                # Count the number of fingers up for the second hand
                fingers2 = detector.fingersUp(hand2)
                #print(fingers2)
                return fingers2,lmList2, hh
                
                
            # Count the number of fingers up for the first hand
        fingers1 = detector.fingersUp(hand1)
        hh=0
        #print(fingers1)
        return fingers1, lmList1,hh
        
    else:
        return None
    

#def draw(info, prev_pos, canvas):
    fingers1, lmList1 = info
    current_pos = None

    if fingers1 == [0, 1, 0, 0, 0]:
        current_pos = lmList1[8][0:2]
        if prev_pos is None: prev_pos = current_pos
        cv2.line(canvas, current_pos, prev_pos, color = (255,0,255), thickness = 10)
    elif fingers1 == [1, 1, 1, 1, 1]:    
        canvas = np.zeros_like(img)


    return current_pos, canvas

def SendToAI(prom, fingers1):
    if fingers1 == [1, 1, 1, 0, 0]:
        prompt = {
            "modelUri": "gpt://b1gvmhcp2qkhho7aiflg/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "2000"
            },
            "messages": [
            {
            "role": "system",
            "text": "Ты — умный математик"
            },
            {
            "role": "user",
            "text": "реши эту задачу" + prom
            }
        ]
        }
        response = requests.post(url, headers=headers, json = prompt)
        result = response.text
        print(result)
        print(prom)
        

flag = True
def Plus(fingers1, prom, flag):
    if fingers1 == [0,0,0,0,0]:
        flag = True 
    if fingers1 == [0,0,0,0,1] and flag == True:
        prom = prom + '+'
        flag = False
        print(prom)
    elif fingers1 == [1, 1, 1, 1, 1]:    
        prom=""
        print(prom)
    return prom, flag

def Minus(fingers1,prom,flag):
    if fingers1 == [0,0,0,0,0]:
        flag = True 
    if fingers1 == [0,0,0,1,1] and flag == True:
        prom = prom +'-'
        flag = False
        print(prom)
    return prom, flag

def Nums(fingers2,prom, flag):
    
    if fingers2 == [0,0,0,0,0]:
        flag = True     
    if fingers2==[1,0,0,0,0] and flag == True:
        prom = prom +'1'
        flag = False  
        print(prom) 
    elif fingers2==[1,1,0,0,0] and flag == True:
        prom = prom +'2'
        flag = False
        print(prom)
    elif fingers2==[1,1,1,0,0] and flag == True:
        prom = prom +'3'
        flag = False
        print(prom)
    elif fingers2==[1,1,1,1,0] and flag == True:
        prom = prom +'4'
        flag = False
        print(prom)
    elif fingers2==[1,1,1,1,1] and flag == True:
        prom = prom +'5'
        flag = False
        print(prom)
    elif fingers2==[0,0,0,0,1] and flag == True:
        prom = prom +'6'
        flag = False
        print(prom)
    elif fingers2==[0,0,0,1,1] and flag == True:
        prom = prom +'7'
        flag = False
        print(prom)
    elif fingers2==[0,0,1,1,1] and flag == True:
        prom = prom +'8'
        flag = False
        print(prom)
    elif fingers2==[0,1,1,1,1] and flag == True:
        prom = prom +'9'
        flag = False
        print(prom)
    elif fingers2==[1,0,0,0,1] and flag == True:
        prom = prom +'0'
        flag = False
        print(prom)
    
    return prom, flag
        

prev_pos = None 
canvas = None
image_combined = None



while True:
        # Capture each frame from the webcam
        # 'success' will be True if the frame is successfully captured, 'img' will contain the frame
    success, img = cap.read()
    img = cv2.flip(img, flipCode=1)

    if canvas is None:
        canvas = np.zeros_like(img)
        
    
    info = getHandInfo(img)
    
    if info:
        fingers1, lmList1, hh = info
        #print(fingers1)
        #prev_pos, canvas = draw(info, prev_pos, canvas)
        if hh ==0:
            SendToAI(prom,fingers1)
            prom, flag = Plus(fingers1,prom, flag)
            prom, flag = Minus(fingers1,prom, flag)
        if hh==1 :
            prom, flag = Nums(fingers1,prom,flag)
    
    
    alpha = 0.7
    image_combined = cv2.addWeighted(img, alpha,canvas,beta=0.3,gamma=0)


    # Display the image in a window
    #cv2.imshow("Image", img)
    #cv2.imshow("Canvas", canvas)
    cv2.imshow("image_combined", image_combined)

    # Keep the window open and update it for each frame; wait for 1 millisecond between frames
    cv2.waitKey(1)