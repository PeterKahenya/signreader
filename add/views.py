import os
import cv2
import base64
import time
from django.shortcuts import render,HttpResponse
from train.context import get_classes

WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"train")
VALIDATE_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"validate")
IMAGE_DIM=224

def index(request):
        T_CLASSES,T_NUMBER_OF_CLASSES=get_classes(TRAIN_DIR)
        t_total=0
        t_no_of_images_per_class=[]
        for word in T_CLASSES:
                word_dict={}
                word_path=os.path.join(TRAIN_DIR,word)
                count=len(os.listdir(word_path))
                t_total=t_total+count
                word_dict[word]=count
                t_no_of_images_per_class.append(word_dict)
    
        V_CLASSES,V_NUMBER_OF_CLASSES=get_classes(VALIDATE_DIR)
        v_total=0
        v_no_of_images_per_class=[]
        for word in V_CLASSES:
                word_dict={}
                word_path=os.path.join(VALIDATE_DIR,word)
                count=len(os.listdir(word_path))
                v_total=v_total+count
                word_dict[word]=count
                v_no_of_images_per_class.append(word_dict)
        if request.method=="GET":
                return render(request,"add.html",{"r_total":6000-t_total,'pct':round(100-(6000-t_total)/60,2)},None)
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
                        cv2.imwrite(uploaded_file_url,resized_image)
                        print(dataset+" gesture added for the letter :"+word)
                        return HttpResponse("ADDED")
                else:
                        return HttpResponse("Method Not allowed!!")
