# Repo with scripts to produce DDM samples with CRAB

## Setup
By default the production is run in CMSSW_12_4_5. This is an el7 release, and therefore one needs to use singularity containers to run it on lxplus. The setup can be done using the following commands in any LXPLUS node:

```
cmssw-el7
source setup
```

## Generating cfgs
For a given mass of the Higgs boson (`mh`), mass of the boson that produces the LLPs (`mx`) and lifetime of the X candidate (`ctaux`), a template fragment is used to generate the corresponding CFGs. To produce CFGs one simply needs to run:

```
python3 prepare_ddm_longlived_cfgs.py --mh $mh --mx $mx --ctaux $ctaux  
```

This will generate:
 * A `fragment` file that will be stored under `CMSSW_12_4_5/src/Configuration/GenProduction/python/MH-${mh}_MX-${mx}_CTAUX${ctaux}/fragment.py`. This is used by the `cmsDriver.py` to generate the submission script.
 * A `pset` config file that will be stored `CMSSW_12_4_5/src/MH-${mh}_MX-${mx}_CTAUX${ctaux}/pset.py` with the output of the `cmsDriver.py`.
 * A `crab` submission file stored in `CMSSW_12_4_5/src/MH-${mh}_MX-${mx}_CTAUX${ctaux}/run_mc.py` with all the necessary stuff to run MC production on crab. 

To run MC, one can simply do

```
python3 run_mc.py --storage $storage --nevents $nevents
```

## Notes
 * By default, the output storage is set to the CERNBOX of the user that submits the jobs. This can be changed either in the `run_mc_template.py` script in the source folder, or by using the option `--storage $storage` when submitting the generation of events.
 * By default the script will run 1M events in total, with an splitting of 2k events per job.
 * By default the output tier will be GEN-SIM-DIGI-RAW, and the L1 Trigger will also run. This can be changed in the `prepare_ddm_longlived_cfgs.py` script, by modifying the options `datatier` and `-s GEN,SIM,L1,DIGI,DIGI2RAW` options in the script (the `-s` stems from "steps" to run).
