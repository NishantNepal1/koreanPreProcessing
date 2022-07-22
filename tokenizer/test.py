
import csv

with open('../preprocessedData/posTagReviewDataNoStop.csv.csv', 'r', encoding="utf-8") as file:
    my_reader = csv.reader(file, delimiter=',')
    for index, row in enumerate(my_reader):
        if index == 0: continue
        #print(type(row[0]),type(row[1]), type(row[2]))
        listRep = row[2].strip('][').split(', ')
        print(type(listRep))
        print(index)

"""
import pandas as pd

# read text file into pandas DataFrame
df = pd.read_csv("stopwords-ko.txt", sep="/n")

# display DataFrame
df.to_csv("stopwordsKorean.csv")



print(df)
"""