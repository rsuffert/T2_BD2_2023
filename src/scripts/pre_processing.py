import pandas as pd
from unidecode import unidecode
import numpy as np
import os
import csv

current_dir = os.path.dirname(__file__)
datasets_dir_path = os.path.join(current_dir, "..", "datasets")

raw_dataset_path = os.path.join(datasets_dir_path, "V_OCORRENCIA_AMPLA.csv")
df = pd.read_csv(raw_dataset_path, sep=";")

# 1. Filtering columns
df_treated = df[['Operacao', 'Operador_Padronizado', 'Descricao_do_Tipo', 
                 'Fase_da_Operacao', 'Aerodromo_de_Origem', 'Aerodromo_de_Destino']]

# 2. Removing accentuation and special characters
def replace_special_char(cell):
    if not isinstance(cell, str): return cell       # only operate on strings
    cell = unidecode(cell)                          # removing accentuation
    cell = cell.replace('ç', 'c').replace('Ç', 'C') # removing additional special character
    return cell.strip()
df_treated = df_treated.applymap(replace_special_char)

# 3. Keeping only "regular flights" and "air taxis"
df_treated = df_treated.query("Operacao in ('Voo Regular', 'Taxi Aereo')")

# 4. Standardize values
df_treated = df_treated.applymap(lambda x: "AZUL" if x == "AZUL LINHAS AEREAS BRASILEIRAS S.A." else x)
df_treated = df_treated.replace("", np.nan) # considering empty strings as null cells

# 5. For each airport, map how many accidents happened in each
airports_accidents = {}
takeoff_synonyms = ["Subida", "Decolagem"]
land_synonyms = ["Pouso", "Aproximacao", "Descida", "Procedimento de Aproximacao"]
for index, row in df_treated.iterrows():   # for each row in the dataset
    accident_phase = row[3]
    if accident_phase in takeoff_synonyms: # if the accident happened during takeoff, increment the number of accidents for the origin airport by one
        origin = row[4]
        if origin in airports_accidents: airports_accidents[origin] = airports_accidents[origin] + 1
        else:                            airports_accidents[origin] = 1
    elif accident_phase in land_synonyms:  # if the accident happened during landing, increment the number of accidents for the destination airport by one
        destination = row[5]
        if destination in airports_accidents: airports_accidents[destination] = airports_accidents[destination] + 1
        else:                                 airports_accidents[destination] = 1
# create a new CSV that stores the number of accidents for each airport in the dataset that has had an accident
airports_accidents_dataset_path = os.path.join(datasets_dir_path, "airports_accidents.csv")
with open(airports_accidents_dataset_path, "w") as file:
    writer = csv.writer(file, delimiter=';', lineterminator='\n')
    writer.writerow(['Airport','#Accidents'])
    for airport, accidents in airports_accidents.items():
        writer.writerow([airport,accidents])

# 6. Visualizing the data (summary of the dataset after transforming the data)
print(df_treated['Operacao'].value_counts())
print(df_treated['Operador_Padronizado'].value_counts())
print(df_treated['Fase_da_Operacao'].value_counts())
print(df_treated['Aerodromo_de_Destino'].value_counts())
print(df_treated['Descricao_do_Tipo'].value_counts())

print("\n\nGENERAL SUMMARY:")
print(df_treated.describe().transpose())

print("\n\nNULL VALUES PER COLUMN:")
print(df_treated.isnull().sum())

treated_dataset_path = os.path.join(datasets_dir_path, "dataset_treated.csv")
df_treated.to_csv(treated_dataset_path, sep=";")

#E.g.: getting TAP accidents
#print(df_treated.query("Operador_Padronizado == 'TAP AIR PORTUGAL'").shape[0])