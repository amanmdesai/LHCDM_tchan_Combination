import os
import argparse

parser = argparse.ArgumentParser(prog = 'DMSimpt_Combination',description = '')
parser.add_argument("--input", type=str,help='Input Data file path and Name',default="/eos/user/a/aman/dsb_lowstat/")
parser.add_argument("--programpath", type=str,help='path to NLOCombination.py',default="/eos/user/a/aman/LHCDM_tchan_Combination/")
parser.add_argument("--output", type=str,help='Output file path and Name',default="/eos/user/a/aman/LHCDM_tchan_Combination/output/")
parser.add_argument("--ma5dir", type=str,help='Input file path and Name',default="/eos/user/a/aman/LHCDM_tchan_Combination/madanalysis5")
parser.add_argument("--wmratio", type=str,help='yes/no for fixed wy/my ratio',default="yes")
args = parser.parse_args()

MODELArray = ["F3S"]
YMASSArray = [1300]
XMASSArray = [900]
COUPLINGArray = [5]
QuarkArray = ["d"]
OrderArray = ["NLO"]

"""
MODELArray = ["S3D", "S3M", "F3S", "F3C", "F3V", "F3W"]
XMASSArray = [10, 50]
YMASSArray = [100, 200]
COUPLINGArray = [5]
QuarkArray = ["d"]
OrderArray = ["LO", "NLO"]
"""

for my in YMASSArray:
    for mx in XMASSArray:
        for coup in COUPLINGArray:
            for model in MODELArray:
                for quark in QuarkArray:
                    for order in OrderArray:
                        #if os.path.exists(os.path.join(args.input, "Results_"+model+"_recast","MA5_Recast", model + "_XX_" + order + "_SM"+ quark + "_MY" + str(my) + "_MX" + str(mx) + "_recast")):
                            job_name = "{}_SM{}_mY{}_mX{}_coup{}.sub".format(model, quark, my, mx, coup)
                            run_name = "{}_SM{}_mY{}_mX{}_coup{}.sh".format(model, quark, my, mx, coup)
                            os.system("rm " + run_name)
                            os.system("echo \#!/bin/bash >> {}".format(run_name))
                            os.system("echo cd /eos/user/a/aman/LHCDM_tchan_Combination >> {}".format(run_name))
                            os.system("echo source py3_env/bin/activate >> {}".format(run_name))
                            os.system("echo python {}/NLOCombination.py --MY {} --MX {} --coup {} --quark {} --order NLO --model {} --input {} --output {} --wmratio {} >> {}".format(args.programpath, my, mx, coup, quark, model, args.input, args.output, args.wmratio, run_name))
                            os.system("rm " + job_name)
                            os.system("touch " + job_name)
                            os.system("echo Executable            = {}>> {}".format(run_name, job_name))
                            os.system("echo Output                = log/ap.{}.out >> {}".format(job_name,job_name))
                            os.system("echo Error                 = log/ap.{}.err >> {}".format(job_name,job_name))
                            os.system("echo Log                   = log/ap.{}.log >> {}".format(job_name,job_name))
                            os.system("echo should_transfer_files   = yes>> {}".format(job_name))
                            os.system("echo RequestCpus = 8 >> {}".format(job_name))
                            os.system("echo +JobFlavour = 'testmatch' >> {}".format(job_name))
                            os.system("echo queue>> {}".format(job_name))
                            os.system("condor_submit {}".format(job_name))