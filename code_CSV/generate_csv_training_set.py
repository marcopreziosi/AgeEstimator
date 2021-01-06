import shutil
import csv
import glob, os
import random


'''
Lette le annotazioni relative al nostro training set, lo script scrive un nuovo csv in 
cui tali annnotaioni sono riordinate in modo alernato dalla classe 0 alla classe 100
'''

dict_temp_directory={}

for i in range(101):
    dict_temp_directory[i] = []

with open('training_160.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        age = int(round(float(row[1]), 0))
        dict_temp_directory[age].append(row)


counter = 0
csv_file = open('csv_for_organization_training_2000_160.csv', 'w')

keys_list = list(dict_temp_directory.keys())
lenght = len(keys_list)
while len(dict_temp_directory.keys())!= 0:
    for i in range (101):
        if i in list(dict_temp_directory.keys()):
            if len(dict_temp_directory[i]) > 0:
                row = dict_temp_directory[i][len(dict_temp_directory[i])-1]
                csv_file.write(str(row[0]) + ','+str(row[1])+'\n') 
                dict_temp_directory[i].remove(row)
            else:
                counter += 1
                print(counter) 
                del(dict_temp_directory[i]) 

csv_file.close()