import pandas as pd
import numpy as np
result_data = pd.read_csv("Result.txt", delim_whitespace=True, names=["l", "m", "n", "i"])
result_data = result_data.reset_index()  
result_data["Index"] = result_data.index + 1  
wannier_data = pd.read_csv("wannier90_hr.datO", delim_whitespace=True, names=[
    "l", "m", "n", "l1", "m1", "n1", "i", "j", "Re", "Im"
])

wannier_data_with_I = pd.merge(
    wannier_data,
    result_data,
    on=["l", "m", "n", "i"],
    how="left"
).rename(columns={"Index": "I"})
wannier_data_with_IJ = pd.merge(
    wannier_data_with_I,
    result_data,
    left_on=["l1", "m1", "n1", "j"],
    right_on=["l", "m", "n", "i"],
    how="left",
    suffixes=("_left", "_right")
).rename(columns={"Index": "J"})

final_output = wannier_data_with_IJ[["I", "J", "Re", "Im"]]
final_output.to_csv('matrix.datpro',sep='\t',index=False,header=False,float_format='%.14f')
print("Matrix Done")