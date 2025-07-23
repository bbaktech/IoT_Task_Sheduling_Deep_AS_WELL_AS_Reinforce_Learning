
import pandas as pd
df = pd.read_csv('dataset-23-07-202523-00-59.txt',sep=',',header=0,index_col=False)
df.to_csv('DataSet3.csv', index=None)
