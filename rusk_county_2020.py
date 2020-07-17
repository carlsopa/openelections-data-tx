import tabula
import pandas as pd
import numpy as np
import math

pdf_file = 'RUSK_COUNTY-2020_MARCH_3RD_DEMOCRATIC_PRIMARY_332020-DEM Pct by Pct.pdf'
headers = ['county','precinct','district','party','candidate','votes']
voting_style = ['early_voting','election_day','provisional','mail']
result = []
page = 1
data = tabula.read_pdf(pdf_file,guess=False,multiple_tables=True,pages=('all'))
for x in data:
    print(page)
    index = 0
    df = x
    df = df.drop(df.index[[0,1,2]])
    df = df[:-2]
    df = df.drop(columns = ['OFFICIAL RESULTS'])
    # print(df)
    
    #check to see if the data frame is the start of a new precinct.  If so, then remove the overall statistic data from it.
    if 'STATISTICS' in str(df.iloc[:,0][3]):
        df = df.drop(df.index[0:5])
        for x in df.index:
            if type(df.loc[x]['Unnamed: 1']) == str:
                if len(df.loc[x]['Unnamed: 1']) < 4:
                    if len(df.loc[x]['Unnamed: 1']) == 3:                      
                        df['Unnamed: 0'][x] =str(df.loc[x]['Unnamed: 1']).split()[0]
                        df['Unnamed: 1'][x] =str(df.loc[x]['Unnamed: 1']).split()[1]
        
        
        df = df.dropna(subset=['Summary Results Report'])
        
        df = df[~df['Summary Results Report'].str.contains('Ballots')]
    df = df.reset_index(drop=True)
    if len(df.columns)== 5:
        df = df.rename(columns={
            'Unnamed: 1':'mail',
            'Unnamed: 0':'total',
            'Unnamed: 2':'early voting',
            'Unnamed: 3':'election day'
        })
    if len(df.columns) >= 6:
       df = df.rename(columns={
        'Unnamed: 0':'total',       
        'Unnamed: 2':'mail',
        'Unnamed: 3':'early voting',
        'Unnamed: 4':'election day'
    })
           
    if len(df.columns) == 7:
       df = df.rename(columns={
        'Unnamed: 0':'total',       
        'Unnamed: 2':'mail',
        'Unnamed: 3':'early voting',
        'Unnamed: 4':'election day',
        'Unnamed: 5':'election day'
    }) 
    #clean up the first column, remove unneeded rows, and also any rows that have no values in it
    remove_strings=['Vote For 1','TOTAL']
    remove_strings_list = df.index[df['Summary Results Report'].isin(remove_strings)].tolist()
    df = df.drop(df.index[remove_strings_list])
    df = df.dropna(subset=['Summary Results Report'])    

    if 'Unnamed: 1' in df.columns:
        
        for index in df[df['Unnamed: 1'].notna()].index.tolist():
            df.loc[index,'total'] = df.loc[index,'Unnamed: 1']
        df = df.drop(columns=['Unnamed: 1']) 

    col_list = ['total','mail','early voting','election day']
    totals_index_list = df.index[df['total'].isna()].tolist()
    count_lst = df.loc[totals_index_list].isnull().sum(axis=1)
    # print(df)
    # print(df.loc[totals_index_list])
    for index, value in count_lst.items():
        # print(index)      
        if value <= 3:
            
            row = df.loc[[index]]
            # print(row)
            try:
                count = float(df.loc[index]['Summary Results Report'].rsplit(' ',1)[1])
                name = df.loc[index]['Summary Results Report'].rsplit(' ',1)[0]
                df.loc[index,'total'] = count
                df.loc[index,'Summary Results Report'] = name
                #print('second')
            except:
                break
      

    df = df.dropna(axis='columns',how='all')
    
    # print(df)
    print('----------')        

    df = df.reset_index(drop=True)
    df = df.dropna(how='all')
    result.append(df)
    page = page+1

pd.concat(result).to_csv('pdb.csv')