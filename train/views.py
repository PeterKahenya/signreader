#import statements
import os
import cv2
from .context import get_classes
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Model
from django.shortcuts import render,HttpResponse
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet import MobileNet,preprocess_input
from tensorflow.keras.layers import Dense, Dropout,Conv2D,MaxPooling2D,Flatten


#commonly used variables and paths
WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR=os.path.join(WORK_DIR,"models")
TRAIN_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"train")
VALIDATE_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"validate")
image_gen=ImageDataGenerator(preprocessing_function=preprocess_input)
IMAGE_DIM=224


def create_and_train_model(classes,classes_count,t_images_count,v_images_count,train_batches=10,validate_batches=10):
    #one-time setups for each training session
    t_batches_per_epoch=int(t_images_count/train_batches)
    v_batches_per_epoch=int(v_images_count/validate_batches)    
    train_batch=image_gen.flow_from_directory(TRAIN_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=classes,batch_size=train_batches)
    validate_batch=image_gen.flow_from_directory(VALIDATE_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=classes,batch_size=validate_batches)
    

    mobile=MobileNet()
    x=mobile.layers[-6].output
    predictions=Dense(classes_count,activation='softmax')(x)
    model=Model(inputs=mobile.input,outputs=predictions)
    for layer in model.layers[:-23]:
        layer.trainable=False

    #compile model using accuracy to measure model performance
    model.compile(optimizer=Adam(),loss='categorical_crossentropy',metrics=['accuracy'])
    model.fit_generator(train_batch,steps_per_epoch=t_batches_per_epoch,validation_data=validate_batch,validation_steps=v_images_count,epochs=10,verbose=1)


    #save trained model
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    model.save(os.path.join(MODEL_DIR,"model.hd5"))


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

        return render(request,"train.html",{"t_no_of_classes":T_NUMBER_OF_CLASSES,
                                            "t_no_of_images_per_class":t_no_of_images_per_class,
                                            "t_total":t_total,
                                            "v_no_of_classes":V_NUMBER_OF_CLASSES,
                                            "v_no_of_images_per_class":v_no_of_images_per_class,
                                            "v_total":v_total
                                            },
                                            None)
    else:
        if request.method=="POST":

            create_and_train_model(classes=T_CLASSES,classes_count=T_NUMBER_OF_CLASSES,t_images_count=t_total,v_images_count=v_total,train_batches=1,validate_batches=1)

            return HttpResponse("model is trained")
        else:
            return HttpResponse("method not allowed")
