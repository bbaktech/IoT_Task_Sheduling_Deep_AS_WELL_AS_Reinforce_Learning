
import pandas as pd
df = pd.read_csv('dataset-09-08-202509-26-23.txt',sep=',',header=0,index_col=False)
df.to_csv('DataSet3.csv', index=None)
