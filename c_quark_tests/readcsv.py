import pandas as pd
import math

columns_data = [
    'quark', 'model', 'process', 'order',  'YPDG', 'my(GeV)', 'XPDG', 'mx(GeV)', 'coupling_name', 'coupling', 'XS', 'CS(pb)', 'Tag', 'FileExtension'
]

inputfile = "Sigmas.csv"

df = pd.read_csv(inputfile)#, columns=columns_data)
#df = df.drop(columns=['YPDG', 'XPDG', 'coupling_name', 'XS', 'Tag', 'FileExtension'])


mY =1300
mX = 900
order = "LO"
model = "F3S"
coupling = 3.5

df['CShat(pb)'] = df['CS(pb)']/df['coupling']


df = df[df["model"] == model]

print(df["coupling"].unique())
df = df.replace('YYt', 'YYtPP')
df = df.replace('YYbt', 'YYtPM')
df = df.replace('YbYbt', 'YYtMM')

float_cols = ['my(GeV)', 'mx(GeV)', 'coupling','CS(pb)']

for col in float_cols:
    df[col] = df[col].astype(float)

#rescale_xsec_XX=df[(df["model"] == model) & (df["my(GeV)"] == my) & (df["mx(GeV)"] == mx) & (df["order"] == order) & (df["process"] == proc)].values[0]#['CShat(pb)'].values[0]


#print(rescale_xsec_XX[rescale_xsec_XX["process"] == "XX"])



rescale_xsec_XX = 0
rescale_xsec_XY = 0
rescale_xsec_YYi = 0
rescale_xsec_YYQCD = 0
rescale_xsec_YYtPP = 0
rescale_xsec_YYtPM = 0
rescale_xsec_YYtMM = 0
coupling_power = {'XX' : 4, 'XY':2, 'YYi':2, 'YYQCD': 0, 'YYtPP': 4, 'YYtPM': 4, 'YYtMM': 4}

select_row = df[(df["my(GeV)"] == mY) & (df["mx(GeV)"] == mX) ]
select_row_order  = df[(df["my(GeV)"] == mY) & (df["mx(GeV)"] == mX)  & (df["order"] == order)]
select_row_YYi  = df[(df["my(GeV)"] == mY) & (df["mx(GeV)"] == mX) & (df["process"] == 'YYi') & (df["order"] == 'LO')]

# calculate k factor
xsec_YYQCD_LO=select_row[(select_row["process"] == 'YYQCD') & (select_row['order'] == 'LO')]['CShat(pb)'].values[0]

xsec_YYtPM_LO=select_row[(select_row["process"] == 'YYtPM') & (select_row['order'] == 'LO')]['CShat(pb)'].values[0]


if order == "NLO":
    xsec_YYQCD_NLO=select_row[(select_row["process"] == 'YYQCD') & (select_row['order'] == 'NLO')]['CShat(pb)'].values[0]
    xsec_YYtPM_NLO=select_row[(select_row["process"] == 'YYtPM') & (select_row['order'] == 'NLO')]['CShat(pb)'].values[0]

if xsec_YYQCD_LO == 0 or xsec_YYtPM_LO == 0:
    print("missing YYQCD at LO or YYtPM at LO")
    sys.exit()


if order == "NLO":
    Kfactor_YYi = math.sqrt((xsec_YYQCD_NLO*xsec_YYtPM_NLO)/(xsec_YYQCD_LO*xsec_YYtPM_LO))

if select_row_order.empty:
    print("no point found")
    sys.exit()

if order == "LO":
    rescale_xsec_YYi = select_row_YYi['CShat(pb)'].values[0]*coupling**coupling_power['YYi']
elif order == "NLO":
    rescale_xsec_YYi = select_row_YYi['CShat(pb)'].values[0]*coupling**coupling_power['YYi']*Kfactor_YYi

rescale_xsec_XX=select_row_order[select_row_order["process"] == 'XX']['CShat(pb)'].values[0]*coupling**coupling_power['XX']
rescale_xsec_XY=select_row_order[select_row_order["process"] == 'XY']['CShat(pb)'].values[0]*coupling**coupling_power['XY']
rescale_xsec_YYQCD=select_row_order[select_row_order["process"] == 'YYQCD']['CShat(pb)'].values[0]*coupling**coupling_power['YYQCD']
rescale_xsec_YYtPP=select_row_order[select_row_order["process"] == 'YYtPP']['CShat(pb)'].values[0]*coupling**coupling_power['YYtPP']
rescale_xsec_YYtPM=select_row_order[select_row_order["process"] == 'YYtPM']['CShat(pb)'].values[0]*coupling**coupling_power['YYtPM']
rescale_xsec_YYtMM=select_row_order[select_row_order["process"] == 'YYtMM']['CShat(pb)'].values[0]*coupling**coupling_power['YYtMM']
#rescale_xsec_YYi=select_row_order_YYi[select_row_order_YYi["process"] == 'YYi']['CShat(pb)'].values[0]*coupling**coupling_power['YYi']

print(select_row_order[select_row_order["process"] == 'YYtMM']["XPDG"])

print(select_row_order[select_row_order["process"] == 'YYtMM']["FileExtension"])


