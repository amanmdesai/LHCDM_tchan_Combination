import argparse
import json
import logging
import os
import sys
import ma5_expert as ma5
import pandas as pd
import tarfile
import gzip


# define point
mY = 2800
mX = 1200
proc = 'XX'
order = 'NLO'
couplings = [3.5,5.0]
coupling_power = {'XX' : 4, 'XY':2, 'YYi':2, 'YYQCD': 0, 'YYtPP': 4, 'YYtPM': 4, 'YYtMM': 4}

quark = 'u'
model = 'S3M'

folderName = "installed_files/Sigmas"
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

rescale_xsec = {}

for coup in couplings:
    rescale_xsec[coup]=select_XXrow['CShat(pb)'].values[0]*coup**coupling_power[proc]

print(rescale_xsec)

name_recast_file = model + "_" + proc + "_" + order + "_SMu_" + "MY" + str(mY) + "_MX" + str(mX) + "_recast"

file = os.path.join(folderName, "MA5_Recast",name_recast_file+".tar.gz")

if os.path.exists(file):
    print("File found")
else:
    print("file not found exiting code")
    sys.exit()

# madanalysis expert mode 


"""
parser = argparse.ArgumentParser(description="Setup scanner")

pathgroup = parser.add_argument_group("Path handling")

pathgroup.add_argument("--ma5-dir",dest="MA5DIR", type=str, help="Set madanalysis 5 directory",
                        default = "/scratch/lp1c12/DMtsimp_project/NLOcombination/core/MA5expertSED_MA5HS/madanalysis5")

args = parser.parse_args()
"""

ma5dir = "/home/amdesai/Music/LHCDM_tchan_Combination/installed_files/MA5expert/madanalysis5"#ma5dir
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

ma5.BackendManager.set_madanalysis_backend("/home/amdesai/Music/LHCDM_tchan_Combination/installed_files/MA5expert/madanalysis5")

main_path = "/home/amdesai/Music/LHCDM_tchan_Combination/installed_files/Sigmas"

# Output folder
combined_path = "/home/amdesai/Music/LHCDM_tchan_Combination/output"
if not os.path.isdir(combined_path):
    os.mkdir(combined_path)

# Samples to be combined. Each set of samples are generated and stored in separate directories
XX_path  = os.path.join(main_path, "MA5_Recast/S3M_XX_NLO_SMu_MY2800_MX1200_recast/Output/SAF/dmtsimp/cms_sus_19_006/Cutflows")

xsec_XX  = rescale_xsec[5]

luminosity=137
"""
with tarfile.open(XX_path+".tar.gz", 'r:gz') as tar:
    # List the contents of the tar file
    file_names = tar.getnames()
    print(file_names)
    
    #file_content = tar.extractfile(XX_path)#+"/Output/SAF/dmtsimp/cms_sus_19_006/Cutflows/")

    # Loop through each file in the tar file
    for file_name in file_names:
        # Extract the file content
        file_content = tar.extractfile(file_name)
        
        # Read the content of the file
        content = file_content.read()
        
        # Do something with the content (print it, process it, etc.)
        print(content)
"""

XX_collection  = ma5.cutflow.Collection(XX_path,  xsection = xsec_XX,  lumi = luminosity,)

xsec = xsec_XX

if not os.path.isdir(combined_path):
    os.mkdir(combined_path)

with open(os.path.join(combined_path,'sample_info_XX.json'),'w') as info_file:
    info = {"xsec" : float(xsec)}
    json.dump(info, info_file, indent = 4)

# Run Recast
main.datasets.Add("dmtsimp")
main.datasets.Get("dmtsimp").xsection = xsec # combined xsec
extrapolated_lumi = "default"; analysis = "cms_sus_19_006"
outfile = os.path.join(combined_path, 'CLs_output.dat')

run_recast = RunRecast(main, "S3M_XX/cms_sus_19_006")
run_recast.pad = os.path.join(ma5dir, "tools/PAD")
run_recast.logger.setLevel(logging.DEBUG)

ET = run_recast.check_xml_scipy_methods()

lumi, regions, regiondata = run_recast.parse_info_file(ET,analysis,extrapolated_lumi)

# Reset signal region yields for combined sample
for reg in regions:
    regiondata[reg]["Nf"] = XX_collection[reg].final_cut.eff * xsec_XX  
    regiondata[reg]["N0"] = xsec
    
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
name="SED_NAMERUN xsec="+str(xsec)
with open(os.path.join(combined_path, "done"), "a+") as d:
    d.write(f"{name}\n")
