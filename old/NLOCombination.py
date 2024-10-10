import argparse
import json
import logging
import sys
import ma5_expert as ma5
import pandas as pd
import shutil
import os
import math

# Test command to run
# python NLOCombination.py --MY 1300 --MX 900 --coup 5 --quark d --order NLO --model F3S 

def extract_tar(tar_gz_file, extract_path):
    print(os.path.join(extract_path,tar_gz_file))
    if os.path.exists(os.path.join(extract_path,tar_gz_file)):
        return 0
    tar_gz_file=tar_gz_file+".tar.gz"
    try:
        shutil.unpack_archive(tar_gz_file, extract_path, 'gztar')
        print(f"Successfully extracted '{tar_gz_file}' to '{extract_path}'.")
    except Exception as e:
        print(f"Error extracting '{tar_gz_file}': {e}")


parser = argparse.ArgumentParser(prog = 'NLOCombination',description = '')
parser.add_argument("--MY", type=int,help='mass of DM mediator')
parser.add_argument("--MX", type=int,help='mass of DM particle')
parser.add_argument("--coup", type=float,help='Coupling')
parser.add_argument("--quark", type=str,help='Quark')
parser.add_argument("--order", type=str,help='order')
parser.add_argument("--model", type=str,help='Model')
parser.add_argument("--input", type=str,help='Input file path and Name',default="/eos/user/a/aman/dsb_lowstat/")
parser.add_argument("--output", type=str,help='Output file path and Name',default="/eos/user/a/aman/LHCDM_tchan_Combination/output/")
parser.add_argument("--ma5dir", type=str,help='Input file path and Name',default="/eos/user/a/aman/LHCDM_tchan_Combination/madanalysis5")
parser.add_argument("--process", type=str,help='process: XX, XY, YYQCD, YYt, YYsum, or Full',default="Full")
parser.add_argument("--wmratio", type=str,help='y/n for fixed wy/my ratio',default="y")
args = parser.parse_args()

# define point

mY = args.MY
mX = args.MX
order = args.order
coupling = args.coup
quark = args.quark
model = args.model
proc_study = args.process

inputfolder = args.input 
folderName = os.path.join(inputfolder, "Results_{}_recast".format(model))
fileName = "Sigmas/{}_sigmas.dat".format(model)

print("Summary of inputs")
print("mY mX order coupling quark model")
print(mY, mX, order, coupling, quark, model)

coupling_power = {'XX' : 4, 'XY':2, 'YYi':2, 'YYQCD': 0, 'YYtPP': 4, 'YYtPM': 4, 'YYtMM': 4}
processes_full = ['XX','XY','YYi','YYQCD','YYtPP','YYtPM','YYtMM']
PAD4SFS = ["atlas_exot_2018_06"]
analysis_names = ["atlas_conf_2019_040","atlas_exot_2018_06", "cms_sus_19_006", "cms_exo_20_004", "atlas_susy_2018_17"]
luminosity=137

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

if args.wmratio == "y":
    num_columns = 15  
    columns_data=['my(GeV)', 'mx(GeV)', 'quark', 'wy/my', 'coupling', 'process', 'order', 'lhapdfID', 'CS(pb)', 
                                        'stat(%)', 'scale+(%)', 'scale-(%)', 'PDF+(%)', 'PDF-(%)', 'CShat(pb)']
elif args.wmratio == "n":
    num_columns = 14
    columns_data=['my(GeV)', 'mx(GeV)', 'coupling', 'quark', 'process', 'order', 'lhapdfID', 'CS(pb)', 
                                        'stat(%)', 'scale+(%)', 'scale-(%)', 'PDF+(%)', 'PDF-(%)', 'CShat(pb)']
        


num_rows = len(data) // num_columns  # Calculate the number of rows
data_rows = [data[i:i+num_columns] for i in range(0, len(data), num_columns)]


# Convert the 2D list into a Pandas DataFrame
df = pd.DataFrame(data_rows, columns=columns_data)

df = df.drop(df.index[0])

float_cols = ['my(GeV)', 'mx(GeV)', 'coupling','CS(pb)','stat(%)', 'scale+(%)', 'scale-(%)', 'PDF+(%)', 'PDF-(%)', 'CShat(pb)']

for col in float_cols:
    df[col] = df[col].astype(float)


rescale_xsec_XX = 0
rescale_xsec_XY = 0
rescale_xsec_YYi = 0
rescale_xsec_YYQCD = 0
rescale_xsec_YYtPP = 0
rescale_xsec_YYtPM = 0
rescale_xsec_YYtMM = 0

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

# madanalysis expert mode 

ma5dir = args.ma5dir 
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

ma5.BackendManager.set_madanalysis_backend(args.ma5dir)

main_path = folderName

# Samples to be combined. Each set of samples are generated and stored in separate directories

for proc in processes_full:

    if proc == "YYi":
        order_file = "LO"
    else:
        order_file = order

    name_recast_file = model + "_" + proc + "_" + order_file + "_SM"+ quark + "_MY" + str(mY) + "_MX" + str(mX)  + "_recast"

    file = os.path.join(folderName, "MA5_Recast",name_recast_file)
    extract_tar(file, os.path.join("/tmp/MA5_Recast"))
    file = file+ ".tar.gz"
    print(file)

    if os.path.exists(file):
        print("File found")
    else:
        print("file not found exiting code")
        sys.exit()

# Output folder

#if proc_study == "Full":
combined_path = args.output +  model + "_" + proc_study + "_" + order_file + "_SM"+ quark+ "_MY" + str(mY) + "_MX" + str(mX) + "_coup" + str(coupling) + "_recast" 
#else:
#    combined_path = args.output + name_recast_file 

if not os.path.isdir(combined_path):
    os.system("mkdir -p " + combined_path)


#for coupling in couplings:
for ana in analysis_names:
    XX_path  = os.path.join("/tmp/MA5_Recast/{}_XX_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))
    XY_path  = os.path.join("/tmp/MA5_Recast/{}_XY_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))
    YYi_path  = os.path.join("/tmp/MA5_Recast/{}_YYi_LO_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, quark, mY, mX, ana))
    YYQCD_path  = os.path.join("/tmp/MA5_Recast/{}_YYQCD_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))
    YYtPP_path  = os.path.join("/tmp/MA5_Recast/{}_YYtPP_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))
    YYtPM_path  = os.path.join("/tmp/MA5_Recast/{}_YYtPM_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))
    YYtMM_path  = os.path.join("/tmp/MA5_Recast/{}_YYtMM_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))

    if proc_study == "XX":
        xsec_proc  = rescale_xsec_XX

    if proc_study == "XY":
        xsec_proc  = rescale_xsec_XY

    if proc_study == "YYQCD":
        xsec_proc  = rescale_xsec_YYQCD

    if proc_study == "YYt":
        xsec_proc  = rescale_xsec_YYtMM + rescale_xsec_YYtPM + rescale_xsec_YYtPP

    if proc_study == "YYSum":
        xsec_proc  = rescale_xsec_YYi + rescale_xsec_YYQCD + rescale_xsec_YYtPP + rescale_xsec_YYtPM + rescale_xsec_YYtMM

    if proc_study == "Full":
        xsec_proc  = rescale_xsec_XX + rescale_xsec_XY + rescale_xsec_YYi + rescale_xsec_YYQCD + rescale_xsec_YYtPP + rescale_xsec_YYtPM + rescale_xsec_YYtMM
    
    xsec = xsec_proc

    XX_collection  = ma5.cutflow.Collection(XX_path,  xsection = rescale_xsec_XX,  lumi = luminosity,)
    XY_collection  = ma5.cutflow.Collection(XY_path,  xsection = rescale_xsec_XY,  lumi = luminosity,)
    YYi_collection  = ma5.cutflow.Collection(YYi_path,  xsection = rescale_xsec_YYi,  lumi = luminosity,)
    YYQCD_collection = ma5.cutflow.Collection(YYQCD_path, xsection = rescale_xsec_YYQCD, lumi = luminosity,)
    YYtPP_collection = ma5.cutflow.Collection(YYtPP_path, xsection = rescale_xsec_YYtPP, lumi = luminosity,)
    YYtPM_collection = ma5.cutflow.Collection(YYtPM_path, xsection = rescale_xsec_YYtPM, lumi = luminosity,)
    YYtMM_collection = ma5.cutflow.Collection(YYtMM_path, xsection = rescale_xsec_YYtMM, lumi = luminosity,)

    with open(os.path.join(combined_path,'sample_info_proc.json'),'w') as info_file:
        info = {"xsec" : float(xsec)}
        json.dump(info, info_file, indent = 4)

    # Run Recast
    main.datasets.Add("dmtsimp")
    main.datasets.Get("dmtsimp").xsection = xsec # combined xsec
    extrapolated_lumi = "default"; analysis = ana
    outfile = os.path.join(combined_path, 'CLs_output.dat')

    run_recast = RunRecast(main, "{}_XX/{}".format(model, ana))
    if ana in PAD4SFS:
        run_recast.pad = os.path.join(ma5dir, "tools/PADForSFS")
    else:
        run_recast.pad = os.path.join(ma5dir, "tools/PAD")

    run_recast.logger.setLevel(logging.DEBUG)

    ET = run_recast.check_xml_scipy_methods()

    lumi, regions, regiondata = run_recast.parse_info_file(ET,analysis,extrapolated_lumi)

    # Reset signal region yields for combined sample
    for reg in regions:

        if proc_study == "XX":
            regiondata[reg]["Nf"] = XX_collection[reg].final_cut.eff * rescale_xsec_XX 

        if proc_study == "XY":
            regiondata[reg]["Nf"] = XY_collection[reg].final_cut.eff * rescale_xsec_XY

        if proc_study == "YYQCD":
            regiondata[reg]["Nf"] = YYQCD_collection[reg].final_cut.eff * rescale_xsec_YYQCD

        if proc_study == "YYt":
            regiondata[reg]["Nf"] = YYtPP_collection[reg].final_cut.eff * rescale_xsec_YYtPP + \
                                    YYtPM_collection[reg].final_cut.eff * rescale_xsec_YYtPM + \
                                    YYtMM_collection[reg].final_cut.eff * rescale_xsec_YYtMM 

        if proc_study == "YYSum":
            regiondata[reg]["Nf"] = YYi_collection[reg].final_cut.eff * rescale_xsec_YYi + \
                                    YYQCD_collection[reg].final_cut.eff * rescale_xsec_YYQCD + \
                                    YYtPP_collection[reg].final_cut.eff * rescale_xsec_YYtPP + \
                                    YYtPM_collection[reg].final_cut.eff * rescale_xsec_YYtPM + \
                                    YYtMM_collection[reg].final_cut.eff * rescale_xsec_YYtMM 

        if proc_study == "Full":
            regiondata[reg]["Nf"] = XX_collection[reg].final_cut.eff * rescale_xsec_XX + \
                                    XY_collection[reg].final_cut.eff * rescale_xsec_XY + \
                                    YYQCD_collection[reg].final_cut.eff * rescale_xsec_YYQCD + \
                                    YYi_collection[reg].final_cut.eff * rescale_xsec_YYi + \
                                    YYtPP_collection[reg].final_cut.eff * rescale_xsec_YYtPP + \
                                    YYtPM_collection[reg].final_cut.eff * rescale_xsec_YYtPM + \
                                    YYtMM_collection[reg].final_cut.eff * rescale_xsec_YYtMM 
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
