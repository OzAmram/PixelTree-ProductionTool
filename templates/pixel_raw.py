# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: --step=RAW2DIGI,RECO --data --scenario=pp --conditions=auto:run2_data --python_filename=test.py --filein=/store/data/Run2016D/ZeroBias/RAW/v2/000/276/811/00000/14FC42EC-0A4B-E611-89FE-02163E011937.root --fileout=test.root --number=4 --era=Run2_25ns --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RECO',eras.Run2_25ns)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
# Ben
process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.options = cms.untracked.PSet( SkipEvent = cms.untracked.vstring('ProductNotFound'), wantSummary = cms.untracked.bool(True) )


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(<number_of_events>)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('<source_root_file_name>'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--step=RAW2DIGI,RECO nevts:4'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction)

# --------------------------------------------------------------------
# ---------------------------- Ben -----------------------------------
# Additional output definition
process.GlobalTag.globaltag = '<global_tag>'

# Trajectory producer
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.TrackRefitter.src = 'generalTracks'
process.TrackRefitter.NavigationSchool = ""

# RecHit production
process.load("RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi")

process.PixelFilter = cms.EDFilter("TriggerResultsFilter",
    triggerConditions = cms.vstring('HLT_ZeroBias_v*/1'),
    hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
    l1tResults = cms.InputTag( "" ),
    daqPartitions = cms.uint32( 1 ),
    l1tIgnoreMask = cms.bool( False ),
    l1techIgnorePrescales = cms.bool( True ),
    throw = cms.bool( True )
)

process.PixelTree = cms.EDAnalyzer(
    "PixelTree",
    verbose                      = cms.untracked.int32(0),
    rootFileName                 = cms.untracked.string('<output_root_file_name>'),
    #type                         = cms.untracked.string(getDataset(process.source.fileNames[0])),
    globalTag                    = process.GlobalTag.globaltag,
    dumpAllEvents                = cms.untracked.int32(0),
    PrimaryVertexCollectionLabel = cms.untracked.InputTag('offlinePrimaryVertices'),
    muonCollectionLabel          = cms.untracked.InputTag('muons'),
    trajectoryInputLabel         = cms.untracked.InputTag('TrackRefitter'),    
    trackCollectionLabel         = cms.untracked.InputTag('generalTracks'),
    pixelClusterLabel            = cms.untracked.InputTag('siPixelClusters'),
    pixelRecHitLabel             = cms.untracked.InputTag('siPixelRecHits'),
    HLTProcessName               = cms.untracked.string('HLT'),
    L1GTReadoutRecordLabel       = cms.untracked.InputTag('gtDigis'),
    hltL1GtObjectMap             = cms.untracked.InputTag('hltL1GtObjectMap'),
    HLTResultsLabel              = cms.untracked.InputTag('TriggerResults::HLT')
    )

process.PixelTree_step = cms.Path(process.PixelFilter*process.siPixelRecHits*process.TrackRefitter*process.PixelTree)

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step, process.PixelTree_step)
