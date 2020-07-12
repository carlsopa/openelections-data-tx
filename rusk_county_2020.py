import tabula
import pandas as pd
pdf_file = 'RUSK_COUNTY-2020_MARCH_3RD_DEMOCRATIC_PRIMARY_332020-DEM Pct by Pct.pdf'
result = []
data = tabula.read_pdf(pdf_file,multiple_tables=True,pages='all')
for x in data:
    df = x
    df = df.rename(columns={'Unnamed: 0':'candidate','Unnamed: 2':'votes','Ballots By':'mail','Unnamed: 3':'early_voting','Election':'election_day'})
    #df = df.drop(columns=['Unnamed: 1'])
    #df = df.drop([0,1])
    #df = df.dropna(how='all')
    #df = df.dropna(subset=['candidate'])
    result.append(df)

pd.concat(result).to_csv('pd.csv')