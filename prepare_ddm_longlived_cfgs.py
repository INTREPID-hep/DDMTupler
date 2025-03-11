"""
Macro to generate GENSIM-CFGs for MC generation. The code works in the following tree structure:

|-- CMSSW_12_4_5/src # This is the release folder
|---------------- Configuration/GenProduction/python/ # This is the folder where fragments are stored
|---------------- $PROC # The value of $PROC depends on the input parameters 

Notes: usage of CMSSW_12_4_5 needs use of singularity. 
"""

import sys
import os
import subprocess
import argparse
from datetime import datetime

# The name below will be applied to the dataset name. It's only relevant for dataset publication
# on DAS.

date = datetime.today().strftime( "%Y-%m-%d" ).replace("-", "_")
dataset_tag = f"privateMC_DDM_{date}"

def create_folder( fold ):
    """ Just create an output folder if it does not exist """
    if not os.path.exists( fold ):
        os.system( f"mkdir -p {fold}" )
        return False
    return True

if __name__ == "__main__":

    # -- Get user input and convert into dictionary
    parser = argparse.ArgumentParser()
    parser.add_argument('--mh', dest = "HIGGSMASS", default = "125", help = "Mass of the Higgs boson")
    parser.add_argument('--mx', dest = "XMASS", default = "2000", help = "Mass of the scalar boson")
    parser.add_argument('--ctaux', dest = "XCTAU", default = "10", help = "Lifetime of the scalar boson")

    opts = vars( parser.parse_args() )
    opts["HIGGSWIDTH"] = 0.027 * float( opts["HIGGSMASS"] ) # Width higgs
    opts["XWIDTH"] = ( 1000. / float( opts["XCTAU"] ) )*0.19733e-15 # Width of the scalar


    # Define process name
    proc_name = "HTo2LongLivedTo2mu2jets_MH-{HIGGSMASS}_MFF-{XMASS}_CTau-{XCTAU}_TuneCP5_13p6TeV".format( **opts )
    cfgname = f"fragment.py"
    psetname = f"pset.py"

    # -- Define relevant paths
    pwd             = os.getcwd()
    fold_name       = "MH-{HIGGSMASS}_MX-{XMASS}_CTAUX{XCTAU}".format( **opts )
    release_folder  = f"{pwd}/CMSSW_12_4_5/src"
    fragment_folder = f"Configuration/GenProduction/python/{fold_name}" # To be used from within release_folder 
    submit_folder   = f"{pwd}/CMSSW_12_4_5/src/{fold_name}"


    # -- Read the template and prepare the content for the fragment
    f = open( "template_fragment.py", "r" )
    content = f.read()
    content = content.format( **opts ) 
    f.close()

    # -- Start writing stuff
    os.chdir( release_folder ) 

    # -- Save the fragment
    create_folder( fragment_folder )
    os.chdir( fragment_folder ) 

    outf = open( cfgname, "w" )
    outf.write( content )
    outf.close()

    # -- Return to the workfolder
    create_folder( submit_folder )
    os.chdir( submit_folder )

    # -- Create and run the cmsDriver
    cmd_args = [
        "cmsDriver.py",
	    f"{fragment_folder}/{cfgname}",
        "-n 1000", 
        "-s GEN,SIM,DIGI,L1,DIGI2RAW", #,DIGI,L1,DIGI2RAW 
        "--nThreads=8",
        "--conditions=auto:phase1_2023_realistic",
        "--era=Run3",
	    "--geometry=SimDB",
        "--fileout=file:out.root",
        "--eventcontent=FEVTDEBUGHLT",
        "--pileup=NoPileUp",
        "--datatier=GEN-SIM-DIGI-RAW", # GEN-SIM-DIGI-RAW
        f"--python_filename={psetname}",
	    "--no_exec",
        "--mc"
    ] 

    # Compile the fragments
    os.system( "scram b -j 8" )
    os.system( " ".join( cmd_args ) )


    # Now also copy the submission script
    opts_for_submit = {
        "PROCNAME" : proc_name,
        "PSETNAME" : psetname,
        "DATASET_TAG" : dataset_tag
    }

    f = open( f"{pwd}/run_mc_template.py", "r" )
    content = f.read()
    content = content.format( **opts_for_submit ) 
    f.close()

    fout = open("run_mc.py", "w")
    fout.write( content )
    fout.close()
