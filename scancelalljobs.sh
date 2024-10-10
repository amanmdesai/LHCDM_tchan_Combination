#!/bin/bash

currentfolder=$(pwd)
currentfile=$(basename "$0")

# Check if no arguments provided
if [ $# -eq 0 ]; then
    jobname="_reinterpretation"  # Default value
else
    jobname="$1"  # Use the provided argument
fi

# Get list of running jobs
runningjobs=$(condor_q -dag -nobatch | grep "${jobname}" | awk '{print $1}')
echo $runningjobs
# If there are running jobs, remove them
if [[ ! -z $runningjobs ]]; then
    condor_rm $runningjobs
fi
