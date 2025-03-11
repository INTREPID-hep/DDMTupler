source /cvmfs/cms.cern.ch/cmsset_default.sh
release=CMSSW_12_4_5
scram=slc7_amd64_gcc700
export SCRAM_ARCH=$scram
cmsrel $release
cd $release
cmsenv
cd -
