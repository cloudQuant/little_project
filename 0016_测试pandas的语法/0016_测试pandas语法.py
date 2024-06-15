import pandas as pd

df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6, 7, 8],
                   'b': [1, 2, 3, 4, 5, 6, 7, 8],
                   'id': [1, 1, 1, 1, 2, 2, 2, 3]})

df1 = df.groupby(['id'], as_index=True).a.sum()
print(df1.idxmax())
