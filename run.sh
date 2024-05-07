#!/bin/bash

cd /eos/user/a/aman/LHCDM_tchan_Combination
source py3_env/bin/activate
python NLOCombination.py --MY 1300 --MX 900 --coup 5 --quark d --order NLO --model F3S 
#python NLOCombination.py
