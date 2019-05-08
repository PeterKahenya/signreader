#import statements
import os
import tensorflow.keras as keras
from tensorflow.keras.applications.mobilenet import MobileNet
from tensorflow.keras.optimizers import SGD,Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import Dense, Dropout,Conv2D,MaxPooling2D,Flatten,Activation

WORK_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR=os.path.join(os.path.join(WORK_DIR,"temp"),"models")
TRAIN_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"train")
VALIDATE_DIR=os.path.join(os.path.join(WORK_DIR,"images"),"validate")
IMAGE_DIM=224

image_gen=ImageDataGenerator(preprocessing_function=keras.applications.mobilenet.preprocess_input)

def get_classes(directory):
    words=[]
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("jpg") or file.endswith("jpeg") or file.endswith("png"):
                path=os.path.join(root,file)
                word=os.path.basename(os.path.dirname(path))
                if not word in words:
                    words.append(word)
    return words,len(words)
def create_train_model():
    CLASSES,CLASSES_COUNT=get_classes(TRAIN_DIR)
    train_batch=image_gen.flow_from_directory(TRAIN_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=1)
    validate_batch=image_gen.flow_from_directory(VALIDATE_DIR,target_size=(IMAGE_DIM,IMAGE_DIM),classes=CLASSES,batch_size=1)
    mobile=MobileNet()
    x=mobile.layers[-6].output
    predictions=Dense(2,activation='softmax')(x)
    model=Model(inputs=mobile.input,outputs=predictions)
    for layer in model.layers[:-23]:
        layer.trainable=False
    model.compile(Adam(lr=.0001),loss="categorical_crossentropy",metrics=['accuracy'])
    model.fit_generator(train_batch,steps_per_epoch=29,validation_data=validate_batch,validation_steps=2,epochs=50,verbose=2)
    model.save(os.path.join(MODEL_DIR,"model.hd5"))
create_train_model()

