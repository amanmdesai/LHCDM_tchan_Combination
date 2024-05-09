# LHCDM_tchan_Combination
MA5 Expert Analysis Final result combination at NLO 

Step 1: 

Run `source install_lxplus.sh` to install all necessary packages

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
                           [--output OUTPUT] [--ma5dir MA5DIR]
                           [--wmratio WMRATIO]

options:
  -h, --help         show this help message and exit
  --input INPUT      Input file path and Name
  --output OUTPUT    Output file path and Name
  --ma5dir MA5DIR    Input file path and Name
  --wmratio WMRATIO  yes/no for fixed wy/my ratio
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