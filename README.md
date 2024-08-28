# LHCDM_tchan_Combination
MA5 Expert Analysis Final result combination at NLO 

Step 1: 

Run `source installation_scripts/install_lxplus.sh` to install all necessary packages

**Note**: Needs the user to change path for installation

Step 2: 

`source py3_env/bin/activate`


To run interactively, use `python NLOCombination.py --MY 1300 --MX 900 --coup 5 --quark d --order NLO --model F3S`

for submission to condor:

`run.sh` and `job.sub` are used

## To submit multiple condor jobs: 

Options for Job Submit script

```code
python job_creator.py
usage: DMSimpt_Combination [-h] [--input INPUT]
                           [--programpath PROGRAMPATH]
                           [--output OUTPUT] [--ma5dir MA5DIR]
                           [--wmratio WMRATIO] [--model MODEL]
                           [--quark QUARK]

options:
  -h, --help            show this help message and exit
  --input INPUT         Input Data file path and Name
  --programpath PROGRAMPATH
                        path to NLOCombination.py
  --output OUTPUT       Output file path and Name
  --ma5dir MA5DIR       Input file path and Name
  --wmratio WMRATIO     y/n for fixed wy/my ratio
  --model MODEL         model
  --quark QUARK         quark
``` 


Options for NLOCombination.py

```code
python NLOCombination.py --help
usage: DMSimpt_Combination [-h] [--MY MY] [--MX MX]
                           [--coup COUP] [--quark QUARK]
                           [--order ORDER] [--model MODEL]
                           [--input INPUT] [--output OUTPUT]
                           [--ma5dir MA5DIR]
                           [--wmratio WMRATIO]

options:
  -h, --help         show this help message and exit
  --MY MY            mass of DM mediator
  --MX MX            mass of DM particle
  --coup COUP        Coupling
  --quark QUARK      Quark
  --order ORDER      order
  --model MODEL      Model
  --input INPUT      Input file path and Name
  --output OUTPUT    Output file path and Name
  --ma5dir MA5DIR    Input file path and Name
  --wmratio WMRATIO  yes/no for fixed wy/my ratio
```



=========================================

python3 job_creator.py --input /eos/user/a/aman/SamplesForAman/d --wmratio n

python3 job_creator.py --input /eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/d  --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_d_S3M/ --wmratio y --quark d --model S3M

python3 job_creator.py --input /eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/d  --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_d_F3S/ --wmratio y --quark d --model F3S

python3 job_creator.py --input /eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/d  --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_d_F3V/ --wmratio y --quark d --model F3V



python3 job_creator.py --input /eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/s --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_s_S3M/ --wmratio y --quark s --model S3M

python3 job_creator.py --input /eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/s --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_s_F3S/ --wmratio y --quark s --model F3S

python3 job_creator.py --input /eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/s --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_s_F3V/ --wmratio y --quark s --model F3V



python3 job_creator.py --input /eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/u  --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_u_S3M/ --wmratio y --quark u --model S3M

python3 job_creator.py --input /eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/u  --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_u_F3S/ --wmratio y --quark u --model F3S

python3 job_creator.py --input /eos/project/d/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/u  --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_u_F3V/ --wmratio y --quark u --model F3V



python3 job_creator.py --input /eos/project/b/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/b  --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_b_S3M/ --wmratio y --quark b --model S3M

python3 job_creator.py --input /eos/project/b/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/b  --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_b_F3S/ --wmratio y --quark b --model F3S

python3 job_creator.py --input /eos/project/b/dmwg-shared-space/DM_tchannel/GeneralSimulation/Results/b  --output /eos/user/a/aman/LHCDM_tchan_Combination/output2/output_b_F3V/ --wmratio y --quark b --model F3V

