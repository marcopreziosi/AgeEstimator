from keras.models import load_model
import keras.backend as K
from keras.preprocessing import image
import numpy as np
import glob as glob
import argparse
import cv2 as cv2
import csv
from PIL import Image
from numpy import asarray
import os

def init_param():
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", type=int, default=0,  help="Show images")
    parser.add_argument("--dir", type=str,  help="Folder that contains directories of identities")
    parser.add_argument("--annotation", type=str,  help="Annotations for crop")
    parser.add_argument("--net", type=str,  help="Net path")
    parser.add_argument("--csv", type=str,  help="If it is not None, it writes on csv file")
    args = parser.parse_args()
    return args

#Accuracy che tiene conto del grado di confidenza della rete
def contrastive_accuracy(y_true, y_pred):
    return  1.0-K.mean(K.max(abs(y_pred-y_true),axis=1)) 

IMAGE_SIZE = (160, 160)

args = init_param()

if args.csv is not None:
    f = open(args.csv, 'w')



dict_annotation={}
with open(args.annotation) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    key = ''
    for row in csv_reader:
        key = row[2]
        x = int(row[4]) 
        y = int(row[5])
        w = int(row[6])
        h = int(row[7])
        dict_annotation[key] = (x,y,w,h)

#caricamento del modello
model = load_model(args.net, custom_objects= {'contrastive_accuracy': contrastive_accuracy})

counter = 0
os.chdir(args.dir)
key_not_found = []

for filename in glob.glob("*/*.jpg"):
    
    img = filename
    frame = cv2.imread (str(img))
    try:
        #crop dell'immagine con le coordinate lette dall'annotation.csv
        bbox = []
        
        (x,y,w,h) = dict_annotation[img]
        bbox.append(x)
        bbox.append(y)
        bbox.append(x + w) 
        bbox.append(y + h)
        padding_px = 0
        img = frame[max(0,bbox[1]-padding_px):min(bbox[3]+padding_px,frame.shape[0]-1),max(0,bbox[0]-padding_px):min(bbox[2]+padding_px, frame.shape[1]-1)]
        img = cv2.resize(img, (160, 160))
        
        #Predict del modello
        img_p = np.reshape(img,[1,160,160,3])
        result = model.predict(img_p)
        img_class = np.argmax(result)
        counter += 1
        print (counter)

        #Vuisualizzazione delle immagini
        if args.view:
            img=cv2.resize(img, (400, 400))
            cv2.putText(img, 'Age predicted: '+str(img_class), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            cv2.imshow('Age', img)
            if cv2.waitKey(0) == ord('q'):
                break

        if args.csv is not None:
            f.write(str(filename)+', '+str(img_class)+'\n')
    
    except KeyError:
        key_not_found.append(img)
    


if args.csv is not None:
    f.close()


print (key_not_found)


