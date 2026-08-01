import pandas as pd
import numpy as np
import openpyxl as xl
import matplotlib as stat


a = np.random.randint(2, 9, size=[3, 4], dtype=np.int16)

# print(a)

df = pd.DataFrame(a, index=["P", "Q", "R"], columns=["A", "B", "C", "D"])

print(df.shape)


coffee = pd.read_csv(
    "https://raw.githubusercontent.com/KeithGalli/complete-pandas-tutorial/refs/heads/master/warmup-data/coffee.csv")

print(coffee)

print(coffee.sample(10))
