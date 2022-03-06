'''
Created by Shubharthak Sangharasha
@github: shubharthaksangharsha
'''
#Import Libraries
import cv2
from cvzone.HandTrackingModule import HandDetector

#Button Class 
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos 
        self.width = width 
        self.height = height
        self.value = value 
        
    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)  
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)
        cv2.putText(img, self.value , (self.pos[0]  + 42, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 
                    2, (50, 50 , 50), 2)
    
    def checkClick(self, x, y):
        # x1 < x < x1 + width
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)
            cv2.putText(img, self.value , (self.pos[0]  + 32, self.pos[1] + 75), cv2.FONT_HERSHEY_PLAIN, 
                    5, (0, 0 , 0), 5)
            return True
        return False 
#webcam 
cap = cv2.VideoCapture(0)

#Detection of Hands
detector = HandDetector(maxHands=1, detectionCon=0.8)

#Creating button 
buttonListValues = [['7', '8', '9', '*'],
                    ['4', '5', '6', '-'],
                    ['1', '2', '3', '+'],
                    ['0', '/', '.', '=']]
buttonList = []

for x in range(4):
    for y in range(4):
        xpos = x * 100 + 120
        ypos = y * 100 
        buttonList.append(Button((xpos, ypos), 100, 100, buttonListValues[y][x]))

#Clear button 
clear_button = Button((520,0), 100, 100, 'C')
#Back Button 
back_button = Button((520,100), 100, 100, '<-')
#Left Paranthesis
leftParanthesis = Button((520, 200), 100, 100 , '(')
#Right Paranthesis
rightParanthesis = Button((520, 300), 100, 100 , ')')
#Variables 
myEquation = ''
delayCounter = 0
while True:
    #Get image from webcam 
    success, img = cap.read()
    img = cv2.flip(img, 1)
    
    #Detection of hand
    hands, img  = detector.findHands(img, flipType=False)

    #Draw all buttons
    cv2.rectangle(img, (120, 400), (400 + 120, 490 + 490 ),
                      (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (120, 400), (400+ 120, 490 ),
                      (50, 50, 50), 3)
    for button in buttonList:
        button.draw(img)
    clear_button.draw(img)
    back_button.draw(img)
    leftParanthesis.draw(img)
    rightParanthesis.draw(img)
    #Check for Hand
    if hands:
        lmList = hands[0]['lmList']
        length, _, img  = detector.findDistance(lmList[8][:2], lmList[12][:2], img)  
        x, y = lmList[8][:2]
        if length < 50:
            try:
                for i, button in enumerate(buttonList):
                    if button.checkClick(x, y) and not delayCounter:
                        myValue = buttonListValues[int(i % 4)][int(i / 4)]
                        print(myValue) 
                        if myValue == '=':
                            myEquation = str(eval(myEquation))
                        else:
                            myEquation += myValue                    
                        delayCounter = 1
                if clear_button.checkClick(x,y) and not delayCounter:
                    print(clear_button.value)
                    myEquation = ''
                    delayCounter = 1
                if back_button.checkClick(x,y) and not delayCounter:
                    print(back_button.value)
                    myEquation = myEquation[:len(myEquation) - 1]
                    delayCounter = 1
                if leftParanthesis.checkClick(x,y) and not delayCounter:
                    print(leftParanthesis.value)
                    myEquation += '('
                    delayCounter = 1
                if rightParanthesis.checkClick(x,y) and not delayCounter:
                    print(rightParanthesis.value)
                    myEquation += ')'
                    delayCounter = 1
            except Exception as e:
                myEquation = 'Error'
                print(e)
                    
    #Avoid Duplicates 
    if delayCounter:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0
            
    #Display the equation/result 
    cv2.putText(img, myEquation , (125, 450), cv2.FONT_HERSHEY_PLAIN, 
                    3, (50, 50 , 50), 3)
    
    #Display Image 
    cv2.imshow('Virtual Calculator by Shubharthak', img)
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()