# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

df = pd.read_pickle('concatenated.pkl')
df = df.dropna(subset = ['PY','CR'])  # Get rid of badly imported data
cited_ref = df.CR
orig_art_yr = df.PY

a = cited_ref.size
refs_per = np.zeros(a)  # Citations per article
name = []               # Citation author
year = []               # Cited article year of pub
age = []                # Cited article age wrt published art.
journal = []            # Journal name of cited article

for i, row in enumerate(cited_ref.values):
    auths = cited_ref.values[i]   # Read the cell with all the citations for one article
    parts = auths.split(';')      # Split the citations based on semi-colon
    refs_per[i] = 0;              # Count the number of citations
    
# Split the citation into parts based on comma to get the year and journal name
    for j in parts:
        if len(j.split(',')) == 3:
             n,y,jou =  j.split(',')
        elif len(j.split(',')) == 4:
             n,y,jou,ver =  j.split(',')
        elif len(j.split(',')) == 5:
             n,y,jou,ver,page =  j.split(',')
        elif len(j.split(',')) == 6:
             n,y,jou,ver,page,doi =  j.split(',')
        y = y.strip()
        if y.isdigit():      # Some citations don't have a year, throw  them away
            name.append(n)
            year.append(y)            
            year = [int(i) for i in year]
            temp = orig_art_yr.values[i] - float(y)
            age.append(temp)         
            journal.append(jou)
            refs_per[i] += 1
        else:
            pass

## Write the Top Most Cited Journals to csv file                
journal = [x.upper() for x in journal]  # Convert all names to uppercase
cc = Counter(journal)
p = cc.most_common()
cols = ['name','count']
pp = pd.DataFrame(p,columns = cols)
pp['name'] = pp['name'].str.upper()  # Convert all names to uppercase
pp = pp.set_index('name')
pp = pp.groupby(pp.index).sum()      # Find duplicate names and add the counts
pp = pp.sort_values(['count'], ascending = [False])   # Sort list by counts
pp.to_csv('MaxCitedJournals.csv')                    # Write to csv file

