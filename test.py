import pandas as pd
import pickle
import requests

'''
import csv
with open("static/anime-dataset-2023.csv", encoding="utf8") as csv_file:
    Anime_Data = csv.reader(csv_file, delimiter=",")
    Anime_Data = list(Anime_Data)

for a in Anime_Data:
    print(a)
'''



data = pd.read_csv("static/anime-dataset-2023.csv")
print(data)
data.head()
data.describe()
