import sys
import os
import pandas as pd

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

data.remove
num_columns = 14  # Number of columns in each row
num_rows = len(data) // num_columns  # Calculate the number of rows
data_rows = [data[i:i+num_columns] for i in range(0, len(data), num_columns)]


# Convert the 2D list into a Pandas DataFrame
df = pd.DataFrame(data_rows, columns=['my(GeV)', 'mx(GeV)', 'coupling', 'quark', 'process', 'order', 'lhapdfID', 'CS(pb)', 
                                     'stat(%)', 'scale+(%)', 'scale-(%)', 'PDF+(%)', 'PDF-(%)', 'CShat(pb)'])

df = df.drop(df.index[0])

float_cols = ['my(GeV)', 'mx(GeV)', 'coupling','CS(pb)','stat(%)', 'scale+(%)', 'scale-(%)', 'PDF+(%)', 'PDF-(%)', 'CShat(pb)']

for col in float_cols:
    #print(col,df[col])
    df[col] = df[col].astype(float)



# define point
mY = 2800
mX = 1200
proc = 'XX'
order = 'NLO'
couplings = [0.1,3.5]
coupling_power = {'XX' : 4, 'YYt': 4}


select_XXrow  = df[(df["my(GeV)"] == mY) & (df["mx(GeV)"] == mX) & (df['process']==proc) & (df['order'] == order)]

if select_XXrow.empty:
    print("no point found")
    sys.exit()


for coup in couplings:
    print(select_XXrow['CShat(pb)']*coup**coupling_power[proc])