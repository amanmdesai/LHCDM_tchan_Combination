import sys
import os
import pandas as pd

folderName = "Sigmas"
fileName = "S3M_sigmas.dat"
inputfile = os.path.join(folderName,fileName)


import pandas as pd

# Define the file path
file_path = inputfile

# Read the file content
with open(file_path, 'r') as file:
    content = file.read()

# Replace all pipe symbols with spaces
data = content.replace('|', ' ')
data=data.split(" ")
data = [x for x in data if x.strip()]
print(data[13])


# Define the separator pattern
#separator_pattern = r'\s*\|\s*'
#cols = ["my(GeV)", "mx(GeV)", "coupling","quark","process","order","lhapdfID","CS(pb)","stat(%)","scale+(%)","scale-(%)","PDF+(%)","PDF-(%)","CShat(pb)"]   

# Read the file using pandas
#data = pd.read_csv(file_path, names=cols,sep=separator_pattern, engine='python')

# Display the data
#print(data)#["my(GeV)"])

"""

f = open(inputfile,'r')
data = f.read().split('|')
data_read = []
#.split('\n')
print(data)


cols = ["my(GeV)", "mx(GeV)", "coupling","quark","process","order","lhapdfID","CS(pb)","stat(%)","scale+(%)","scale-(%)","PDF+(%)","PDF-(%)","CShat(pb)"]   

result = pd.read_csv(inputfile,names=cols,index_col=None,sep='\t') #

print(result)

print(result["my(GeV)"])
"""

#print(inputfile)
#cols = ["my(GeV)", "mx(GeV)", "coupling","quark","process","order","lhapdfID","CS(pb)","stat(%)","scale+(%)","scale-(%)","PDF+(%)","PDF-(%)","CShat(pb)"]   
#print(result)
#result['Col'].str.replace('|', ':')
#print(result["my(GeV)"])
#print(result, result.columns)
#f = open(inputfile,'r')
#data = f.readlines()#.split('\t')
#data.remove(" | ")
#print(data)