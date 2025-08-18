
import pandas as pd
df = pd.read_csv('dataset-18-08-202509-52-48.txt',sep=',',header=0,index_col=False)
df.to_csv('DataSet3.csv', index=None)
