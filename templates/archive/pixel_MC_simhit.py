# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: -s GEN,SIM,DIGI,L1,DIGI2RAW,RAW2DIGI,RECO --evt_type MinBias_cfi --conditions auto:phase1_2017_realistic --era Run2_2017 --geometry DB:Extended --fileout file:MinBias_GENSIMRECO.root --python_filename=PahseI_MinBias_cfg.py --runUnscheduled -n 10
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RECO',eras.Run2_2017)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic50ns13TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
	input = cms.untracked.int32(5)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
	annotation = cms.untracked.string('MinBias_cfi nevts:10'),
	name = cms.untracked.string('Applications'),
	version = cms.untracked.string('$Revision: 1.19 $')
)

# Additional output definition

# Other statements
process.XMLFromDBSource.label = cms.string("Extended")
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2017_realistic', '')

process.generator = cms.EDFilter("Pythia6GeneratorFilter",
	PythiaParameters = cms.PSet(
		parameterSets = cms.vstring('pythiaUESettings', 
			'processParameters'),
		processParameters = cms.vstring('MSEL=0         ! User defined processes', 
			'MSUB(11)=1     ! Min bias process', 
			'MSUB(12)=1     ! Min bias process', 
			'MSUB(13)=1     ! Min bias process', 
			'MSUB(28)=1     ! Min bias process', 
			'MSUB(53)=1     ! Min bias process', 
			'MSUB(68)=1     ! Min bias process', 
			'MSUB(92)=1     ! Min bias process, single diffractive', 
			'MSUB(93)=1     ! Min bias process, single diffractive', 
			'MSUB(94)=1     ! Min bias process, double diffractive', 
			'MSUB(95)=1     ! Min bias process'),
		pythiaUESettings = cms.vstring('MSTJ(11)=3     ! Choice of the fragmentation function', 
			'MSTJ(22)=2     ! Decay those unstable particles', 
			'PARJ(71)=10 .  ! for which ctau  10 mm', 
			'MSTP(2)=1      ! which order running alphaS', 
			'MSTP(33)=0     ! no K factors in hard cross sections', 
			'MSTP(51)=10042 ! structure function chosen (external PDF CTEQ6L1)', 
			'MSTP(52)=2     ! work with LHAPDF', 
			'MSTP(81)=1     ! multiple parton interactions 1 is Pythia default', 
			'MSTP(82)=4     ! Defines the multi-parton model', 
			'MSTU(21)=1     ! Check on possible errors during program execution', 
			'PARP(82)=1.8387   ! pt cutoff for multiparton interactions', 
			'PARP(89)=1960. ! sqrts for which PARP82 is set', 
			'PARP(83)=0.5   ! Multiple interactions: matter distrbn parameter', 
			'PARP(84)=0.4   ! Multiple interactions: matter distribution parameter', 
			'PARP(90)=0.16  ! Multiple interactions: rescaling power', 
			'PARP(67)=2.5    ! amount of initial-state radiation', 
			'PARP(85)=1.0  ! gluon prod. mechanism in MI', 
			'PARP(86)=1.0  ! gluon prod. mechanism in MI', 
			'PARP(62)=1.25   ! ', 
			'PARP(64)=0.2    ! ', 
			'MSTP(91)=1      !', 
			'PARP(91)=2.1   ! kt distribution', 
			'PARP(93)=15.0  ! ')
	),
	comEnergy = cms.double(10000.0),
	filterEfficiency = cms.untracked.double(1.0),
	maxEventsToPrint = cms.untracked.int32(0),
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	pythiaPylistVerbosity = cms.untracked.int32(0)
)


# Path and EndPath definitions


process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction)

# -----------------------------------------
# Ben

from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randSvc.populate()

# # # -- Trajectory producer
# process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
# process.TrackRefitter.src = 'generalTracks'
# process.TrackRefitter.NavigationSchool = ""

# # -- RecHit production
# process.load("RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi")


process.PixelTree = cms.EDAnalyzer(
	"PixelTree",
	verbose                      = cms.untracked.int32(1),
	rootFileName                 = cms.untracked.string('<output_root_file_name>'),
	phase                        = cms.untracked.int32(1),
	#type                         = cms.untracked.string(getDataset(process.source.fileNames[0])),
	globalTag                    = process.GlobalTag.globaltag,
	dumpAllEvents                = cms.untracked.int32(0),
	PrimaryVertexCollectionLabel = cms.untracked.InputTag('offlinePrimaryVertices'),
	muonCollectionLabel          = cms.untracked.InputTag('muons'),
	# trajectoryInputLabel         = cms.untracked.InputTag('TrackRefitter::Demo'),
	trajectoryInputLabel         = cms.untracked.InputTag('generalTracks'),
	trackCollectionLabel         = cms.untracked.InputTag('generalTracks'),
	pixelClusterLabel            = cms.untracked.InputTag('siPixelClusters'),
	pixelRecHitLabel             = cms.untracked.InputTag('siPixelRecHits'),
	HLTProcessName               = cms.untracked.string('HLT'), 
	L1GTReadoutRecordLabel       = cms.untracked.InputTag('gtDigis'), 
	hltL1GtObjectMap             = cms.untracked.InputTag('hltL1GtObjectMap'), 
	HLTResultsLabel              = cms.untracked.InputTag('TriggerResults::HLT'),
	# SimHits
	accessSimHitInfo             = cms.untracked.bool(True),
	associatePixel               = cms.bool(True),
	associateStrip               = cms.bool(False),
	associateRecoTracks          = cms.bool(False),
	pixelSimLinkSrc              = cms.InputTag("simSiPixelDigis"),
	ROUList                      = cms.vstring(
		'TrackerHitsPixelBarrelLowTof', 
		'TrackerHitsPixelBarrelHighTof', 
		'TrackerHitsPixelEndcapLowTof', 
		'TrackerHitsPixelEndcapHighTof'),
	associateHitbySimTrack       = cms.bool(False),
)
process.PixelTree_step = cms.Path( process.PixelTree)
process.schedule = cms.Schedule(process.generation_step,process.simulation_step,process.digitisation_step,process.L1simulation_step,process.digi2raw_step,process.raw2digi_step,process.reconstruction_step, process.PixelTree_step)

# -----------------------------------------

# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

# Customisation from command line