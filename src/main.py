import pandas as pd

operations_index = pd.read_excel("../data/operations.xlsx", index_col=2)
print(operations_index.head(2))