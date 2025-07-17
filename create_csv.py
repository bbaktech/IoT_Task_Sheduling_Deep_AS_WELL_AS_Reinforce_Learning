
import pandas as pd
df = pd.read_csv('dataset-16-07-202508-54-03.txt',sep=',',header=0,index_col=False)
df.to_csv('DataSet3.csv', index=None)
