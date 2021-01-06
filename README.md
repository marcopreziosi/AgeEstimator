# Marco Preziosi - Stefano Saldutti - Salvatore Reina - Bruno Vento 
# Progetto Artificial Vision gruppo 8

Il file di addestramento è "gruppo8_train_mobilenet.ipynb"
Il modello usato per la valutazione delle performance è "gruppo8_mobilenet.h5"


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
│   ├── train.age_detected_vgg.csv              --> Csv delle annotazioni sulla cartella "train"
│   ├── annotation_vgg.csv                      --> Csv delle annotazioni per eseguire il crop sul train
│   ├── test.detected.csv                       --> Csv delle annotazioni per eseguire il crop sul "test"
│   ├── csv_training_reorganized_2000_160.csv   --> Csv del training set riorganizzato
│   ├── validation_2000_160.csv                 --> Csv del validation_set
│   ├── dataset_complete_2000_160.csv           --> Csv del dataset completo utilizzato
```

NOTE: la notazione "2000_160" sta ad indicare che i file sono riferiti al dataset generato come specificato nella documentazione. 

