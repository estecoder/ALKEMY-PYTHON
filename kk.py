from typing import List
import pandas as pd
from config import Postgres as pg

df = pd.DataFrame(
	{
		"A":[],
		"B":[],
		"C":[],
	}
)
d = []
for i in range(0,5):
	d.append(i)
df["B"] = d
print(df["A"].empty)
print(df["A"].dropna().empty)
print(df["A"].all())
