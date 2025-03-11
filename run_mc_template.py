# source /cvmfs/cms.cern.ch/common/crab-setup.sh
# python3 run_mc.py

import os, sys
from optparse import OptionParser
from multiprocessing import Process
import subprocess

from CRABAPI.RawCommand       import crabCommand
from CRABClient.UserUtilities import config
from CRABClient.JobType       import CMSSWConfig

if __name__ == "__main__":

    process_name = "{PROCNAME}"

    parser = OptionParser(usage = "python run_mc.py [options]", description = "Main options")
    parser.add_option("--storage", dest = "storage", default = "T3_CH_CERNBOX", help = "Storage site") 
    parser.add_option("--nevents", dest = "nevents", default = 1e6, type = int, help = "Storage site") 
    opts, args = parser.parse_args()
    
    config = config()
    def submit(config):
        res = crabCommand('submit', config = config)

    workarea  = "{PROCNAME}_workarea"
    config.General.requestName  = "{PROCNAME}_ddm"
    config.General.workArea     = workarea
    config.General.transferLogs = True

    # Job type
    config.JobType.pluginName  = 'PrivateMC'
    config.JobType.allowUndistributedCMSSW = True
    config.JobType.numCores = 8
    config.JobType.psetName    = './{PSETNAME}'
    config.JobType.maxMemoryMB = 4000

    # Data handling
    config.Data.splitting   = 'EventBased'
    config.Data.unitsPerJob = 2000 
    config.Data.totalUnits  = opts.nevents 
    config.Data.outputPrimaryDataset = "{PROCNAME}"
    config.Data.publication = False 
    config.Data.inputDBS = "phys03"
    config.Data.outputDatasetTag = "{DATASET_TAG}"

    # I/O
    config.Site.storageSite = opts.storage
    config.Site.blacklist   = []
    config.Site.ignoreGlobalBlacklist = True

    p = Process(target=submit, args=(config,))
    p.start()
    p.join()
    del p
    del config




