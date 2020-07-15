#left to right: 215mm
#top: 30
#bottom: 260
#left 0
#right 210
#Registered Voters, Ballots Cast, Straight Party, President, US Senate, US House, Railroad Commissioner, State Senate, State Represenative

import tabula
import pandas as pd
import numpy as np
import math
pdf_file = 'RUSK_COUNTY-2020_MARCH_3RD_DEMOCRATIC_PRIMARY_332020-DEM Pct by Pct.pdf'
headers = ['county','precinct','district','party','candidate','votes']
voting_style = ['early_voting','election_day','provisional','mail']
result = []

data = tabula.read_pdf(pdf_file,guess=False,multiple_tables=True,pages=('1-9'))
for x in data:
    index = 0
    df = x
    df = df.drop(df.index[[0,1,2]])
    df = df[:-2]
    df = df.drop(columns = ['OFFICIAL RESULTS'])
    
    #check to see if the data frame is the start of a new precinct.  If so, then remove the overall statistic data from it.
    if 'STATISTICS' in str(df.iloc[:,0][3]):
        df.drop(df.index[0:5],inplace=True)
        df[['total','mail']] = df['Unnamed: 1'].str.split(expand=True)
        df.reindex(columns=['Summary Results Report','Unnamed: 0','mail','Unnamed: 2','Unnamed: 3','total','Unnamed: 1'])
        df['Unnamed: 0'] = df['Unnamed: 0'].combine_first(df['total'])
        df.drop(columns=['Unnamed: 1','total'],inplace=True)
    df.reset_index(drop=True,inplace=True)
    
    #clean up the first column, remove unneeded rows, and also any rows that have no values in it
    remove_strings=['Vote For 1','TOTAL']
    result = df.index[df['Summary Results Report'].isin(remove_strings)].tolist()
    df.drop(df.index[result],inplace=True)
    df.dropna(subset=['Summary Results Report'],inplace=True)    
    df.dropna(axis='columns',how='all',inplace=True)


  #Unnamed: 0 = Total, 
    #df.rename(columns={'Unnamed: 0':'candidate','Unnamed: 2':'votes','Ballots By':'mail','Unnamed: 3':'early_voting','Election':'election_day'},inplace=True)

    #df = df.drop([0,1])
    df = df.dropna(how='all')
    #df = df.dropna(subset=['candidate'])
    print(df)
    result.append(df)
#print(data)
#pd.concat(result).to_csv('pda.csv')