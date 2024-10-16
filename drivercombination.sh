#!/bin/bash

# uncomment for debug purposes
# set -x 

currentfolder=$(pwd)
currentfile=`basename "$0"`

####################### 
#### DM PARAMETERS ####
#######################

declare -a XMASSArray=(-5 -1 1 10 50 100); # DM masses
declare -a YMASSArray=(10 50 100); # mediator masses
for i in `seq 0 100 4000`; do XMASSArray=("${XMASSArray[@]}" "$i"); YMASSArray=("${YMASSArray[@]}" "$i"); done

declare -a COUPLINGArray=(-0.05)
# declare -a QUARKArray=("u" "d" "c" "s" "t" "b" "u d c s t b")
declare -a QUARKArray=("u" "d")

# declare -a MODELArray=("S3M" "F3S" "F3V" "S3D" "F3C" "F3W")
declare -a MODELArray=("S3M" "F3S" "F3V")
declare -a PROCESSArray=("XX" "XY" "YYQCD" "YYtch" "YYsum" "Full")
declare -a ORDERArray=("NLO" "LO")

##############################
#### LXPLUS CONFIGURATION ####
##############################

lxplususer=$USER
condorsubfolder="${HOME}/condorsubs/DMtsimp_condor_reinterpretations" # folder where simulation logs are stored. It will be generated automatically if non-existent
lxpluscores=1
walltime="00:03:00:00" # dd:hh:mm:ss
#walltime="\"testmatch\"" # this is an alternative way: if a flavour is given, it will be automatically assigned to JobFlavour instead of +MaxRuntime
walltime="\"microcentury\"" # this is an alternative way: if a flavour is given, it will be automatically assigned to JobFlavour instead of +MaxRuntime

maxrunningjobs=3000; # how many jobs can be queued at the same time: when this value is hit, the script will wait ${waittosubmit} seconds for jobs to complete before submitting others
waittosubmit=60; # how many seconds to wait before checking again

outputlabel="_reinterpretation"

ResultsFolder="/eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/Reinterpretations"

##################
#### test run ####
##################


#declare -a MODELArray=("S3M")
#declare -a PROCESSArray=("Full")
#declare -a ORDERArray=("NLO")





###############
#### LOOPS ####
###############

XMASSArray=($(printf "%s\n" "${XMASSArray[@]}" | sort -nu)); 
YMASSArray=($(printf "%s\n" "${YMASSArray[@]}" | sort -nu)); 

echo "x mass array: ${XMASSArray[@]}"
echo "y mass array: ${YMASSArray[@]}"

jobcounter=1
for quark in ${QUARKArray[@]}; do
for model in ${MODELArray[@]}; do
for process in ${PROCESSArray[@]}; do
for order in ${ORDERArray[@]}; do
for my in ${YMASSArray[@]}; do
for mx1 in ${XMASSArray[@]}; do


  #######################
  #### DEFINE X MASS ####
  #######################

  mx=$mx1
  if (( $(echo "$mx1 < 0" |bc -l) )); then mx=$(echo "${my}+${mx1}" | bc -l); fi
  

  ###################################
  #### SOME ONLY-LO COMBINATIONS ####
  ###################################
  # Vector DM because some processes have a vector propagator which cannot be treated consistently in a simplified model (gauge invariance)
  if [[ $model == "F3V" || $model == "F3W" ]] && [[ $order == "NLO" ]]; then continue; fi

  ############################
  #### CONSISTENCY CHECKS ####
  ############################
  
  # consistency of the scan point: my>mx+mq; for light quarks mq=0
  if (( $(echo "$my <= $mx" |bc -l) )); then continue; fi
  # consistency of the scan point: my>0 and mx>0
  if (( $(echo "$my <= 0" |bc -l) )) || (( $(echo "$mx <= 0" |bc -l) )); then continue; fi
  
  # some processes are not allowed for specific quark generations
  if [[ $quark == "t" ]]; then
    if [[ $process == "XX" && ${order} == "LO" ]] || [[ $process == "XY" || $process == "YYtch" || $process == "YYsum" ]]; then continue; fi 
    if (( $(echo "${my}-${mx} < ${mt}" | bc -l) )); then continue; fi
  fi

  COUPLING1Array=${COUPLINGArray[@]}
  if [[ $quark == "u" || $quark == "d" ]]; then
    if [[ $model == "S3M" || $model == "S3D" ]]; then COUPLING1Array=("${COUPLINGArray[@]}" "3.5"); fi
    if [[ $model == "F3S" || $model == "F3C" ]]; then COUPLING1Array=("${COUPLINGArray[@]}" "4.8"); fi
    if [[ $model == "F3V" || $model == "F3W" ]]; then COUPLING1Array=("${COUPLINGArray[@]}" "1.0"); fi
  fi

  for coupling in ${COUPLING1Array[@]}; do

    if (( $(echo "$coupling < 0" | bc -l) )); then wmy=$(awk "BEGIN {print -1 * $coupling}"); fi

    #####################
    #### NAME OF RUN ####
    #####################
    qstring="${quark// /}"
    namerun="${model}_${process}_${order}_MY${my}_MX${mx}_SM${qstring}_coup${coupling}${outputlabel}"
    if (( $(echo "$coupling < 0" | bc -l) )); then
      namerun="${model}_${process}_${order}_MY${my}_MX${mx}_SM${qstring}_WMY${wmy}${outputlabel}"
    fi
  
    if (( $(echo "$coupling < 0" | bc -l) )); then
      printf "model=%-3s process=%-5s order=%-3s my=%-5s mx=%-5s wY/mY=%-9.2f quarks=%-12s " $model $process $order $my $mx $wmy $qstring
    else
      printf "model=%-3s process=%-5s order=%-3s my=%-5s mx=%-5s coupling=%-6.1f quarks=%-12s " $model $process $order $my $mx $coupling $qstring
    fi
  
    ###########################################################
    #### CHECK THAT TARBALL IS PRESENT FOR XX, XY or YYQCD ####
    ###########################################################

    find_tarball_for_masses() {
      folder=$1
      mY=$2
      mX=$3
      model=$4

      case "$model" in
        "S3M")
          pattern="mass2000004_([0-9]+\.[0-9]+)_mass52_([0-9]+\.[0-9]+)_dms3u22_([0-9\.eE\+-]+)_xs_([0-9\.eE\+-]+)"
          ;;
        "F3S")
          pattern="mass5920004_([0-9]+\.[0-9]+)_dmf3u22_([0-9\.eE\+-]+)_mass51_([0-9]+\.[0-9]+)_xs_([0-9\.eE\+-]+)"
          ;;
        "F3V")
          pattern="mass5920004_([0-9]+\.[0-9]+)_mass53_([0-9]+\.[0-9]+)_dmf3u22_([0-9\.eE\+-]+)_xs_([0-9\.eE\+-]+)"
          ;;
        *)
          echo "Invalid model: $model"
          return 1
          ;;
      esac

      # Find tarball files in the folder matching the pattern
      matching_files=$(ls "$folder" | grep -E "$pattern")

      # Check if we found any matching files
      if [ -z "$matching_files" ]; then
        # No match found
        return 1
      else
        # Match found
        return 0
      fi

    }

    
    MA5exists=1
    missingpointsfile="$ResultsFolder/Results_${model}_SM${qstring}/${process}_${order}_MY${my}_MX${mx}_coup${coupling}/missingpoints.dat"
    if (( $(echo "$coupling < 0" | bc -l) )); then
      missingpointsfile="$ResultsFolder/Results_${model}_SM${qstring}/${process}_${order}_MY${my}_MX${mx}_WMY${wmy}/missingpoints.dat"
    fi

    if [[ ${process} == "XX" || ${process} == "XY" || ${process} == "YYQCD" ]]; then
      MA5tarballpath="${ResultsFolder}/../${quark}/Results_${model}_recast/MA5_Recast/${model}_${process}_${order}_SM${quark}_MY${my}_MX${mx}_recast.tar.gz"
      if [[ ! -f ${MA5tarballpath} ]]; then MA5exists=0; fi
      if [[ $quark == "c" ]]; then
        MA5tarballpath="${ResultsFolder}/../${model}_${process}/${order}/"
	if ! find_tarball_for_masses "$MA5tarballpath" "$my" "$mx" "$model"; then MA5exists=0; fi
      fi
    elif [[ $process == "YYsum" ]]; then
      if [[ -f $missingpointsfile ]]; then
        for proc1 in "YYtPP" "YYtPM" "YYtMM" "YYt" "YYbt" "YbYbt"; do
          # Check if proc1 is present in the second-to-last column
          if grep -q "\s${proc1}\s" "$missingpointsfile"; then
            MA5tarballpath="${ResultsFolder}/../${quark}/Results_${model}_recast/MA5_Recast/${model}_${proc1}_${order}_SM${quark}_MY${my}_MX${mx}_recast.tar.gz"
            if [[ $quark == "c" ]]; then
              MA5tarballpath="${ResultsFolder}/../${model}_${proc1}/${order}/"
	    fi
            # Check if tarball does not exist
            if [[ ! -f "$MA5tarballpath" ]]; then printf "$proc1 "; MA5exists=0; fi
          fi
        done
      fi
    elif [[ $process == "Full" ]]; then
      if [[ -f $missingpointsfile  ]]; then
        for proc1 in "XX" "XY" "YYQCD" "YYi" "YYtPP" "YYtPM" "YYtMM" "YYt" "YYbt" "YbYbt"; do
           # Check if proc1 is present in the second-to-last column
          if grep -q "\s${proc1}\s" "$missingpointsfile"; then
            MA5tarballpath="${ResultsFolder}/../${quark}/Results_${model}_recast/MA5_Recast/${model}_${proc1}_${order}_SM${quark}_MY${my}_MX${mx}_recast.tar.gz"
            if [[ $quark == "c" ]]; then
              MA5tarballpath="${ResultsFolder}/../${model}_${proc1}/${order}/"
            fi
            # Check if tarball does not exist
	    if [[ ! -f "$MA5tarballpath" ]]; then printf "$proc1 "; MA5exists=0; fi
          fi
        done
      fi
    fi
    if [[ $MA5exists == "0" ]]; then
      echo "MA5 tarball not found!"
      continue
    fi
    
    ########################################
    #### CHECK THAT RUN IS NOT DONE YET ####
    ########################################
    tarballresult="$ResultsFolder/Results_${model}_SM${qstring}/${process}_${order}_MY${my}_MX${mx}_coup${coupling}.tar.gz"
    if (( $(echo "$coupling < 0" | bc -l) )); then
      tarballresult="$ResultsFolder/Results_${model}_SM${qstring}/${process}_${order}_MY${my}_MX${mx}_WMY${wmy}.tar.gz"
    fi

    # Check if the tarball exists
    if [[ -f "$tarballresult" ]]; then
      # Check if tarball is corrupted (by checking return value of tar)
      if tar -tzf "$tarballresult" > /dev/null 2>&1; then
        # Tarball is valid, now check for 'done' file
        if tar -tzf "$tarballresult" | grep -q 'done'; then
          echo "already done"
          continue
        else
          # 'done' file not found, proceed to remove the tarball and reprocess
          printf "'done' file not found, removing and reprocessing... "
          rm "$tarballresult"
        fi
      else
        # Tarball is corrupted
        printf "Corrupted tarball detected, removing and reprocessing... "
        rm -f "$tarballresult"                # Remove the corrupted tarball
        folder="${tarballresult%.tar.gz}"      # Derive the folder name by removing the suffix
        rm -rf "$folder"                       # Remove the corresponding folder
      fi
    fi




    ##############################
    #### NAME OF CONDOR FILES ####
    ##############################
  
    condorsubfolder1="${condorsubfolder}/${model}_${order}_SM${qstring}" 
    condorsub="${condorsubfolder1}/${namerun}_condorsub"
    condorscript="${condorsubfolder1}/DMtsimp_${namerun}.sh"
    
    # ------------------------- #
    # write condor instructions #
    # ------------------------- #
    mkdir -p $condorsubfolder1

    # convert walltime from dd:hh:mm:ss to nsecs (if not in this format, it won't change the variable)
    IFS=':' read -r -a components <<< "$walltime"
    if [[ ${#components[@]} -eq 1 ]]; then
      walltime1="${components[0]}"
    elif [[ ${#components[@]} -eq 2 ]]; then
      walltime1=$(( ${components[0]} * 60 + ${components[1]} ))
    elif [[ ${#components[@]} -eq 3 ]]; then
      walltime1=$(( ${components[0]} * 3600 + ${components[1]} * 60 + ${components[2]} ))
    elif [[ ${#components[@]} -eq 4 ]]; then
      walltime1=$(( ${components[0]} * 86400 + ${components[1]} * 3600 + ${components[2]} * 60 + ${components[3]} ))
    fi

    # write condorsub
    echo "executable              = ${condorscript}"                        > ${condorsub}
    echo "notification            = Error"                                 >> ${condorsub}
    echo "should_transfer_files   = yes"                                   >> ${condorsub}
    echo "output                  = ${condorsubfolder1}/${namerun}_output" >> ${condorsub}
    echo "error                   = ${condorsubfolder1}/${namerun}_output" >> ${condorsub}
    echo "log                     = ${condorsubfolder1}/${namerun}_output" >> ${condorsub}
    echo "RequestCpus             = ${lxpluscores}"                        >> ${condorsub}
    
    # Ensure that output is transferred even if evicted
    echo "WHEN_TO_TRANSFER_OUTPUT = ON_EXIT_OR_EVICT"                      >> ${condorsub}
    echo "+SpoolOnEvict           = False"                                 >> ${condorsub}

    if [[ "${walltime1}" =~ ^[0-9]+$ ]]; then
      echo "+MaxRuntime             = ${walltime1}"                       >> ${condorsub}
    else
      echo "+JobFlavour             = ${walltime}"                        >> ${condorsub}
    fi
    
    echo "queue"                                                          >> ${condorsub}
    
    # write condor script
    echo "#!/bin/bash"                                                     > ${condorscript}
    
    echo ""                                                                                                                                           >> ${condorscript}
    echo "cd /eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/LHCDM_tchan_Combination"                                                  >> ${condorscript}
    echo "source ./py3_env/bin/activate"                                                                                                              >> ${condorscript}
    echo "python NLOCombination.py --MY ${my} --MX ${mx} --coup ${coupling} --order ${order} --model ${model} --quarks ${quark} --process ${process}" >> ${condorscript}
    echo "deactivate"                                                                                                                                 >> ${condorscript}
    echo ""                                                                                                                                           >> ${condorscript}

    # ------------------ #
    # condor the process #
    # ------------------ #
  
    isrunning=$(condor_q -nobatch | grep ${namerun})
    if [[ $isrunning != "" ]]; then 
      echo "already ongoing; skip to next point..." 
      continue
    fi

    # check how many jobs are running before lauching others
    runningjobs=$(condor_q | wc -l ) # this counts also the header and footer lines, which are 8 in total
    totmin=0
    totsec=0
    totdays=0
    tothours=0
    flagrepeat=0
    while (( $(echo "${runningjobs}-8 > ${maxrunningjobs}" | bc -l) ))
    do
      waitm=$((waittosubmit / 60))
      waits=$((waittosubmit % 60))
      for (( n=${waittosubmit}-1; n>=0; n-- )); do
        totsec=$((totsec+1))
        minutes=$((n / 60))
        seconds=$((n % 60))

        totdays=$((totsec / 86400)) # 86400 seconds in a day
        tothours=$((totsec / 3600 % 24)) # Reset tothour after 1 day
        totmin=$((totsec / 60 % 60)) # Reset totmin after 1 hour
        totsec1=$((totsec % 60)) # Reset totsec1 after 1 minute
        if [[ $flagrepeat == "0" ]]; then echo ""; flagrepeat=1; fi
        printf "\r%-3s jobs already running or queuing, checking again in %02dm %02ds before submitting other jobs: -%02d:%02d --- Total wait: %02dd %02dh %02dm %02ds" ${maxrunningjobs} $waitm $waits $minutes $seconds $totdays $tothours $totmin $totsec1
        sleep 1
      done
      runningjobs=$(condor_q | wc -l )
    done
    if [[ $flagrepeat == "1" ]]; then echo ""; fi

  
    cd ${condorsubfolder1}/
    JOBID=$(condor_submit -terse ${condorsub})
    JOBID1=$(echo "$JOBID" | awk '{print $1}')
    runningjobs=$(echo "${runningjobs}-8" | bc )
    echo "Submitted job ${JOBID1} ($runningjobs jobs in queue)"

    ###########################################

#     exit
    
  done
 
done
done
done
done
done
done 
