
import pandas as pd
import sys
import csv
maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


# pipeline not created
# change the name of the file
stopWordfile = 'stopwordsKorean.csv'
stopWordList = set()

with open(stopWordfile, 'r', encoding="utf-8") as file:
    my_reader = csv.reader(file, delimiter=',')
    for index, row in enumerate(my_reader):
        if index == 0: continue
        stopWordList.add(row[1])

print(len(stopWordList))
stopWordList = list(stopWordList)
# posTaggedData file
# change posFil path

posFile = '../preprocessedData/posTagDescData.csv'

outList = []
with open(posFile, 'r', encoding='utf-8') as file:
    my_reader = csv.reader(file, delimiter=",")
    for index, row in enumerate(my_reader):
        # Skip first line if title is set
        if index == 0: continue
        #print(row[1])
        listRep = x = [x for x in eval(row[3])]
        refWordPos = []
        #removing stop words
        for items in listRep:
            if items[0] in stopWordList:
                continue
            else:
                refWordPos.append(items)
        #creating Tokens
        tokens = []
        for items in listRep:
            tokens.append(items[0])
        # print(index, len([row[0], row[1], row[2], listRep,  refWordPos]))
        outList.append([row[0], row[1], row[2], tokens,listRep,  refWordPos])
        #print(row[1], tokens, listRep, refWordPos)
        print(index)
        #outList.append([row[0], tokens, listRep, refWordPos])
df = pd.DataFrame(list(outList), columns=["English Name", "Korean Name","Unfiltered Description", "Tokens","POS",
 "POS NO STOP "])
#df = pd.DataFrame(outList, columns=["Unfiltered Description", "Tokens", "POS", "POS NO STOP"])
df.to_csv("../preprocessedData/posTagDescReviewNoStop.csv")
