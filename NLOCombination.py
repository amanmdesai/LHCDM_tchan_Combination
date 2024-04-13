import sys
import os
import pandas as pd
from io import StringIO

folderName = "Sigmas"
fileName = "S3M_sigmas.dat"
inputfile = os.path.join(folderName,fileName)

# Define the file path
file_path = inputfile

# Read the file content
with open(file_path, 'r') as file:
    content = file.read()


# Replace all pipe symbols with spaces
raw_data = content.replace('|', ' ')
raw_data=raw_data.split(" ")
raw_data = [x for x in raw_data if x.strip()]

data = []
[data.extend(s.split('\n')) for s in raw_data]
data = list(filter(None, data))

print("newdata",data)
data.remove
num_columns = 14  # Number of columns in each row
num_rows = len(data) // num_columns  # Calculate the number of rows
print(num_rows)
data_rows = [data[i:i+num_columns] for i in range(0, len(data), num_columns)]

print(data_rows)

# Convert the 2D list into a Pandas DataFrame
df = pd.DataFrame(data_rows, columns=['my(GeV)', 'mx(GeV)', 'coupling', 'quark', 'process', 'order', 'lhapdfID', 'CS(pb)', 
                                     'stat(%)', 'scale+(%)', 'scale-(%)', 'PDF+(%)', 'PDF-(%)', 'CShat(pb)'])

print(df.head)
df = df.drop(df.index[0])
print(df.head)

float_cols = ['my(GeV)', 'mx(GeV)', 'coupling','CS(pb)','stat(%)', 'scale+(%)', 'scale-(%)', 'PDF+(%)', 'PDF-(%)', 'CShat(pb)']

for col in float_cols:
    print(col,df[col])
    df[col] = df[col].astype(float)

select_XXrow  = df[(df["my(GeV)"] == 2800) & (df["mx(GeV)"] == 1200) & (df['process']=='XX') & (df['order'] =='NLO')]

print(select_XXrow)

