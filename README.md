# PixelTree-ProductionTool

DPG Tool for making pixel trees: batch handler, DAS handler
instructions.txt has some useful tips but is out of date.

Recipe:
cmsrel CMSSW_X_Y_Z (e.g 9_1_0_pre3)
cd CMSSW_X_Y_Z/src; cmsenv
git clone https://github.com/cms-analysis/DPGAnalysis-SiPixelTools.git
cd DPGAnalysis-SiPixelTools/PixelTrees/
scram b -j12
git clone https://github.com/BenjaminMesic/PixelTree-ProductionTool.git

voms-proxy-init --voms cms --valid 168:00 -rfc

python TreeProduction.py

NOTE:
TreeProduction.py is main script. 
By default, it makes python config files without sending them to batch.
If you want to send jobs, uncomment
# t.send_jobs()
