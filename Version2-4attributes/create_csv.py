
import pandas as pd
df = pd.read_csv('dataset-23-07-202522-34-57.txt',sep=',',header=0,index_col=False)
df.to_csv('DataSet4.csv', index=None)
