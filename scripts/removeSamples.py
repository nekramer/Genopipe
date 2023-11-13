import sys
import pandas as pd
import difflib
import os

# Read in samples to remove
removeSamples = pd.read_csv(sys.argv[1], sep = " ")

removePLINK = []
for row in removeSamples.itertuples():

    if os.path.isfile('output/binary/' + row.Batch + '.fam') == False:
        print('Files for batch ' + row.Batch + ' not found. Skipping...')
    else:

        famFile = pd.read_csv('output/binary/' + row.Batch + '.fam', sep = " ", header = None)

        # Match donor to 2nd column
        donorID = difflib.get_close_matches(row.Donor, famFile.iloc[:,1], 1, cutoff = 0.4)[0]

        # Select FID and within-family id columns
        colIDs = famFile.loc[(famFile[1] == donorID)][[0, 1]]

        removePLINK.append(colIDs)

if len(removePLINK) > 0:
    removePLINK_df = pd.concat(removePLINK)
    removePLINK_df.to_csv("remove.plink", sep = " ", header = False, index = False)
else:
    print('No samples to remove.')
    with open('remove.plink', 'w') as f:
        pass    

