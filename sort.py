import pandas as pd
df=pd.read_table("wannier90_hr.datO",sep="    ",header=None)
s1=df.iloc[:,[0,1,2,6]]
s2=df.iloc[:,[3,4,5,7]]
s1.columns=[0,1,2,3];s2.columns=[0,1,2,3]
s3 = pd.concat([s1, s2], ignore_index=True)
sorts = s3.drop_duplicates().sort_values(by=[0, 1, 2, 3], ascending=[True, True, True, True]).reset_index(drop=True)
sorts.to_csv('Result.txt', sep='\t', index=False, header=False)
print("Sorting Done.")
