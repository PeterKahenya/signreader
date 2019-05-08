import os
import cv2
import base64
import time
from django.shortcuts import render,HttpResponse

WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"train")
VALIDATE_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"validate")
IMAGE_DIM=224
def index(request):
    if request.method=="GET":
        return render(request,"add.html",None,None)
    else:
        if request.method=="POST":
                hand_roi=request.POST['hand_roi']
                hand_roi=hand_roi.replace("data:image/png;base64,","")

                img_data = base64.b64decode(hand_roi)
                word=request.POST['word'].lower()
                dataset=request.POST['dataset_choice']

                img_path=""
                if dataset=="train":
                        img_path=os.path.join(TRAIN_DIR,word)
                else:
                        img_path=os.path.join(VALIDATE_DIR,word)
                if not os.path.exists(img_path):
                        os.makedirs(img_path)

                uploaded_file_url = os.path.join(img_path,word+str(int(time.time()*1000))+".jpg")
                img_file = open(uploaded_file_url, "wb+")
                img_file.write(img_data)
                img_file.close()

                img=cv2.imread(uploaded_file_url)
                resized_image=cv2.resize(img,(IMAGE_DIM,IMAGE_DIM))
                resized_image_gray=cv2.cvtColor(resized_image,cv2.COLOR_BGR2GRAY)
                cv2.imwrite(uploaded_file_url,resized_image)
                print(dataset+" gesture added for the letter :"+word)
                return HttpResponse("ADDED")
        else:
            return HttpResponse("Method Not allowed!!")
