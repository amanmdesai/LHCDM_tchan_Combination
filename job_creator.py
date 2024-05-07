import os

MODELArray = ["S3D", "S3M", "F3S", "F3C", "F3V", "F3W"]
XMASSArray = [10, 50]
YMASSArray = [100, 200]
COUPLINGArray = [5]
QuarkArray = ["d"]

for my in YMASSArray:
    for mx in XMASSArray:
        for coup in COUPLINGArray:
            for model in MODELArray:
                for quark in QuarkArray:
                    job_name = "{}_SM{}_mY{}_mX{}_coup{}.sub".format(model, quark, my, mx, coup)
                    run_name = "{}_SM{}_mY{}_mX{}_coup{}.sh".format(model, quark, my, mx, coup)

                    os.system("rm " + run_name)
                    os.system("echo cd /eos/user/a/aman/LHCDM_tchan_Combination>> {}".format(run_name))
                    os.system("echo source py3_env/bin/activate >> {}".format(run_name))
                    os.system("echo python NLOCombination.py --MY 1300 --MX 900 --coup 5 --quark d --order NLO --model F3S  >> {}".format(run_name))
                    os.system("rm " + job_name)
                    os.system("touch " + job_name)
                    os.system("echo Executable            = {}>> {}".format(run_name, job_name))
                    #os.system(f"echo Output                = log/ap.$(ClusterId).$(ProcId).out>> {job_name}")
                    #os.system(f"echo Error                 = log/ap.$(ClusterId).$(ProcId).err>> {job_name}")
                    #os.system(f"echo Log                   = log/ap.$(ClusterId).log>> {job_name}")
                    os.system("echo should_transfer_files   = yes>> {}".format(job_name))
                    os.system("echo RequestCpus = 8 >> {}".format(job_name))
                    os.system("echo +JobFlavour = 'testmatch' >> {}".format(job_name))
                    os.system("echo queue>> {}".format(job_name))
                    os.system("condor_submit {}".format(job_name))



