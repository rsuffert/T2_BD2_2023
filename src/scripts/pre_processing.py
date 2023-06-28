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
df_treated = df[['Operacao', 'Operador_Padronizado', 'Descricao_do_Tipo', 'Data_da_Ocorrencia']]

# 2. Fix cell values
# removing accent marks and special characters
def replace_special_char(cell):
    if not isinstance(cell, str): return cell       # only operate on strings
    cell = unidecode(cell)                          # removing accent marks
    cell = cell.replace('ç', 'c').replace('Ç', 'C') # removing additional special character
    return cell.strip()
df_treated = df_treated.applymap(replace_special_char)
# extract the year in which the accident happened
df_treated['Data_da_Ocorrencia'] = df_treated['Data_da_Ocorrencia'].apply(lambda x: x.split('-')[0])
df_treated = df_treated.rename(columns={'Data_da_Ocorrencia': 'Ano_Ocorrencia'})

# 3. Keeping only "regular flights" and "air taxis"
df_treated = df_treated.query("Operacao in ('Voo Regular', 'Taxi Aereo')")

# 4. Standardize values
df_treated = df_treated.applymap(lambda x: "AZUL" if x == "AZUL LINHAS AEREAS BRASILEIRAS S.A." else x)
df_treated = df_treated.replace("", np.nan) # considering empty strings as null cells

# 5. Find out how many accidents happened for each year
year_accidents = {}
for index, row in df_treated.iterrows():
    accident_year = row['Ano_Ocorrencia']
    if accident_year in year_accidents: year_accidents[accident_year] = year_accidents[accident_year] + 1
    else:                               year_accidents[accident_year] = 1
# create a new CSV that stores the number of accidents for each airport in the dataset that has had an accident
year_accidents_dataset_path = os.path.join(datasets_dir_path, "year_accidents.csv")
with open(year_accidents_dataset_path, "w") as file:
    writer = csv.writer(file, delimiter=';', lineterminator='\n')
    writer.writerow(['Ano','Nro_Acidentes'])
    for year, accidents in year_accidents.items():
        writer.writerow([year,accidents])

# 6. Visualizing the data (summary of the dataset after transforming the data)
print(df_treated['Operacao'].value_counts())
print(df_treated['Operador_Padronizado'].value_counts())
print(df_treated['Descricao_do_Tipo'].value_counts())
print(df_treated['Ano_Ocorrencia'].value_counts)

print("\n\nGENERAL SUMMARY:")
print(df_treated.describe().transpose())

print("\n\nNULL VALUES PER COLUMN:")
print(df_treated.isnull().sum())

treated_dataset_path = os.path.join(datasets_dir_path, "dataset_treated.csv")
df_treated.to_csv(treated_dataset_path, sep=";")

#E.g.: getting TAP accidents
#print(df_treated.query("Operador_Padronizado == 'TAP AIR PORTUGAL'").shape[0])