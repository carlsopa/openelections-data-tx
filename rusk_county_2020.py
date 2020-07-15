import tabula
import pandas as pd
import numpy as np
import math
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
    
    #check to see if the data frame is the start of a new precinct.  If so, then remove the overall statistic data from it.
    if 'STATISTICS' in str(df.iloc[:,0][3]):
        df = df.drop(df.index[0:5])
        df[['total','mail']] = df['Unnamed: 1'].str.split(expand=True)
        df.reindex(columns=['Summary Results Report','Unnamed: 0','mail','Unnamed: 2','Unnamed: 3','total','Unnamed: 1'])
        df['Unnamed: 0'] = df['Unnamed: 0'].combine_first(df['total'])
        df = df.drop(columns=['Unnamed: 1','total'])
        df = df.rename(columns={
            'Unnamed: 0':'total',
            'Unnamed: 2':'early voting',
            'Unnamed: 3':'election day'
        })
    df = df.reset_index(drop=True)
    
    #clean up the first column, remove unneeded rows, and also any rows that have no values in it
    remove_strings=['Vote For 1','TOTAL']
    remove_strings_list = df.index[df['Summary Results Report'].isin(remove_strings)].tolist()
    df = df.drop(df.index[remove_strings_list])
    df = df.dropna(subset=['Summary Results Report'])    
    df = df.dropna(axis='columns',how='all')
    df = df.rename(columns={
        'Unnamed: 0':'total',
        'Unnamed: 2':'mail',
        'Unnamed: 3':'early voting',
        'Unnamed: 4':'election day'
    })
    #print(df)
    col_list = ['total','mail','early voting','election day']
    totals_index_list = df.index[df['total'].isna()].tolist()
    count_lst = df.loc[totals_index_list].isnull().sum(axis=1)
    for index, value in count_lst.items():
        if value == 1:
            row = df.loc[[index]]
            df['total'][index] = row['Summary Results Report'].str.rsplit().str[-1]
            name = row['Summary Results Report'].str.rsplit(n=1).str[0]
            #print(df.loc[index]['Summary Results Report'].rsplit(' ',1)[0])
            df['Summary Results Report'][index] = df.loc[index]['Summary Results Report'].rsplit(' ',1)[0]
            
            
    
    #print(df)




    df = df.reset_index(drop=True)
    df = df.dropna(how='all')
    result.append(df)
print(result)
#pd.concat(result).to_csv('pda.csv')