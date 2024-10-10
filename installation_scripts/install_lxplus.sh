#!/bin/bash

# uncomment for debug purposes
# set -x 

currentfolder="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
currentfile="${0##*/}"

###################################
#### INSTALL AND CONFIGURE MA5 ####
###################################
InstallMadAnalysisfolder="${currentfolder}/../"


if [[ ! -e ${InstallMadAnalysisfolder}/MA5installed ]]; then
  if [[ -d ${InstallMadAnalysisfolder}/madanalysis5 ]]; then
    echo "Removing previous MA5 installation"
    rm -rf ${InstallMadAnalysisfolder}/madanalysis5
  fi

echo "Installing MA5"
mkdir -p ${InstallMadAnalysisfolder}
cd ${InstallMadAnalysisfolder}
git clone https://github.com/MadAnalysis/madanalysis5.git

python3 -m venv py3_env
source py3_env/bin/activate
pip3 install --upgrade pip
python3 -m pip install scipy click tqdm six jsonschema jsonpatch PyYAML pyhf pandas lxml ma5-expert  
#   deactivate

  # bug fix: modify the ma5 executable to work with python > 3.9 (see https://github.com/MadAnalysis/madanalysis5/issues/237)
  # if fixed in new releases this has no effect
  sed -i "s|import importlib|from importlib import util|g"                               ${InstallMadAnalysisfolder}/madanalysis5/bin/ma5
  sed -i "s|if not importlib.util.find_spec(\"six\"):|if not util.find_spec(\"six\"):|g" ${InstallMadAnalysisfolder}/madanalysis5/bin/ma5

  cd ${InstallMadAnalysisfolder}/madanalysis5
  python3 bin/ma5 -s < $InstallMadAnalysisfolder/installation_scripts/MA5_installpackages

  cd $InstallMadAnalysisfolder

  # bug fix to avoid the recast crashing for some searches
  # if fixed in new releases this has no effect
  sed -i "s|new_sigma = new_sigma \* lumi_scaling\*\*2|new_sigma = sigma\*lumi_scaling\*\*2|g" ${InstallMadAnalysisfolder}/madanalysis5/madanalysis/misc/run_recast.py

  if [[ -d ${InstallMadAnalysisfolder}/madanalysis5/tools/PADForSFS ]] && [[ -d ${InstallMadAnalysisfolder}/madanalysis5/tools/PAD ]]; then
    touch ${InstallMadAnalysisfolder}/MA5installed
  fi
fi

deactivate
