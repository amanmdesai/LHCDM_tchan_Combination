import os
import argparse

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

os.system(f"rm -rf {args.model}_{args.quark}")
os.system(f"rm -rf log_{args.quark}_{args.model}")
os.system(f"mkdir -p {args.model}_{args.quark}")

for model in MODELArray:
    for quark in QuarkArray:
        if model == "S3M" and quark == "u":
            COUPLINGArray = [1.0, 3.5]
        elif model == "F3S" and quark == "u":
            COUPLINGArray = [1.0, 4.8]
        else: 
            COUPLINGArray = [1.0]
        for coup in COUPLINGArray:  
            for my in YMASSArray:
                for mx in XMASSArray:
                    if mx < 0:
                        mx = mx + my
                    if mx >= my:
                        continue
                    os.system(f"mkdir -p log_{quark}_{model}")
                    for order in OrderArray:
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

                            print("file : ", os.path.join(args.input, "Results_"+model+"_recast","MA5_Recast", model + "_" + proccheck + "_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_recast.tar.gz"))

                            if os.path.exists(os.path.join(args.input, "Results_"+model+"_recast","MA5_Recast", model + "_" + proccheck + "_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_recast.tar.gz")):
                                job_name = "{}_{}/{}_SM{}_mY{}_mX{}_proc{}_order{}_coup{}.sub".format(model, quark, model, quark, my, mx, proc, order, coup)
                                run_name = "{}_{}/{}_SM{}_mY{}_mX{}_proc{}_order{}_coup{}.sh".format(model, quark, model, quark, my, mx, proc, order, coup)
                                if os.path.exists(job_name): 
                                    os.system("rm " + job_name)
                                if os.path.exists(run_name):
                                    os.system("rm " + run_name)
                                os.system("touch " + run_name)
                                os.system("touch " + job_name)
                                os.system("echo \#!/bin/bash >> {}".format(run_name))
                                os.system("echo cd /eos/user/a/aman/LHCDM_tchan_Combination >> {}".format(run_name))
                                os.system("echo source py3_env/bin/activate >> {}".format(run_name))
                                os.system("echo python {}/NLOCombination.py --MY {} --MX {} --coup {} --quark {} --process {} --order {} --model {} --input {} --output {} --wmratio {} >> {}".format(args.programpath, my, mx, coup, quark, proc, order, model, args.input, args.output, args.wmratio, run_name))
                                os.system("echo Executable            = {}>> {}".format(run_name, job_name))
                                os.system(f"echo Output                = log_{quark}_{model}/ap.{job_name}.\$\(ClusterId\).\$\(ProcId\).out >> {job_name}")
                                os.system(f"echo Error                 = log_{quark}_{model}/ap.{job_name}.\$\(ClusterId\).\$\(ProcId\).err >> {job_name}")
                                os.system(f"echo Log                   = log_{quark}_{model}/ap.{job_name}.\$\(ClusterId\).\$\(ProcId\).log >> {job_name}")
                                os.system("echo should_transfer_files   = yes >> {}".format(job_name))
                                os.system("echo RequestCpus = 1 >> {}".format(job_name))
                                os.system("echo +JobFlavour = \"\'tomorrow\'\" >> {}".format(job_name))
                                os.system("echo queue >> {}".format(job_name))

                                name_recast_file = model + "_" + proc + "_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_coup" + str(coup) + "_recast"

                                if os.path.exists(os.path.join(args.output, name_recast_file, "CLs_output.dat")):
                                    print(os.path.join(args.output, name_recast_file, "CLs_output.dat"), "file exists")
                                    print("skipping")
                                    continue
                                else:
                                    os.system("condor_submit {}".format(job_name))
                            else:
                                print(os.path.join(args.input, "Results_"+model+"_recast","MA5_Recast", model + "_" + proccheck + "_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_recast.tar.gz"), "file does not exists")
