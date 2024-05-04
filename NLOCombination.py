import argparse
import json
import logging
import sys
import ma5_expert as ma5
import pandas as pd
import tarfile
import shutil
import os


"""
def extract_tar(tar_file, destination):
    with tarfile.open(tar_file, 'r:gz') as tar:
        tar.extractall(destination)
"""

def extract_tar(tar_gz_file, extract_path):
    try:
        shutil.unpack_archive(tar_gz_file, extract_path, 'gztar')
        print(f"Successfully extracted '{tar_gz_file}' to '{extract_path}'.")
    except Exception as e:
        print(f"Error extracting '{tar_gz_file}': {e}")




# define point
mY = 1300
mX = 900
proc = 'Full'
order = 'NLO'
couplings = [3.5,5.0]
coupling = 5.0
coupling_power = {'XX' : 4, 'XY':2, 'YYi':2, 'YYQCD': 0, 'YYtPP': 4, 'YYtPM': 4, 'YYtMM': 4}
processes_full = ['XX','XY','YYi','YYQCD','YYtPP','YYtPM','YYtMM']
PAD4SFS = ["atlas_exot_2018_06"]
analysis_names = ["atlas_conf_2019_040","atlas_exot_2018_06",]#"cms_exo_20_004","cms_sus_19_006"]


luminosity=137

quark = 'd'
model = 'F3S'

#folderName = "/eos/user/a/aman/SamplesForAman/u/Results_F3S_recast"
#fileName = "Sigmas/F3S_sigmas.dat"

folderName = "/eos/user/a/aman/dsb_lowstat/Results_F3S_recast"
fileName = "Sigmas/F3S_sigmas.dat"

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
num_columns = 15  # Number of columns in each row
num_rows = len(data) // num_columns  # Calculate the number of rows
data_rows = [data[i:i+num_columns] for i in range(0, len(data), num_columns)]


# Convert the 2D list into a Pandas DataFrame
df = pd.DataFrame(data_rows, columns=['my(GeV)', 'mx(GeV)', 'quark', 'wy/my', 'coupling', 'process', 'order', 'lhapdfID', 'CS(pb)', 
                                     'stat(%)', 'scale+(%)', 'scale-(%)', 'PDF+(%)', 'PDF-(%)', 'CShat(pb)'])

df = df.drop(df.index[0])

float_cols = ['my(GeV)', 'mx(GeV)', 'coupling','CS(pb)','stat(%)', 'scale+(%)', 'scale-(%)', 'PDF+(%)', 'PDF-(%)', 'CShat(pb)']

for col in float_cols:
    #print(col,df[col])
    df[col] = df[col].astype(float)

select_row  = df[(df["my(GeV)"] == mY) & (df["mx(GeV)"] == mX)  & (df['order'] == order)]
select_row_YYi  = df[(df["my(GeV)"] == mY) & (df["mx(GeV)"] == mX)]

if select_row.empty:
    print("no point found")
    sys.exit()

processes_full = ['XX','XY','YYi','YYQCD','YYtPP','YYtPM','YYtMM']

rescale_xsec_XX = {}
rescale_xsec_XY = {}
rescale_xsec_YYi = {}
rescale_xsec_YYQCD = {}
rescale_xsec_YYtPP = {}
rescale_xsec_YYtPM = {}
rescale_xsec_YYtMM = {}

for coup in couplings:
    rescale_xsec_XX[coup]=select_row[select_row["process"] == 'XX']['CShat(pb)'].values[0]*coup**coupling_power['XX']
    rescale_xsec_XY[coup]=select_row[select_row["process"] == 'XY']['CShat(pb)'].values[0]*coup**coupling_power['XY']
    rescale_xsec_YYi[coup]=select_row_YYi[select_row_YYi["process"] == 'YYi']['CShat(pb)'].values[0]*coup**coupling_power['YYi']
    rescale_xsec_YYQCD[coup]=select_row[select_row["process"] == 'YYQCD']['CShat(pb)'].values[0]*coup**coupling_power['YYQCD']
    rescale_xsec_YYtPP[coup]=select_row[select_row["process"] == 'YYtPP']['CShat(pb)'].values[0]*coup**coupling_power['YYtPP']
    rescale_xsec_YYtPM[coup]=select_row[select_row["process"] == 'YYtPM']['CShat(pb)'].values[0]*coup**coupling_power['YYtPM']
    rescale_xsec_YYtMM[coup]=select_row[select_row["process"] == 'YYtMM']['CShat(pb)'].values[0]*coup**coupling_power['YYtMM']


# madanalysis expert mode 

ma5dir = "/eos/user/a/aman/LHCDM_tchan_Combination/madanalysis5"#ma5dir
if not os.path.isdir(ma5dir):
    sys.exit('Detected MadAnalysis 5 general folder is not correct: ' + ma5dir)
os.environ['MA5_BASE']=ma5dir

sys.path.insert(0, ma5dir)


# Adding the python service folder to the current PYTHONPATH
servicedir = ma5dir+'/tools/ReportGenerator/Services/'
servicedir = os.path.normpath(servicedir)
if not os.path.isdir(servicedir):
    sys.exit('Detected MadAnalysis 5 service folder is not correct: ' + ma5dir)
sys.path.insert(0, servicedir)


from madanalysis.core.main import Main as ma5_main
from madanalysis.misc.run_recast import RunRecast
from madanalysis.enumeration.ma5_running_type import MA5RunningType

main = ma5_main()
main.mode=MA5RunningType.RECO

main.forced         = False
main.script         = True
main.developer_mode = True
main.debug = True
main.InitObservables(main.mode)
main.archi_info.ma5dir = ma5dir

main.CheckConfig(debug=True)
main.CheckConfig2(debug=True)
main.recast = "on"


print(f"has PAD: {main.session_info.has_pad}\n"
      f"has PAD4SFS {main.session_info.has_padsfs}\n"
      f"has scipy {main.session_info.has_scipy}\n"
      f"has pyhf {main.session_info.has_pyhf}")

ma5.BackendManager.set_madanalysis_backend("/eos/user/a/aman/LHCDM_tchan_Combination/madanalysis5")

main_path = folderName

#"/home/amdesai/Music/LHCDM_tchan_Combination/installed_files/Sigmas"

# Samples to be combined. Each set of samples are generated and stored in separate directories


for proc in processes_full:

    if proc == "YYi":
        order_file = "LO"
    else:
        order_file = order

    name_recast_file = model + "_" + proc + "_" + order_file + "_SMd_" + "MY" + str(mY) + "_MX" + str(mX) + "_recast"

    file = os.path.join(folderName, "MA5_Recast",name_recast_file+".tar.gz")
    extract_tar(file, os.path.join(folderName, "MA5_Recast",))

    print(file)

    if os.path.exists(file):
        print("File found")
    else:
        print("file not found exiting code")
        sys.exit()

# Output folder

if proc == "Full":
    combined_path = "/eos/user/a/aman/LHCDM_tchan_Combination/output/" + model + "_" + proc + "_" + order_file + "_SMd_" + "MY" + str(mY) + "_MX" + str(mX) + "_recast" 
else:
    combined_path = "/eos/user/a/aman/LHCDM_tchan_Combination/output/" + name_recast_file 

if not os.path.isdir(combined_path):
    os.mkdir(combined_path)


#for coup in couplings:
for ana in analysis_names:
    XX_path  = os.path.join(main_path, "MA5_Recast/F3S_XX_NLO_SMd_MY1300_MX900_recast/Output/SAF/dmtsimp/{}/Cutflows".format(ana))
    XY_path  = os.path.join(main_path, "MA5_Recast/F3S_XY_NLO_SMd_MY1300_MX900_recast/Output/SAF/dmtsimp/{}/Cutflows".format(ana))
    YYi_path  = os.path.join(main_path, "MA5_Recast/F3S_YYi_LO_SMd_MY1300_MX900_recast/Output/SAF/dmtsimp/{}/Cutflows".format(ana))
    YYQCD_path  = os.path.join(main_path, "MA5_Recast/F3S_YYQCD_NLO_SMd_MY1300_MX900_recast/Output/SAF/dmtsimp/{}/Cutflows".format(ana))
    YYtPP_path  = os.path.join(main_path, "MA5_Recast/F3S_YYtPP_NLO_SMd_MY1300_MX900_recast/Output/SAF/dmtsimp/{}/Cutflows".format(ana))
    YYtPM_path  = os.path.join(main_path, "MA5_Recast/F3S_YYtPM_NLO_SMd_MY1300_MX900_recast/Output/SAF/dmtsimp/{}/Cutflows".format(ana))
    YYtMM_path  = os.path.join(main_path, "MA5_Recast/F3S_YYtMM_NLO_SMd_MY1300_MX900_recast/Output/SAF/dmtsimp/{}/Cutflows".format(ana))

    xsec_proc  = rescale_xsec_XX[coupling] + rescale_xsec_XY[coupling] + rescale_xsec_YYi[coupling] + rescale_xsec_YYQCD[coupling] + \
    rescale_xsec_YYtPP[coupling] + rescale_xsec_YYtPM[coupling] + rescale_xsec_YYtMM[coupling]
    
    xsec = xsec_proc

    XX_collection  = ma5.cutflow.Collection(XX_path,  xsection = rescale_xsec_XX[coupling],  lumi = luminosity,)
    XY_collection  = ma5.cutflow.Collection(XY_path,  xsection = rescale_xsec_XY[coupling],  lumi = luminosity,)
    YYi_collection  = ma5.cutflow.Collection(YYi_path,  xsection = rescale_xsec_YYi[coupling],  lumi = luminosity,)
    YYQCD_collection = ma5.cutflow.Collection(YYQCD_path, xsection = rescale_xsec_YYQCD[coupling], lumi = luminosity,)
    YYtPP_collection = ma5.cutflow.Collection(YYtPP_path, xsection = rescale_xsec_YYtPP[coupling], lumi = luminosity,)
    YYtPM_collection = ma5.cutflow.Collection(YYtPM_path, xsection = rescale_xsec_YYtPM[coupling], lumi = luminosity,)
    YYtMM_collection = ma5.cutflow.Collection(YYtMM_path, xsection = rescale_xsec_YYtMM[coupling], lumi = luminosity,)

    if not os.path.isdir(combined_path):
        os.mkdir(combined_path)

    with open(os.path.join(combined_path,'sample_info_proc.json'),'w') as info_file:
        info = {"xsec" : float(xsec)}
        json.dump(info, info_file, indent = 4)

    # Run Recast
    main.datasets.Add("dmtsimp")
    main.datasets.Get("dmtsimp").xsection = xsec # combined xsec
    extrapolated_lumi = "default"; analysis = ana
    outfile = os.path.join(combined_path, 'CLs_output.dat')

    run_recast = RunRecast(main, "F3S_XX/{}".format(ana))
    if ana in PAD4SFS:
        run_recast.pad = os.path.join(ma5dir, "tools/PADForSFS")
    else:
        run_recast.pad = os.path.join(ma5dir, "tools/PAD")

    run_recast.logger.setLevel(logging.DEBUG)

    ET = run_recast.check_xml_scipy_methods()

    lumi, regions, regiondata = run_recast.parse_info_file(ET,analysis,extrapolated_lumi)

    # Reset signal region yields for combined sample
    for reg in regions:
        regiondata[reg]["Nf"] = XX_collection[reg].final_cut.eff * rescale_xsec_XX[coupling] + \
                                XY_collection[reg].final_cut.eff * rescale_xsec_XY[coupling] + \
                                YYQCD_collection[reg].final_cut.eff * rescale_xsec_YYQCD[coupling] + \
                                YYi_collection[reg].final_cut.eff * rescale_xsec_YYi[coupling] + \
                                YYtPP_collection[reg].final_cut.eff * rescale_xsec_YYtPP[coupling] + \
                                YYtPM_collection[reg].final_cut.eff * rescale_xsec_YYtPM[coupling] + \
                                YYtMM_collection[reg].final_cut.eff * rescale_xsec_YYtMM[coupling] 
        regiondata[reg]["N0"] = xsec
    #regiondata[reg]["nb"]=extrapolated_lumi/luminosity*regiondata[reg]["nb"]
    # Calculate exclusion limits
    regiondata = run_recast.extract_sig_cls(regiondata, regions, lumi,"exp")
    regiondata = run_recast.extract_sig_lhcls(regiondata, lumi, "exp")
    regiondata = run_recast.extract_sig_cls(regiondata, regions, lumi, "obs")
    regiondata = run_recast.extract_sig_lhcls(regiondata, lumi, "obs")
    regiondata = run_recast.extract_cls(regiondata, regions, xsec, lumi)

    # write the output file
    with open(outfile,'a+') as mysummary:
        run_recast.write_cls_header(xsec, mysummary)
        run_recast.write_cls_output(analysis, regions, regiondata, {}, mysummary, False, lumi)
        mysummary.write('\n')

    # fill "done.txt"
    name="MY"+str(mY)+"_MX"+str(mX)+"_coup"+str(coupling)+"_xsec="+str(xsec)
    with open(os.path.join(combined_path, "done"), "a+") as d:
        d.write(f"{name}\n")
