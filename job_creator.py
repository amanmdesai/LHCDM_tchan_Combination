import os
import json
import argparse
import pandas as pd


parser = argparse.ArgumentParser(prog = 'DMSimpt_Combination',description = '')
parser.add_argument("--input", type=str,help='Input Data file path and Name',default="/eos/user/a/aman/dsb_lowstat/")
parser.add_argument("--programpath", type=str,help='path to NLOCombination.py',default="/eos/user/a/aman/LHCDM_tchan_Combination/")
parser.add_argument("--output", type=str,help='Output file path and Name',default="/eos/user/a/aman/LHCDM_tchan_Combination/output/")
parser.add_argument("--ma5dir", type=str,help='Input file path and Name',default="/eos/user/a/aman/LHCDM_tchan_Combination/madanalysis5")
parser.add_argument("--wmratio", type=str,help='y/n for fixed wy/my ratio',default="y")
parser.add_argument("--model", type=str,help='model',default="S3M")
parser.add_argument("--quark", type=str,help='quark',default="u")
args = parser.parse_args()


MODELArray = [args.model]
XMASSArray = [-5, -1, 0, 1, 10, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000]
YMASSArray = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000]
COUPLINGArray = [1.0]
QuarkArray = [args.quark]
OrderArray = ["LO","NLO"]
processArray = ["XX", "XY", "YYQCD", "YYt", "YYSum", "Full"]
defaultanalysis_list = ["atlas_conf_2019_040","atlas_exot_2018_06", "cms_sus_19_006", "cms_exo_20_004", "atlas_susy_2018_17"]

for model in MODELArray:
    for quark in QuarkArray:
        if model == "S3M" and quark == "u":
            COUPLINGArray = [1.0, 3.5]
        elif model == "F3S" and quark == "u":
            COUPLINGArray = [1.0, 4.8]
        else: 
            COUPLINGArray = [1.0]
        for my in YMASSArray:
            for mx in XMASSArray:
                if mx < 0:
                    mx = mx + my
                if mx >= my:
                    continue
                if my < 1000:
                    sety = "set1"
                elif my > 1000 and my < 2000:
                    sety = "set2"
                elif my > 2000 and my < 3000:
                    sety = "set3"
                else:
                    sety = "set4"
                for coup in COUPLINGArray:  
                    for order in OrderArray:
                        if not os.path.exists(f"log_{quark}_{model}_{order}_{coup}_{sety}"):
                            os.makedirs(f"log_{quark}_{model}_{order}_{coup}_{sety}")
                        if not os.path.exists(f"script_{quark}_{model}_{order}_{coup}"):
                            os.system(f"mkdir -p script_{quark}_{model}_{order}_{coup}")
                        for proc in processArray:
                            if proc == "Full":
                                proccheck = "XX"
                            elif proc == "YYSum" or proc == "YYt":
                                proccheck = "YYtPM"
                            else:
                                proccheck = proc

                            print("")
                            print("")
                            print("+-------------------------------------------------------+")
                            print("| {:<5} | {:<5} | {:<5} | {:<5} | {:<5} | {:<5} | {:<5} |".format("model", "coup", "mY", "mX", "quark", "order", "proc"))
                            print("+-------------------------------------------------------+")
                            print("| {:<5} | {:<5} | {:<5} | {:<5} | {:<5} | {:<5} | {:<5} |".format(model, coup, my, mx, quark, order, proc))
                            print("+-------------------------------------------------------+")
                            print("")
                            print("")

                            if quark != 'c':

                                print("file : ", os.path.join(args.input, "Results_"+model+"_recast","MA5_Recast", model + "_" + proccheck + "_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_recast.tar.gz"))

                            if (quark != 'c' and os.path.exists(os.path.join(args.input, "Results_"+model+"_recast","MA5_Recast", model + "_" + proccheck + "_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_recast.tar.gz"))) or (quark == 'c'):
                                job_name = "script_{}_{}_{}_{}/{}_SM{}_mY{}_mX{}_proc{}_order{}_coup{}.sub".format(quark, model, order, coup, model, quark, my, mx, proc, order, coup)
                                run_name = "script_{}_{}_{}_{}/{}_SM{}_mY{}_mX{}_proc{}_order{}_coup{}.sh".format(quark, model, order, coup, model, quark, my, mx, proc, order, coup)
                                if os.path.exists(job_name): 
                                    os.system("rm " + job_name)
                                if os.path.exists(run_name):
                                    os.system("rm " + run_name)
                                os.system("touch " + run_name)
                                os.system("touch " + job_name)
                                os.system("echo \#!/bin/bash >> {}".format(run_name))
                                os.system("echo cd /eos/user/a/aman/LHCDM_tchan_Combination >> {}".format(run_name))
                                os.system("echo source py3_env/bin/activate >> {}".format(run_name))
                                if quark == 'c':
                                    os.system("echo python {}/NLOCombination_Cquark.py --MY {} --MX {} --coup {} --quark {} --process {} --order {} --model {} --input {} --output {} --wmratio {} >> {}".format(args.programpath, my, mx, coup, quark, proc, order, model, args.input, args.output, args.wmratio, run_name))
                                else:
                                    os.system("echo python {}/NLOCombination.py --MY {} --MX {} --coup {} --quark {} --process {} --order {} --model {} --input {} --output {} --wmratio {} >> {}".format(args.programpath, my, mx, coup, quark, proc, order, model, args.input, args.output, args.wmratio, run_name))
                                os.system("echo Executable            = {}>> {}".format(run_name, job_name))
                                os.system(f"echo Output                = log_{quark}_{model}_{order}_{coup}_{sety}/ap.{job_name}.\$\(ClusterId\).\$\(ProcId\).out >> {job_name}")
                                os.system(f"echo Error                 = log_{quark}_{model}_{order}_{coup}_{sety}/ap.{job_name}.\$\(ClusterId\).\$\(ProcId\).err >> {job_name}")
                                os.system(f"echo Log                   = log_{quark}_{model}_{order}_{coup}_{sety}/ap.{job_name}.\$\(ClusterId\).\$\(ProcId\).log >> {job_name}")
                                os.system("echo should_transfer_files   = yes >> {}".format(job_name))
                                os.system("echo RequestCpus = 1 >> {}".format(job_name))
                                os.system("echo +JobFlavour = \"\'workday\'\" >> {}".format(job_name))
                                os.system("echo queue >> {}".format(job_name))

                                name_recast_file = model + "_" + proc + "_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_coup" + str(coup) + "_recast"

                                if os.path.exists(os.path.join(args.output, name_recast_file, "CLs_output.dat")) and os.path.exists(os.path.join(args.output, name_recast_file, "CLs_output.json")):
                                    path_json = os.path.join(args.output, name_recast_file, "CLs_output.json")
                                    file_json = open(path_json)
                                    path_dat = os.path.join(args.output, name_recast_file, "CLs_output.dat")
                                    file_dat = open(path_dat)
                                    try:
                                        data = json.load(file_json)
                                        analysis_list = list(data.keys())
                                        df = pd.read_csv(file_dat, delimiter=r'\s+')
                                        unique_dat = list(df["#"].unique())
                                        if "#" in unique_dat:
                                            unique_dat.remove("#") 
                                        analysis_dat = unique_dat
                                        defaultanalysis_list.sort()
                                        analysis_dat.sort()
                                        analysis_list.sort()
                                        if len(analysis_dat) > 0:
                                            #if analysis_list == defaultanalysis_list and analysis_dat == defaultanalysis_list:
                                            print(os.path.join(args.output, name_recast_file, "CLs_output.dat"), "file exists with analysis")
                                            print("skipping")
                                            continue
                                        else:
                                            print("need to rerun again for all analysis")
                                            os.system("condor_submit {}".format(job_name))
                                    except:
                                        os.system("condor_submit {}".format(job_name))
                                else:
                                    os.system("condor_submit {}".format(job_name))
                            else:
                                print(os.path.join(args.input, "Results_"+model+"_recast","MA5_Recast", model + "_" + proccheck + "_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_recast.tar.gz"), "file does not exists")
