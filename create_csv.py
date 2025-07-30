
import pandas as pd
df = pd.read_csv('dataset-29-07-202509-10-05.txt',sep=',',header=0,index_col=False)
df.to_csv('DataSet3.csv', index=None)
