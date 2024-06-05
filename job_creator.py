import os
import argparse

parser = argparse.ArgumentParser(prog = 'DMSimpt_Combination',description = '')
parser.add_argument("--input", type=str,help='Input Data file path and Name',default="/eos/user/a/aman/dsb_lowstat/")
parser.add_argument("--programpath", type=str,help='path to NLOCombination.py',default="/eos/user/a/aman/LHCDM_tchan_Combination/")
parser.add_argument("--output", type=str,help='Output file path and Name',default="/eos/user/a/aman/LHCDM_tchan_Combination/output/")
parser.add_argument("--ma5dir", type=str,help='Input file path and Name',default="/eos/user/a/aman/LHCDM_tchan_Combination/madanalysis5")
parser.add_argument("--wmratio", type=str,help='y/n for fixed wy/my ratio',default="y")
args = parser.parse_args()

MODELArray = ["S3M", "F3S", "F3V"]
XMASSArray = [-5, -1, 0, 1, 10, 50, 100, 200, 400, 600, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000]
YMASSArray = [0, 200, 400, 600, 800, 1000, 1200, 1300, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000]
COUPLINGArray = [1, 3.5]
QuarkArray = ["u"]#["d", "s", "u"]
OrderArray = ["LO","NLO"]
#proc = "Full"
processArray = ["XX", "XY", "YYQCD", "YYtPM", "YYSum", "Full"]


for my in YMASSArray:
    for mx in XMASSArray:
        for coup in COUPLINGArray:
            for model in MODELArray:
                for quark in QuarkArray:
                    for order in OrderArray:
                        for proc in processArray:
                            if mx < 0:
                                mx = mx + my
                            if mx >= my:
                                continue
                            print("file : ", os.path.join(args.input, "Results_"+model+"_recast","MA5_Recast", model + "_XX_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_recast.tar.gz"))
                            if os.path.exists(os.path.join(args.input, "Results_"+model+"_recast","MA5_Recast", model + "_XX_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_recast.tar.gz")):
                                job_name = "{}_SM{}_mY{}_mX{}_proc{}_order{}_coup{}.sub".format(model, quark, my, mx, proc, order, coup)
                                run_name = "{}_SM{}_mY{}_mX{}_proc{}_order{}_coup{}.sh".format(model, quark, my, mx, proc, order, coup)
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
                                os.system(f"echo Output                = log/ap.{job_name}.\$\(ClusterId\).\$\(ProcId\).out >> {job_name}")
                                os.system(f"echo Error                 = log/ap.{job_name}.\$\(ClusterId\).\$\(ProcId\).err >> {job_name}")
                                os.system(f"echo Log                   = log/ap.{job_name}.\$\(ClusterId\).\$\(ProcId\).log >> {job_name}")
                                os.system("echo should_transfer_files   = yes >> {}".format(job_name))
                                os.system("echo RequestCpus = 1 >> {}".format(job_name))
                                os.system("echo +JobFlavour = \"\'tomorrow\'\" >> {}".format(job_name))
                                #os.system("echo +AccountingGroup = \"\'group_u_FCC.local_gen\"\' >> {}".format(job_name))
                                os.system("echo queue >> {}".format(job_name))

                                name_recast_file = model + "_" + proc + "_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_coup" + str(coup) + "_recast"

                                if os.path.exists(os.path.join(args.output, name_recast_file, "CLs_output.dat")):
                                    print(os.path.join(args.output, name_recast_file, "CLs_output.dat"), "file exists")
                                    print("skipping")
                                    continue
                                else:
                                    os.system("condor_submit {}".format(job_name))
                            else:
                                print(os.path.join(args.input, "Results_"+model+"_recast","MA5_Recast", model + "_XX_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_recast.tar.gz"), "file does not exists")
