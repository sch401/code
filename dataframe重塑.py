import pandas as pd
import numpy as np
Sourcedata = pd.read_excel("全时间拆分.xlsx", sheet_name="Sheet1")
columns = Sourcedata.columns.to_list()

training = Sourcedata.sample(frac=0.7, random_state=42)

testing = Sourcedata.drop(training.index)

training = training.melt(id_vars=columns[:-53], value_vars=columns[-53:], var_name='DT', value_name='EMY')
testing = testing.melt(id_vars=columns[:-53], value_vars=columns[-53:], var_name='DT', value_name='EMY')


training.dropna(subset=['EMY'], inplace=True)
testing.dropna(subset=['EMY'], inplace=True)


training.to_excel("training.xlsx",index=False)
testing.to_excel("testing.xlsx",index=False)
