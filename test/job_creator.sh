#!/bin/bash
currentfolder=$(pwd)
declare -a MODELArray=("S3D" "S3M" "F3S" "F3C" "F3V" "F3W")

# --- masses --- #
declare -a XMASSArray=(10 50); # 100); # DM masses
declare -a YMASSArray=(100 200); # mediator masses
declare -a COUPLINGArray=("5"); # "1" "3.5" "4.8"); 
declare -a MODELArray=("S3M"); # "F3S" "F3V")
declare -a QuarkArray=("d"); # "F3S" "F3V")


for my in ${YMASSArray[@]}; do
for mx in ${XMASSArray[@]}; do
for coupling1 in ${COUPLINGArray[@]}; do
for model in ${MODELArray[@]}; do
for quark in ${QuarkArray[@]}; do

# create a .sub file named using model, mx, my, coupling, quark; the only difference from file to file is that run.sh name changes 


#""" file starts

#Executable            = <change name>.sh
#Output                = log/ap.$(ClusterId).$(ProcId).out
#Error                 = log/ap.$(ClusterId).$(ProcId).err
#Log                   = log/ap.$(ClusterId).log
#should_transfer_files   = yes
#RequestCpus = 8
#+JobFlavour = "testmatch"
#queue

#""" file ends

#=================
# create a run.sh file with the following commands where individual masses changes: 


#""" file starts

#!/bin/bash

#cd /eos/user/a/aman/LHCDM_tchan_Combination
#source py3_env/bin/activate
#python NLOCombination.py --MY 1300 --MX 900 --coup 5 --quark d --order NLO --model F3S 


#""" file ends


done
done
done
done

# loop over the list of job.sub files to submit job to condor. 

