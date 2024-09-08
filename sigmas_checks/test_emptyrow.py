import pandas as pd


file_path="F3S_sigmas.dat"

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


num_columns = 15  
columns_data=['my(GeV)', 'mx(GeV)', 'quark', 'wy/my', 'coupling', 'process', 'order', 'lhapdfID', 'CS(pb)', 
                                    'stat(%)', 'scale+(%)', 'scale-(%)', 'PDF+(%)', 'PDF-(%)', 'CShat(pb)']

num_rows = len(data) // num_columns  # Calculate the number of rows
data_rows = [data[i:i+num_columns] for i in range(0, len(data), num_columns)]


# Convert the 2D list into a Pandas DataFrame
df = pd.DataFrame(data_rows, columns=columns_data)

df = df.drop(df.index[0])

float_cols = ['my(GeV)', 'mx(GeV)', 'coupling','CS(pb)','stat(%)', 'scale+(%)', 'scale-(%)', 'PDF+(%)', 'PDF-(%)', 'CShat(pb)']

print(df[1100:1200])


for col in float_cols:
    if col in df.columns:

        df[col] = pd.to_numeric(df[col], errors='coerce')
        problematic_rows = df[df[col].isna()]
        if not problematic_rows.empty:
            print(f"Problematic entries in column '{col}':")
            print(problematic_rows)
    else:
        print(f"Column '{col}' not found in the DataFrame.")


for col in float_cols:
    df[col] = df[col].astype(float)

