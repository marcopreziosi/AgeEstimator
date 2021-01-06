import cv2 as cv2
import os, glob
from statistics import mean 


os.chdir("Dataset/complete_dataset_cropped/")


#Analisi dimensione media delle immagini
width=[]
height=[]
counter = 0
for img_name in glob.glob("*.jpg"):
    img=cv2.imread(img_name)
    width.append(img.shape[1])
    height.append(img.shape[0])
    counter+=1
    print(counter)

w_mean=int(round(mean(width), 0))
h_mean=int(round(mean(height), 0))
print(w_mean)
print(h_mean)

counter = 0
#resize delle immagini
for img_path in glob.glob("*.jpg"):
    counter += 1
    print(counter)
    img=cv2.imread(img_path)
    name=img_path.split('/')[-1].replace(".jpg.chip.jpg", ".jpg")
    img_new_path='Dataset/complete_dataset_resized_160/'+str(name)
    img=cv2.resize(img, (160, 160))
    cv2.imwrite(img_new_path, img)