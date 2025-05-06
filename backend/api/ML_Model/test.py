import pandas as pd

df = pd.read_csv('twitter_training.csv', header=None)
u = df[1].unique()
print(u)