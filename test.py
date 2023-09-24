import pandas as pd

'''
import csv
with open("data/anime-dataset-2023.csv", encoding="utf8") as csv_file:
    Anime_Data = csv.reader(csv_file, delimiter=",")
    Anime_Data = list(Anime_Data)

for a in Anime_Data:
    print(a)
'''

data = pd.read_csv("data/anime-dataset-2023.csv")
print(data)
data.head()
data.describe()
