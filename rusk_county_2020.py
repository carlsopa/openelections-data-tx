#left to right: 215mm
#top: 30
#bottom: 260
#left 0
#right 210
#Registered Voters, Ballots Cast, Straight Party, President, US Senate, US House, Railroad Commissioner, State Senate, State Represenative

import tabula
import pandas as pd
import numpy as np
pdf_file = 'RUSK_COUNTY-2020_MARCH_3RD_DEMOCRATIC_PRIMARY_332020-DEM Pct by Pct.pdf'
headers = ['county','precinct','district','party','candidate','votes']
voting_style = ['early_voting','election_day','provisional','mail']
result = []

data = tabula.read_pdf(pdf_file,guess=False,multiple_tables=True,pages=('1-3'))
for x in data:
    index = 0
    df = x
    df = df.drop(df.index[[0,1,2]])
    df = df[:-2]
    df = df.drop(columns = ['OFFICIAL RESULTS'])
    if 'STATISTICS' in str(df.iloc[:,0][3]):
        print('found')
        df = df.drop(df.index[[0,1,2,3,4]])


    # df = df.rename(columns={'Unnamed: 0':'candidate','Unnamed: 2':'votes','Ballots By':'mail','Unnamed: 3':'early_voting','Election':'election_day'})

#     #df = df.drop([0,1])
#     #df = df.dropna(how='all')
#     #df = df.dropna(subset=['candidate'])
#     result.append(df)
    print(df)
#print(data)
#pd.concat(result).to_csv('pd.csv')