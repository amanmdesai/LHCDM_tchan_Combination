#!/bin/bash
currentfolder=$(pwd)
declare -a MODELArray=("S3D" "S3M" "F3S" "F3C" "F3V" "F3W")

# --- masses --- #
declare -a XMASSArray=(10 50); # 100); # DM masses
declare -a YMASSArray=(100 200); # mediator masses
declare -a COUPLINGArray=("5"); # "1" "3.5" "4.8"); 
declare -a MODELArray=("S3M"); # "F3S" "F3V")



for my in ${YMASSArray[@]}; do
for mx in ${XMASSArray[@]}; do
for coupling1 in ${COUPLINGArray[@]}; do
for model in ${MODELArray[@]}; do

Executable_Name = ${model}_${mx}_${my}_${coupling1}_run.sh

touch $Executable_Name


done
done
done
done

#Executable            = run.sh
#Output                = log/ap.$(ClusterId).$(ProcId).out
#Error                 = log/ap.$(ClusterId).$(ProcId).err
#Log                   = log/ap.$(ClusterId).log
#should_transfer_files   = yes
#RequestCpus = 8
#+JobFlavour = "testmatch"
#queue
