
import pandas as pd
df = pd.read_csv('dataset-24-05-202520-53-50.txt',sep=',',header=0,index_col=False)
df.to_csv('DataSet2.csv', index=None)
