
import pandas as pd
df = pd.read_csv('dataset-23-10-202522-48-03.txt',sep=',',header=0,index_col=False)
df.to_csv('DataSet3.csv', index=None)
