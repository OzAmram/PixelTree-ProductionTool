import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.categories.append('HLTrigReport')
process.MessageLogger.categories.append('L1GtTrigReport')
process.options = cms.untracked.PSet( SkipEvent = cms.untracked.vstring('ProductNotFound'), wantSummary = cms.untracked.bool(True) )


process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.load("CondCore.DBCommon.CondDBSetup_cfi")                                 
process.load("Configuration.StandardSequences.Services_cff")
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = '<global_tag>'

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
process.TrackRefitter.src = 'ctfWithMaterialTracksP5'
process.TrackRefitter.NavigationSchool = ""

# -- RecHit production
process.load("RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi")

process.PixelTree = cms.EDAnalyzer(
    "PixelTree",
    verbose                      = cms.untracked.int32(0),
    rootFileName                 = cms.untracked.string('<output_root_file_name>'),
    globalTag                    = process.GlobalTag.globaltag,
    dumpAllEvents                = cms.untracked.int32(0),
    PrimaryVertexCollectionLabel = cms.untracked.InputTag('offlinePrimaryVertices'),
    muonCollectionLabel          = cms.untracked.InputTag('muons'),
    trajectoryInputLabel         = cms.untracked.InputTag('TrackRefitter::Demo'),
    trackCollectionLabel         = cms.untracked.InputTag('splittedTracksP5'),
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

# -- Path
process.p = cms.Path(
  process.siPixelRecHits*
  process.TrackRefitter*
  process.PixelTree
)
