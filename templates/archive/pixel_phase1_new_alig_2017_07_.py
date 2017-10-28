import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('RECO',eras.Run2_2017)

# -- Standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# -- Log reports
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.categories.append('HLTrigReport')
process.MessageLogger.categories.append('L1GtTrigReport')
process.options = cms.untracked.PSet( SkipEvent = cms.untracked.vstring('ProductNotFound'), wantSummary = cms.untracked.bool(True) )

# -- Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation  = cms.untracked.string('RECO nevts:10'),
    name        = cms.untracked.string('Applications'),
    version     = cms.untracked.string('$Revision: 1.19 $')
)

# -- Global tag
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '<global_tag>', '')

# -- Input files
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
    '<source_root_file_name>'
    )
)

# -- number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(<number_of_events>)
    )

# -- Trajectory producer
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.TrackRefitter.src = 'generalTracks'
process.TrackRefitter.NavigationSchool = ""


# -- New alignment
process.GlobalTag.toGet = cms.VPSet(
    cms.PSet(record = cms.string('TrackerAlignmentRcd'),
             tag = cms.string('TrackerAlignment_StartUp17_v8'),
             connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")),
    cms.PSet(record = cms.string('TrackerSurfaceDeformationRcd'),
             tag = cms.string('TrackerSurfaceDeformations_StartUp17_v8'),
             connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")),
    cms.PSet(record = cms.string('TrackerAlignmentErrorExtendedRcd'),
             tag = cms.string('TrackerAlignmentExtendedErrors_StartUp17_v4'),
             connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"))   
)

# -- RecHit production
process.load("RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi")

process.PixelFilter = cms.EDFilter("TriggerResultsFilter",
    triggerConditions = cms.vstring('HLT_ZeroBias_*/1'),
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
    globalTag                    = process.GlobalTag.globaltag,
    dumpAllEvents                = cms.untracked.int32(0),
    PrimaryVertexCollectionLabel = cms.untracked.InputTag('offlinePrimaryVertices'),
    muonCollectionLabel          = cms.untracked.InputTag('muons'),
    trajectoryInputLabel         = cms.untracked.InputTag('TrackRefitter::RECO'),
    trackCollectionLabel         = cms.untracked.InputTag('generalTracks'),
    pixelClusterLabel            = cms.untracked.InputTag('siPixelClusters'),
    pixelRecHitLabel             = cms.untracked.InputTag('siPixelRecHits'),
    HLTProcessName               = cms.untracked.string('HLT'),
    L1GTReadoutRecordLabel       = cms.untracked.InputTag('gtDigis'),
    hltL1GtObjectMap             = cms.untracked.InputTag('hltL1GtObjectMap'),
    HLTResultsLabel              = cms.untracked.InputTag('TriggerResults::HLT'),
    associatePixel               = cms.bool(False),
    associateStrip               = cms.bool(False),
    associateRecoTracks          = cms.bool(False),
    ROUList                      = cms.vstring(
      'TrackerHitsPixelBarrelLowTof', 
      'TrackerHitsPixelBarrelHighTof', 
      'TrackerHitsPixelEndcapLowTof', 
      'TrackerHitsPixelEndcapHighTof'),
    )

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.PixelTree_step = cms.Path(process.PixelFilter*process.siPixelRecHits*process.TrackRefitter*process.PixelTree)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.PixelTree_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

# process.schedule.remove(process.PixelTree_step)
process.schedule.remove(process.endjob_step)
