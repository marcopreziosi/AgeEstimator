## Overview
Lo scopo del progetto è quello di realizzare una rete neurale per la stima dell’età di una persona. Per questo scopo, è stato addestrato un classificatore.

## Descrizione della soluzione
L’architettura della rete si basa su Fine Tuning della rete MobilenetV2 con input size pari a 160x160, partendo dai pesi ottenuti su “imagenet”. Sia la tipologia di rete sia l’input size usata sono state scelte per ottenere un buon compromesso fra velocità di elaborazione e performance. Una rete con input size più grande avrebbe migliorato le performance del sistema, a discapito del tempo richiesto. Per quanto riguarda la rete, invece, la scelta è ricaduta su MobilenetV2 in quanto ha una dimensione piccola, bassa latenza e per soddisfare i vincoli di risorse di una varietà di casi d'uso, rispetto ad altre reti più “pesanti”.
Per adattare il sistema al nostro scopo, l’ultimo livello della rete MobilenetV2 è stato sostituito con 2 strati densi di 512 e 128 neuroni ciascuno (con funzione di attivazione “relu”), entrambi seguiti da uno strato di Dropout impostato a 0.20, e infine con un ultimo strato denso con funzione di attivazione “softmax”, costituito da 101 neuroni, uno per ogni classe da predire. I 2 strati densi che precedono l’ultimo costituito da 101 classi sono stati inseriti affinché la rete possa sfruttare e combinare in modo appropriato le feature estratte dalla CNN MobilenetV2.
La funzione di costo scelta è la “categorical cross-entropy”, in quanto si adatta bene al task di classificazione multi-classe. Ogni probabilità di classe predetta viene confrontata con l'output 0 o 1 desiderato della classe effettiva e viene calcolato una perdita che penalizza la probabilità in base a quanto è distante dal valore atteso effettivo. Questa funzione di costo richiede che le labels siano codificate in one-hot encoding.

## Descrizione dell'implementazione
La descrizione dettagliata dell'implementazione si può trovare nel file: "relazione_gruppo8.pdf"

## Comandi per lanciare la generazione del cvs GRUPPO_08.csv
Dalla cartella dove si trova il file "csv_test_gruppo8.py" lanciare il comando:

```bash
python3 csv_test_gruppo8.py --dir /Dataset/VGG/test/ --annotation /csv_folder/test.detected.csv --net gruppo8_mobilenet.h5 --csv GRUPPO_08.csv


--dir: Cartella del test (ossia la cartella contenente le cartelle delle identità
--annotation: Csv in cui ci sono le annotazioni per fare il crop
--net: Modello della rete
--csv: Nome del csv da generare 
```
NOTA BENE: Nel file "test.detected.csv" abbiamo riscontrato l'assenza delle immagini listate nel file "immagini_assenti.txt", per cui non è stato possibile effettuare il crop e quindi il test  

# Comandi per lanciare lo script usato per valutare le performance della rete

```bash
python3 test_mobilenet.py --dir /Dataset/training_resized/ --net gruppo8_mobilenet.h5 --csv_input /csv_folder/csv_training_reorganized_2000_160.csv

python3 test_mobilenet.py --dir /Dataset/validation_resized/ --net gruppo8_mobilenet.h5 --csv_input /csv_folder/validation_2000_160.csv

python3 test_mobilenet.py --dir /Dataset/VGG/train --net gruppo8_mobilenet.h5 --csv_input /csv_folder/our_test_2000_160.csv
```

NOTE: our_test_2000_160.csv si basa sulle immagini della cartella di train che non abbiamo usato per l'addestramento. Quindi le abbiamo considerate come test


# Documentazione
```
├── presentazione_gruppo8.pptx
├── relazione_gruppo8.pdf
├── GRUPPO_08.csv
```
# Struttura del progetto
```
├── testcode_gruppo8
│   ├── csv_test_gruppo8.py     --> Generazione del csv GRUPPO_08.csv
│   ├── test_mobilenet.py       --> Script per valutare le performance della rete
 
├── code_DATASET
│   ├── dataset_organization.py --> Selezione di k campioni per ogni classe secondo il criterio spiegato nella documentazione
│   ├── crop_images.py          --> Crop delle immagini in base alle coordinate lette dal file "annotation.csv"
│   ├── resize_image.py         --> Resize di tutte le immagini alla dimensione (160x160)
│   ├── split_dataset.py        --> 90% training set - 10% validation set
│   ├── generation_h5.py        --> Generazione del dataset in formato .h5py

├── code_CSV
│   ├── generate_csv_training_set.py          --> Generazione del csv del training set
│   ├── generate_csv_total.py                 --> Generazione del csv totale (VGG + UTK)
│   ├── generate_csv_remaining_for_test.py.   --> Generazione del csv per le immagini della cartella "train" del dataset VGG-Face2 non utilizzate per l'addestramento della rete

├── csv_folder
│   ├── csv_training_reorganized_2000_160.csv   --> Csv del training set riorganizzato
│   ├── validation_2000_160.csv                 --> Csv del validation_set
│   ├── dataset_complete_2000_160.csv           --> Csv del dataset completo utilizzato
```
File presenti sul link drive inviato per email:
```
├── csv_folder_remaining
│   ├── train.age_detected_vgg.csv              --> Csv delle annotazioni sulla cartella "train"
│   ├── annotation_vgg.csv                      --> Csv delle annotazioni per eseguire il crop sul train 
│   ├── test.detected.csv                       --> Csv delle annotazioni per eseguire il crop sul "test"

├── Dataset
│   ├── dataset_160.h5                          --> Dataset completo
│   ├── label_160.h5                            --> Labels
```



NOTE: la notazione "2000_160" sta ad indicare che i file sono riferiti al dataset generato come specificato nella documentazione. 

