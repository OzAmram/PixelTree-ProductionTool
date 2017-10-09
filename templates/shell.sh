#!/bin/bash

export SCRAM_ARCH=<SCRAM_ARCH>
export X509_USER_PROXY=<X509_USER_PROXY>

cd <working_directory>
eval `scramv1 runtime -sh`

cd -
cmsRun <path_python_file>

cp <root_file_name> /eos/cms/<root_file_name_destination>/
rm <root_file_name> 
