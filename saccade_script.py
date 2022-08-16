# saccade script
# get subject ID, saccade # (per subjID, timestamp, start of sac, end of sac, start/end AOI)
# write to xlsx file
# you may need to change the req_cols in line 16, depending on how many AOIs are in a dataset. That should be all you need to change
import pandas as pd
import numpy as np
from itertools import groupby
from operator import itemgetter

#ENTER FILENAME AND DIRECTORY HERE
filetoread = 'saccadedata_trial1bmp (1).xlsx'
#YOU WILL ENTER WHERE YOU WANT THE OUTPUT FILE TO BE AT THE END OF THE SCRIPT (LINE 71)


# get dataframe
req_cols = [0, 3, 4, 8, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
df = pd.read_excel(filetoread)
pd.set_option("display.max_rows", None, "display.max_columns", None)

# create new dataframe to write to
dfColumns = ['subj', 'saccadeNum', 'compTime', 'startSac', 'endSac','PreAOI','PostAOI']

# list of all saccade indices
saccadeLoc = list(np.where(df['Eye movement type'] == "Saccade"))

# get first / last rows from sacccades
def group(L):
    first = last = L[0]
    for n in L[1:]:
        if n - 1 == last:
            last = n
        else:
            yield first, last
            first = last = n
    yield first, last


firstLast = list(group(saccadeLoc[0]))

# print(df.iloc[saccadeLoc[0][0], 4:])
data = []
saccadeNum = 0
for x, y in firstLast:
    prevFix = x - 1
    postFix = y + 1
    subId = (df.iloc[x, 1])
    #saccadeNum
    timestamp = (df.iloc[x, 0])
    startSac = x
    endSac = y
    preAoi = (df.iloc[prevFix, 4:])
    i = 4
    preAoiList = []
    for item in preAoi:
        if item == 1:
            preAoiList.append(df.columns[i])
        i += 1
    postAoi = (df.iloc[postFix, 4:])
    postAoiList = []
    i = 4
    for item in postAoi:
        if item == 1:
            postAoiList.append(df.columns[i])
        i += 1
    for item in preAoiList:
        if "WordLine" in item:
            preAioPrio = item
        elif "Face" in item:
            preAioPrio = item
        elif "Button" in item:
            preAioPrio = item
        elif "Image" in item:
            preAioPrio = item
        else:
            preAioPrio = ""
    for item in postAoiList:
        if "WordLine" in item:
            postAioPrio = item
        elif "Face" in item:
            postAioPrio = item
        elif "Button" in item:
            postAioPrio = item
        elif "Image" in item:
            postAioPrio = item
        else:
            preAioPrio = ""
    row = [subId, saccadeNum, timestamp, x, y,preAoiList,postAoiList,preAioPrio,postAoiPrio]
    data.append(row)
    saccadeNum += 1

df2 = pd.DataFrame(data, columns=dfColumns)

#ENTER THE DIRECTORY YOUR OUTPUT NEEDS TO GO HERE, DO NOT REMOVE THE 'r' NEXT TO FILE LOCATION, KEEP SINGLE QUOTATIONS
df2.to_excel(r'C:\Users\Rober\Desktop\files\export2.xlsx', index=False)
# EX df2.to_excel(r'C:\Users\Rob\Desktop\fubar.xlsx', index=False)
