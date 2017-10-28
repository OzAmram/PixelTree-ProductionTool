import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.categories.append('HLTrigReport')
process.MessageLogger.categories.append('L1GtTrigReport')
process.options = cms.untracked.PSet( SkipEvent = cms.untracked.vstring('ProductNotFound'), wantSummary = cms.untracked.bool(True) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = '<global_tag>'

# -- Database configuration
process.load("CondCore.DBCommon.CondDBCommon_cfi")
process.load("CondCore.DBCommon.CondDBSetup_cfi")

# -- Conditions
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("RecoVertex.BeamSpotProducer.BeamSpot_cfi")

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

# -- RecHit production
process.load("RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi")

# -- skimming
# process.superPointingFilter = cms.EDFilter(
#     "HLTMuonPointingFilter",
#     SALabel = cms.string("generalTracks"),
#     PropagatorName = cms.string("SteppingHelixPropagatorAny"),
#     radius = cms.double(10.0),
#     maxZ = cms.double(50.0)
#     )

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
    globalTag                    = process.GlobalTag.globaltag,
    dumpAllEvents                = cms.untracked.int32(0),
    PrimaryVertexCollectionLabel = cms.untracked.InputTag('offlinePrimaryVertices'),
    muonCollectionLabel          = cms.untracked.InputTag('muons'),
    trajectoryInputLabel         = cms.untracked.InputTag('TrackRefitter::Demo'),
    trackCollectionLabel         = cms.untracked.InputTag('generalTracks'),
    pixelClusterLabel            = cms.untracked.InputTag('siPixelClusters'),
    pixelRecHitLabel             = cms.untracked.InputTag('siPixelRecHits'),
    HLTProcessName               = cms.untracked.string('HLT'),
    L1GTReadoutRecordLabel       = cms.untracked.InputTag('gtDigis'),
    hltL1GtObjectMap             = cms.untracked.InputTag('hltL1GtObjectMap'),
    HLTResultsLabel              = cms.untracked.InputTag('TriggerResults::HLT')
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
#    process.superPointingFilter*
    process.PixelFilter*
    process.siPixelRecHits*
    process.TrackRefitter*
    process.PixelTree
    )

#process.TrackerDigiGeometryESModule.applyAlignment = True