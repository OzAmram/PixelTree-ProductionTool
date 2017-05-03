#!/bin/bash

export SCRAM_ARCH= <SCRAM_ARCH>
export X509_USER_PROXY= <X509_USER_PROXY>

cd <working_directory>
eval `scramv1 runtime -sh`

cd -
cmsRun <path_python_file>

cmsStage -f  <root_file_name> <root_file_name_destination>
rm <root_file_name> 