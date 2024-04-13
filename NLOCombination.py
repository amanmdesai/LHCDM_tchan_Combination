import sys
import os
import pandas as pd


# define point
mY = 2800
mX = 1200
proc = 'XX'
order = 'NLO'
couplings = [3.5,5.0]
coupling_power = {'XX' : 4, 'XY':2, 'YYi':2, 'YYQCD': 0, 'YYtPP': 4, 'YYtPM': 4, 'YYtMM': 4}

quark = 'u'
model = 'S3M'

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


select_XXrow  = df[(df["my(GeV)"] == mY) & (df["mx(GeV)"] == mX) & (df['process']==proc) & (df['order'] == order)]

if select_XXrow.empty:
    print("no point found")
    sys.exit()

val = {}

for coup in couplings:
    val[coup]=select_XXrow['CShat(pb)']*coup**coupling_power[proc]
    #print(val)


name_recast_file = model + "_" + proc + "_" + order + "_SMu_" + "MY" + str(mY) + "_MX" + str(mX) + "_recast"

file = os.path.join(folderName, "MA5_Recast",name_recast_file+".tar.gz")

if os.path.exists(file):
    print("File found")
else:
    print("file not found exiting code")
    sys.exit()


print(file)