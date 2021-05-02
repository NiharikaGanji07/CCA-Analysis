# -*- coding: utf-8 -*-
import pandas as pd
import glob
import codecs
import csv

df_list = []
path = 'Sentiment.csv'    # input desired location of converted files                
for fname in glob.glob(path):
    df_list.append(pd.read_csv(fname))

complete_df = pd.concat(df_list)
complete_df.to_pickle('concatenated.pkl')
