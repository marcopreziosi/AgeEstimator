############
# Import #
############
import  csv, glob, os
import random
from datetime import datetime
import shutil

IMG_MAX = 2000
'''
Il seguente script viene utilizzato per la generazione della porzione di 
dataset che sarà successivamente divisa in training set e validation set.
In particolare, per ogni classe di età (0-100) verrà preso un numero 
prefissato di immagini, adottando il seguente criterio:
- si prendono k campioni per ogni identità (per evitare di prendere un numero 
  di campionitroppo elevato per una stessa persona)
- se questo numero non raggiunge il limite minimo di immagini prefissate per ogni
  classe, i rimanenti campioni sono scelti casualmente tra quelli ancora disponibili 
  per ciascuna classe.
'''


#dict_volte_personaggio viene utilizzato per contare quate volte viene presa una identità
dict_volte_personaggio ={}
with open('train.age_detected_vgg.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    first_prec = ''
    for row in csv_reader:
        first_curr = row[0].split("/")[0]
        if first_curr not in dict_volte_personaggio.keys():    
            dict_volte_personaggio[first_curr] = []
        
#inizializzazione dizionari

#dict_tot_vgg racchiude le immagini di train disponibili nel dataset VGG
dict_tot_vgg= {}
for i in range(101):
    dict_tot_vgg[i] = []

#dict_tot_vgg racchiude le immagini selezionate per il nostro dataset
dict_img_scelte = {}
for i in range(101):
    dict_img_scelte[i] = []

#dict_tot_vgg racchiude le immagini selezionate dal dataser UTK
utk_dict ={}
for i in range(101):
    utk_dict[i] = []

############
# UTK_dict #
############
os.chdir("../dataset_UTK/")
for file in glob.glob("*.jpg.chip.jpg"):
    age = int(file.split("_")[0])
    utk_dict[age].append(file)

age_utk_length = []
for i in range(101):
    age_utk_length.append(len(utk_dict[i]))

#print (age_utk_length)

############
# VGG_dict #
############
with open('train.age_detected_vgg.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        age = int(round(float(row[1]), 0))
        dict_tot_vgg[age].append(row)

age_vgg_length = []
for i in range(101):
    age_vgg_length.append(len(dict_tot_vgg[i]))



#imm totali per ogni classe di età 
age_tot = []
for i in range(101):
    age_tot.append(age_vgg_length[i] + age_utk_length[i])


for i in range(101):
    temp_list = []
    #Per le classi di età per le quali ho meno del MAX_IMG prendi tutte le immagini disponibili di VGG
    if (age_tot[i]<=IMG_MAX):
            items_list = dict_tot_vgg[i]
            
            for item in items_list:
                dict_img_scelte[i].append(item)
                personaggio = str(item[0].split("/")[0])
                dict_volte_personaggio[personaggio].append("preso")
            #cancello la chiave relativa alla classe che ho finito di prendere
            del(dict_tot_vgg[i])

    #prendiamo solo una parte da vgg (IMG_MAX - img_UTK)
    elif (age_tot[i]>IMG_MAX):
        imm_prendere = 0
        if age_vgg_length[i]>IMG_MAX:
            imm_prendere = IMG_MAX - age_utk_length[i]
        else:
            imm_prendere = age_vgg_length[i] - age_utk_length[i]

        persone_prese = list(dict_volte_personaggio.keys())
        items_list = dict_tot_vgg[i]
        
        for item in items_list:
            #prendo solo le immagini che mi servono
            if len(dict_img_scelte[i]) < imm_prendere:
                personaggio = str(item[0].split("/")[0])
                #non prendo più di 20 imm per cartella
                if len(dict_volte_personaggio[personaggio])<20:
                    dict_img_scelte[i].append(item)
                    temp_list.append(item)
                    dict_volte_personaggio[personaggio].append("preso")
            else:
                break
        
        #rimuovo le immagini che ho preso dal dizionario dict_tot_vgg
        for item in temp_list:
            dict_tot_vgg[i].remove(item)
        

#Vengono presi i campioni rimanenti in modo casuale tra quelli ancora disponibili per ciascuna classe tra i personaggi disponibili 
print ("inizio la compensazione")
for i in range (101):
    if i in list(dict_tot_vgg.keys()):
        if len(dict_img_scelte[i]) < (IMG_MAX - age_utk_length[i]):
            imgs = IMG_MAX  - len(dict_img_scelte[i]) - age_utk_length[i]  
            random.seed(datetime.now())
            random.shuffle(dict_tot_vgg[i])
            for k in range (imgs):
                dict_img_scelte[i].append(dict_tot_vgg[i][k])
                


counter_imgs=0
print("copio le immagini")
#Creazione dataset completo
for i in range(101):
    print ("classe: " + str(i) + " completa")
    items_list = dict_img_scelte[i]
    for item in items_list:
        img_path_origin = item[0]
        img = item[0].replace("/", "_")
        counter_imgs+=1
        shutil.copy2("/Dataset/VGG/train/"+ str(img_path_origin) , "/Dataset/complete_dataset/"+ str(img))

print(counter_imgs)




#Scrittura file 
f = open("Analisi_dataset_scelto.txt", "w")

f.write("Classe \t\t imm prese \t\t vgg \t\t utk\n")
for i in range(101):
    f.write("classe: "+ str(i) + "\t\t" + str(len(dict_img_scelte[i]))+ "\t\t"+ str(age_vgg_length[i]) + "\t\t" + str(age_utk_length[i])+"\n")


f.close()  





