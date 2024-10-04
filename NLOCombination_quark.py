import argparse
import json
import logging
import sys
import ma5_expert as ma5
import pandas as pd
import shutil
import os
import math
import warnings

# Suppress the specific RuntimeWarning related to tarfile extraction
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*tarfile extraction.*")

currentfolder = os.getcwd()

# Test command to run
# python NLOCombination_quark.py --MY 1300 --MX 900 --coup 5 --order NLO --model S3M

def extract_tar(tar_gz_file, extract_path):
    #print(os.path.join(extract_path,tar_gz_file))
    if os.path.exists(os.path.join(extract_path,tar_gz_file)):
        return 0
    tar_gz_file=tar_gz_file+".tar.gz"
    try:
        shutil.unpack_archive(tar_gz_file, extract_path, 'gztar')
        #print(f"Successfully extracted '{tar_gz_file}' to '{extract_path}'.")
    except Exception as e:
        pass
        #print(f"Error extracting '{tar_gz_file}': {e}")


parser = argparse.ArgumentParser(prog = 'NLOCombination',description = '')
parser.add_argument("--MY", type=int,help='mass of DM mediator')
parser.add_argument("--MX", type=int,help='mass of DM particle')
parser.add_argument("--coup", type=float,help='Coupling')
#parser.add_argument("--quark", type=str,help='Quark')
parser.add_argument("--order", type=str,help='order')
parser.add_argument("--model", type=str,help='Model')
parser.add_argument("--input", type=str,help='Input file path and Name',default="/eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results")
parser.add_argument("--output", type=str,help='Output file path and Name',default=f"/eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/Reinterpretations/")
parser.add_argument("--ma5dir", type=str,help='Input file path and Name',default=f"{currentfolder}/madanalysis5")
parser.add_argument("--process", type=str,help='process: XX, XY, YYQCD, YYt, YYsum, or Full',default="Full")
parser.add_argument("--wmratio", type=str,help='y/n for fixed wy/my ratio',default="y")
args = parser.parse_args()

# define point

quarks = ['b']

mY = args.MY
mX = args.MX
order = args.order
coupling = args.coup
model = args.model
proc_study = args.process


coupling_power = {'XX' : 4, 'XY':2, 'YYi':2, 'YYQCD': 0, 'YYtPP': 4, 'YYtPM': 4, 'YYtMM': 4}
processes_full = ['XX','XY','YYi','YYQCD','YYtPP','YYtPM','YYtMM']
PAD4SFS = ["atlas_exot_2018_06"]
analysis_names = ["atlas_conf_2019_040"]#,"atlas_exot_2018_06", "cms_sus_19_006", "cms_exo_20_004", "atlas_susy_2018_17"]

# need to add quark information here


rescale_xsec_XX = [0]*len(quarks)
rescale_xsec_XY = [0]*len(quarks)
rescale_xsec_YYi = [0]*len(quarks)
rescale_xsec_YYQCD = [0]*len(quarks)
rescale_xsec_YYtPP = [0]*len(quarks)
rescale_xsec_YYtPM = [0]*len(quarks)
rescale_xsec_YYtMM = [0]*len(quarks)

folderName = [0]*len(quarks)

# Output folder
qstring=""
for i in range(len(quarks)):
    qstring += quarks[i]

#if proc_study == "Full":
combined_path = args.output +  model + "_" + proc_study + "_" + order + "_SM"+ str(qstring) + "_MY" + str(mY) + "_MX" + str(mX) + "_coup" + str(coupling) + "_recast"
#else:
#    combined_path = args.output + name_recast_file 

if not os.path.isdir(combined_path):
    os.system("mkdir -p " + combined_path)




print("Summary of inputs")
print("mY mX order coupling quark model")

for iquark, quark in enumerate(quarks):

    inputfolder = os.path.join(args.input, quark) 
    folderName[iquark] = os.path.join(inputfolder, "Results_{}_recast".format(model))
    fileName = "Sigmas/{}_sigmas.dat".format(model)

    print(mY, mX, order, coupling, quark, model)

    inputfile = os.path.join(folderName[iquark],fileName)

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


    select_row = df[(df["my(GeV)"] == mY) & (df["mx(GeV)"] == mX) ]
    select_row_order  = df[(df["my(GeV)"] == mY) & (df["mx(GeV)"] == mX)  & (df["order"] == order)]
    select_row_YYi  = df[(df["my(GeV)"] == mY) & (df["mx(GeV)"] == mX) & (df["process"] == 'YYi') & (df["order"] == 'LO')]

    # calculate k factor
    filtered_YYQCD_LO = select_row[(select_row["process"] == 'YYQCD') & (select_row['order'] == 'LO')]
    xsec_YYQCD_LO = filtered_YYQCD_LO['CShat(pb)'].values[0] if not filtered_YYQCD_LO.empty else 0

    filtered_YYtPM_LO = select_row[(select_row["process"] == 'YYtPM') & (select_row['order'] == 'LO')]
    xsec_YYtPM_LO = filtered_YYtPM_LO['CShat(pb)'].values[0] if not filtered_YYtPM_LO.empty else 0

    if order == "NLO":
        filtered_rows = select_row[(select_row["process"] == 'YYQCD') & (select_row['order'] == 'NLO')]
        xsec_YYQCD_NLO = filtered_rows['CShat(pb)'].values[0] if not filtered_rows.empty else 0
        
        filtered_rows = select_row[(select_row["process"] == 'YYtPM') & (select_row['order'] == 'NLO')]
        xsec_YYtPM_NLO = filtered_rows['CShat(pb)'].values[0] if not filtered_rows.empty else 0


    if order == "NLO":
        Kfactor_YYi=1
        if xsec_YYQCD_LO == 0 and xsec_YYtPM_LO == 0:
            print("Both YYQCD at LO and YYtPM at LO are missing, Kfactor set to 1")
        elif xsec_YYQCD_LO == 0:
            print("Missing YYQCD at LO, Kfactor set to 1")
        elif xsec_YYtPM_LO == 0:
            print("Missing YYtPM at LO, Kfactor set to 1")
        else:
            Kfactor_YYi = math.sqrt((xsec_YYQCD_NLO*xsec_YYtPM_NLO)/(xsec_YYQCD_LO*xsec_YYtPM_LO))

    if select_row_order.empty:
        print("no point found")
        sys.exit()

    if order == "LO":
        rescale_xsec_YYi[iquark] = (select_row_YYi['CShat(pb)'].values[0] * coupling ** coupling_power['YYi']) if not select_row_YYi.empty else 0
    elif order == "NLO":
        rescale_xsec_YYi[iquark] = (select_row_YYi['CShat(pb)'].values[0] * coupling ** coupling_power['YYi']*Kfactor_YYi) if not select_row_YYi.empty else 0


    for process in processes_full:
        filtered_rows = select_row_order[select_row_order["process"] == process]
        if not filtered_rows.empty:
            rescale_xsec = filtered_rows['CShat(pb)'].values[0] * coupling ** coupling_power[process]
        else:
            rescale_xsec = 0
    
        # Assign to the corresponding rescale_xsec variable
        if process == 'XX':
            rescale_xsec_XX[iquark] = rescale_xsec
        elif process == 'XY':
            rescale_xsec_XY[iquark] = rescale_xsec
        elif process == 'YYQCD':
            rescale_xsec_YYQCD[iquark] = rescale_xsec
        elif process == 'YYtPP':
            rescale_xsec_YYtPP[iquark] = rescale_xsec
        elif process == 'YYtPM':
            rescale_xsec_YYtPM[iquark] = rescale_xsec
        elif process == 'YYtMM':
            rescale_xsec_YYtMM[iquark] = rescale_xsec



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


# Samples to be combined. Each set of samples are generated and stored in separate directories

def replace_hyphens(data):
    if isinstance(data, dict):
        return {k.replace("-", "_"): replace_hyphens(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_hyphens(item) for item in data]
    else:
        return data

#for iquark,quark in enumerate(quarks):
#    for proc in processes_full:
#
#        if proc == "YYi":
#            order_file = "LO"
#        else:
#            order_file = order
#
#        name_recast_file = model + "_" + proc + "_" + order_file + "_SM"+ quark + "_MY" + str(mY) + "_MX" + str(mX)  + "_recast"
#
#        file = os.path.join(folderName[iquark], "MA5_Recast", name_recast_file)
#        extract_tar(file, os.path.join("/tmp/MA5_Recast"))
#        file = file + ".tar.gz"
#
#        # File name for missing points
#        missingpointsfile = os.path.join(combined_path, 'missingpoints.dat')
#
#        # Build the parameter line
#        parameter_line = f"{mY:<5} {mX:<5} {model:<4} {quark:<3} {proc:<6} {order_file:<4}\n"
#
#        # Check if the parameters are already present in missingpoints.dat
#        if os.path.exists(missingpointsfile):
#            with open(missingpointsfile, 'r') as missingpoints_file:
#                lines = missingpoints_file.readlines()
#                if parameter_line in lines:
#                    if not os.path.exists(file):
#                        # If the tarball is missing, skip to the next point in the loop
#                        print(f"Skipping point {parameter_line.strip()} because the tarball is missing.")
#                        continue  # Skip this iteration
#
#        # If the tarball exists, print the details
#        if os.path.exists(file):
#            print(f"{mY:<5} {mX:<5} {model:<4} {quark:<3} {proc:<6} {order_file:<4}          ", end='\r')
#        else:
#            # If not, log the missing point in missingpoints.dat
#            with open(missingpointsfile, 'a') as missingpoints_file:
#                missingpoints_file.write(parameter_line)












# Flag to track whether there are any points to process
points_processed = False

for iquark, quark in enumerate(quarks):
    for proc in processes_full:

        if proc == "YYi":
            order_file = "LO"
        else:
            order_file = order

        name_recast_file = model + "_" + proc + "_" + order_file + "_SM" + quark + "_MY" + str(mY) + "_MX" + str(mX) + "_recast"

        file = os.path.join(folderName[iquark], "MA5_Recast", name_recast_file)
        extract_tar(file, os.path.join("/tmp/MA5_Recast"))
        file = file + ".tar.gz"

        # File name for missing points
        missingpointsfile = os.path.join(combined_path, 'missingpoints.dat')

        # Build the parameter line
        parameter_line = f"{mY:<5} {mX:<5} {model:<4} {quark:<3} {proc:<6} {order_file:<4}\n"

        # Check if the parameters are already present in missingpoints.dat
        if os.path.exists(missingpointsfile):
            with open(missingpointsfile, 'r') as missingpoints_file:
                lines = missingpoints_file.readlines()
                if parameter_line in lines:
                    if not os.path.exists(file):
                        # If the tarball is missing, skip to the next point in the loop
                        print(f"Skipping point {parameter_line.strip()} because the tarball is missing.")
                        continue  # Skip this iteration

        # If the tarball exists, print the details
        if os.path.exists(file):
            print(f"{mY:<5} {mX:<5} {model:<4} {quark:<3} {proc:<6} {order_file:<4}          ", end='\r')
            points_processed = True  # Set flag to True since we processed a point
        else:
            # If not, log the missing point in missingpoints.dat
            with open(missingpointsfile, 'a') as missingpoints_file:
                missingpoints_file.write(parameter_line)
            points_processed = True  # Set flag to True since we processed a point

# If no points were processed, print a message and exit
if not points_processed:
    print("No new points to process.")
    sys.exit()




outfile = os.path.join(combined_path, 'CLs_output.dat')
with open(outfile, 'w') as mysummary:
    pass  # This clears the file by opening it in 'w' mode



for ana in analysis_names:
    xsec_proc = 0

    XX_path = [0]*len(quarks)
    XY_path = [0]*len(quarks)
    YYi_path = [0]*len(quarks)
    YYQCD_path = [0]*len(quarks)
    YYtPP_path = [0]*len(quarks)
    YYtPM_path = [0]*len(quarks)
    YYtMM_path = [0]*len(quarks)

    XX_collection = [0]*len(quarks)
    XY_collection = [0]*len(quarks)
    YYi_collection = [0]*len(quarks)
    YYQCD_collection = [0]*len(quarks)
    YYtPP_collection = [0]*len(quarks)
    YYtPM_collection = [0]*len(quarks)
    YYtMM_collection = [0]*len(quarks)

    for iquark, quark in enumerate(quarks):

        XX_path[iquark]  = os.path.join("/tmp/MA5_Recast/{}_XX_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))
        XY_path[iquark]  = os.path.join("/tmp/MA5_Recast/{}_XY_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))
        YYi_path[iquark]  = os.path.join("/tmp/MA5_Recast/{}_YYi_LO_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, quark, mY, mX, ana))
        YYQCD_path[iquark]  = os.path.join("/tmp/MA5_Recast/{}_YYQCD_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))
        YYtPP_path[iquark]  = os.path.join("/tmp/MA5_Recast/{}_YYtPP_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))
        YYtPM_path[iquark]  = os.path.join("/tmp/MA5_Recast/{}_YYtPM_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))
        YYtMM_path[iquark]  = os.path.join("/tmp/MA5_Recast/{}_YYtMM_{}_SM{}_MY{}_MX{}_recast/Output/SAF/dmtsimp/{}/Cutflows".format(model, order, quark, mY, mX, ana))

        if proc_study == "XX":
            xsec_proc  += rescale_xsec_XX[iquark]

        if proc_study == "XY":
            xsec_proc  += rescale_xsec_XY[iquark]

        if proc_study == "YYQCD":
            xsec_proc  += rescale_xsec_YYQCD[iquark]

        if proc_study == "YYt":
            xsec_proc  += rescale_xsec_YYtMM[iquark] + rescale_xsec_YYtPM[iquark] + rescale_xsec_YYtPP[iquark]

        if proc_study == "YYSum":
            xsec_proc  += rescale_xsec_YYi[iquark] + rescale_xsec_YYQCD[iquark] + rescale_xsec_YYtPP[iquark] + rescale_xsec_YYtPM[iquark] + rescale_xsec_YYtMM[iquark]

        if proc_study == "Full":
            xsec_proc  += rescale_xsec_XX[iquark] + rescale_xsec_XY[iquark] + rescale_xsec_YYi[iquark] + rescale_xsec_YYQCD[iquark] + rescale_xsec_YYtPP[iquark] + rescale_xsec_YYtPM[iquark] + rescale_xsec_YYtMM[iquark]
    
        XX_collection[iquark]    = ma5.cutflow.Collection(XX_path[iquark],    xsection=rescale_xsec_XX[iquark],    lumi=1) if os.path.exists(XX_path[iquark]) else []
        XY_collection[iquark]    = ma5.cutflow.Collection(XY_path[iquark],    xsection=rescale_xsec_XY[iquark],    lumi=1) if os.path.exists(XY_path[iquark]) else []
        YYi_collection[iquark]   = ma5.cutflow.Collection(YYi_path[iquark],   xsection=rescale_xsec_YYi[iquark],   lumi=1) if os.path.exists(YYi_path[iquark]) else []
        YYQCD_collection[iquark] = ma5.cutflow.Collection(YYQCD_path[iquark], xsection=rescale_xsec_YYQCD[iquark], lumi=1) if os.path.exists(YYQCD_path[iquark]) else []
        YYtPP_collection[iquark] = ma5.cutflow.Collection(YYtPP_path[iquark], xsection=rescale_xsec_YYtPP[iquark], lumi=1) if os.path.exists(YYtPP_path[iquark]) else []
        YYtPM_collection[iquark] = ma5.cutflow.Collection(YYtPM_path[iquark], xsection=rescale_xsec_YYtPM[iquark], lumi=1) if os.path.exists(YYtPM_path[iquark]) else []
        YYtMM_collection[iquark] = ma5.cutflow.Collection(YYtMM_path[iquark], xsection=rescale_xsec_YYtMM[iquark], lumi=1) if os.path.exists(YYtMM_path[iquark]) else []



    xsec = xsec_proc

    with open(os.path.join(combined_path,'sample_info_proc.json'),'w') as info_file:
        info = {"xsec" : float(xsec)}
        json.dump(info, info_file, indent = 4)


    # Run Recast
    main.datasets.Add("dmtsimp")
    main.datasets.Get("dmtsimp").xsection = xsec # combined xsec
    extrapolated_lumi = "default"; analysis = ana
    #outfile = os.path.join(combined_path, 'CLs_output.dat')

    run_recast = RunRecast(main, "{}_XX/{}".format(model, ana))
    if ana in PAD4SFS:
        run_recast.pad = os.path.join(ma5dir, "tools/PADForSFS")
    else:
        run_recast.pad = os.path.join(ma5dir, "tools/PAD")

    run_recast.logger.setLevel(logging.DEBUG)

    ET = run_recast.check_xml_scipy_methods()


    lumi, regions, regiondata = run_recast.parse_info_file(ET,analysis,extrapolated_lumi)
    
    # Replace hyphens with underscores in regions and regiondata
    regions = [region.replace("-", "_") for region in regions]
    regiondata = replace_hyphens(regiondata)

    print(regions, regiondata)
    for reg in regions:
        # Reset signal region yields for combined sample if this is the first iteration
        regiondata[reg]["Nf"] = 0
        regiondata[reg]["N0"] = 0

        for iquark, quark in enumerate(quarks):

            if proc_study == "XX":
                regiondata[reg]["Nf"] += XX_collection[iquark][reg].final_cut.eff * rescale_xsec_XX[iquark]

            if proc_study == "XY":
                regiondata[reg]["Nf"] += XY_collection[iquark][reg].final_cut.eff * rescale_xsec_XY[iquark]

            if proc_study == "YYQCD":
                regiondata[reg]["Nf"] += YYQCD_collection[iquark][reg].final_cut.eff * rescale_xsec_YYQCD[iquark]

            if proc_study == "YYt":
                regiondata[reg]["Nf"] += YYtPP_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtPP[iquark] + \
                                        YYtPM_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtPM[iquark] + \
                                        YYtMM_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtMM[iquark] 

            if proc_study == "YYSum":
                regiondata[reg]["Nf"] += YYi_collection[iquark][reg].final_cut.eff * rescale_xsec_YYi[iquark] + \
                                        YYQCD_collection[iquark][reg].final_cut.eff * rescale_xsec_YYQCD[iquark] + \
                                        YYtPP_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtPP[iquark] + \
                                        YYtPM_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtPM[iquark] + \
                                        YYtMM_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtMM[iquark] 

            if proc_study == "Full":

                # Check each collection before accessing
                if XX_collection[iquark]:  # Check if the collection is not empty
                    regiondata[reg]["Nf"] += XX_collection[iquark][reg].final_cut.eff * rescale_xsec_XX[iquark]

                if XY_collection[iquark]:  # Check if the collection is not empty
                    regiondata[reg]["Nf"] += XY_collection[iquark][reg].final_cut.eff * rescale_xsec_XY[iquark]

                if YYQCD_collection[iquark]:  # Check if the collection is not empty
                    regiondata[reg]["Nf"] += YYQCD_collection[iquark][reg].final_cut.eff * rescale_xsec_YYQCD[iquark]

                if YYi_collection[iquark]:  # Check if the collection is not empty
                    regiondata[reg]["Nf"] += YYi_collection[iquark][reg].final_cut.eff * rescale_xsec_YYi[iquark]

                if YYtPP_collection[iquark]:  # Check if the collection is not empty
                    regiondata[reg]["Nf"] += YYtPP_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtPP[iquark]

                if YYtPM_collection[iquark]:  # Check if the collection is not empty
                    regiondata[reg]["Nf"] += YYtPM_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtPM[iquark]

                if YYtMM_collection[iquark]:  # Check if the collection is not empty
                    regiondata[reg]["Nf"] += YYtMM_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtMM[iquark]


                #regiondata[reg]["Nf"] += XX_collection[iquark][reg].final_cut.eff * rescale_xsec_XX[iquark] + \
                #                        XY_collection[iquark][reg].final_cut.eff * rescale_xsec_XY[iquark] + \
                #                        YYQCD_collection[iquark][reg].final_cut.eff * rescale_xsec_YYQCD[iquark] + \
                #                        YYi_collection[iquark][reg].final_cut.eff * rescale_xsec_YYi[iquark] + \
                #                        YYtPP_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtPP[iquark] + \
                #                        YYtPM_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtPM[iquark] + \
                #                        YYtMM_collection[iquark][reg].final_cut.eff * rescale_xsec_YYtMM[iquark] 
            
            regiondata[reg]["N0"] += xsec
        
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

#    if not os.path.exists(os.path.join(combined_path, 'missingpoints.dat')):
#        with open(os.path.join(combined_path, "done"), "a+") as d:
#            d.write(f"{name}\n")

missingpoints_path = os.path.join(combined_path, 'missingpoints.dat')

# Check if missingpoints.dat exists and is empty
if os.path.exists(missingpoints_path):
    # If the file is empty, delete it
    if os.stat(missingpoints_path).st_size == 0:
        os.remove(missingpoints_path)
        print("missingpoints.dat was empty and has been deleted.")

# If missingpoints.dat does not exist, proceed to write to "done" file
if not os.path.exists(missingpoints_path):
    with open(os.path.join(combined_path, "done"), "a+") as d:
        d.write(f"{name}\n")  # Keeps the line as it was before
