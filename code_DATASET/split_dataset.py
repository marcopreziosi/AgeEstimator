import shutil
import csv
import glob, os
import random
from datetime import datetime

'''
Split del dataset in 90% train - 10% val
'''

dict_complete_data = {}
for i in range(101):
    dict_complete_data[i] = []

with open('/Dataset/dataset_complete_160.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        img_name = row[0]
        if os.path.exists("/Dataset/complete_dataset_resized_160/" + str(img_name)):
            age = int(round(float(row[1]), 0))
            dict_complete_data[age].append(row)


validation_temp = []


f = open("validation_160.csv", "w")
counter = 0
for i in range (101):
    temp = []
    random.seed(datetime.now())
    item_list = dict_complete_data[i]
    lenght = len(item_list)
    validation_temp = random.sample(item_list,int(round((len(item_list)/10),0)))
    for j in range (len(validation_temp)):
        img = validation_temp[j][0]
        age = validation_temp[j][1]
        f.write(str(img) + "," + str(age) + "\n")
        shutil.copy2("/Dataset/complete_dataset_resized_160/"+ str(img) , "/Dataset/validation_160/"+ str(img))
        temp.append(validation_temp[j])
    for item in temp:
        dict_complete_data[i].remove(item)
    counter += 1
    print (counter)
f.close()

f = open("training_160.csv", "w")
counter = 0
for i in range (101):
    for j in range (len(dict_complete_data[i])):
        img = dict_complete_data[i][j][0]
        age = dict_complete_data[i][j][1]
        f.write(str(img) + "," + str(age) + "\n")
        shutil.copy2("/Dataset/complete_dataset_resized_160/"+ str(img) , "/Dataset/training_160/"+ str(img))
        counter += 1
        print (counter)
f.close()
