# eroorrrrrrrrrr





import re
from time import time
import cv2, pandas
import requests
from datetime import datetime
import blob_images

first_frame = None
status_list = [None,None]
times = []
df=pandas.DataFrame(columns=["date_time", "captured" ,])

video = cv2.VideoCapture(0)
print('PROGRAM IS RUNNING!!!')

class send_payload:
    def __init__(self):
        self.payload_insert = {"id":'',"date_time":''}

obj_send_payload = send_payload()
# def convertToBinaryData(filename):
    
#     with open(filename, 'rb') as file:
#         binaryData = file.read()
#     return binaryData
    
while True:

    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5, 5),0)

    if first_frame is None:
        first_frame=gray
        continue
    
    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame, 100, 255, cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    cnts,_=cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1
        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,255), 4)
        
    status_list.append(status)
    status_list=status_list[-2:]
    current_dateTime = datetime.now()
    #12 hour format of date time
    dt = datetime.strptime(str(current_dateTime.hour)+":"+str(current_dateTime.minute), "%H:%M")
    formatted_time = dt.strftime("%I:%M %p")
    formatted_date = datetime.now().strftime("%B %d, %Y")
    date_time = formatted_date + formatted_time
    
    # WAITKEY
    key=cv2.waitKey(1)
    if key == ord('q'):
        break
    
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
        # print("motion detected")
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
        print("Object 2 detected" +str(times))
        imgs = cv2.imwrite("filename.jpg", frame)
  
      
        url = 'http://localhost:3000/data'
        check =  {"date_time": str(datetime.now().strftime("%B %d, %Y - ")+ str(datetime.now().strftime("%H:%M %S sec"))), "captured": imgs}
        # empPicture = convertToBinaryData(imgs)
        x = requests.post(url, json=check)
        # print(times)
        # print(status_list)
        # print(times)
        # for i in times:
        #     print(i)
        #     obj_send_payload.payload_insert['date_time'] = str(i)
        #     check = requests.post('http://localhost:8000/data',json=obj_send_payload.payload_insert)
        #     print(check.text)
            
    cv2.imshow("Color Frame",frame)

video.release() #shts cam
cv2.destroyAllWindows














    # if status_list[-1] == 1 and status_list[-2] == 0:
    #     times.append(date_time)
     
    # if status_list[-1] == 0 and status_list[-2] == 1:
    #     times.append(date_time)


    # for insert_date_time in times:
    #     print(insert_date_time)
    #     obj_send_payload.payload_insert['date_time'] = str(insert_date_time)
    #     check = requests.post('http://localhost:3000/upload',json=obj_send_payload.payload_insert)
    #     print(check.text)