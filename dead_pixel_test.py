

# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step3 --conditions 101X_upgrade2018_realistic_Candidate_2018_03_15_16_26_46 -n 10 --era Run2_2017 --eventcontent RECOSIM,MINIAODSIM,DQM --runUnscheduled -s RAW2DIGI,L1Reco,RECO,RECOSIM,EI,PAT,VALIDATION:@standardValidation+@miniAODValidation,DQM:@standardDQM+@ExtraHLT+@miniAODDQM --datatier GEN-SIM-RECO,MINIAODSIM,DQMIO --geometry DB:Extended --filein file:step2_DIGI_L1_DIGI2RAW_HLT.root --no_exec
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
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.RecoSim_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.PATMC_cff')
process.load('Configuration.StandardSequences.Validation_cff')
process.load('DQMOffline.Configuration.DQMOfflineMC_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('CalibTracker.SiPixelESProducers.SiPixel2DTemplateDBObjectESProducer_cfi')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(20)
)

# Input source
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring('/store/user/cmantill/RelValTTbarLepton_13/crab_step2RelValTTbarLepton_13/180402_221739/0000/step2_DIGI_L1_DIGI2RAW_HLT_5.root'),
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# -----------------------------------------
# Ben

from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randSvc = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randSvc.populate()

# # # -- Trajectory producer
process.load("RecoTracker.TrackProducer.TrackRefitters_cff")
process.TrackRefitter.src = 'generalTracks'
process.TrackRefitter.NavigationSchool = ""

# # -- RecHit production
process.load("RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi")

process.PixelTree = cms.EDAnalyzer(
        "PixelTree",
        verbose                      = cms.untracked.int32(10),
        rootFileName                 = cms.untracked.string('PixelTree_2_10.root'),
        phase                        = cms.untracked.int32(1),
        #type                         = cms.untracked.string(getDataset(process.source.fileNames[0])),                                                                                                                                                                          
        globalTag                    = process.GlobalTag.globaltag,
        dumpAllEvents                = cms.untracked.int32(0),
        PrimaryVertexCollectionLabel = cms.untracked.InputTag('offlinePrimaryVertices'),
        muonCollectionLabel          = cms.untracked.InputTag('muons'),
        trajectoryInputLabel         = cms.untracked.InputTag('TrackRefitter::RECO'),
        TTRHBuilder                  = cms.string('WithAngleAndTemplate'),
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



# Other statements
process.mix.playback = True
process.mix.digitizers = cms.PSet()
for a in process.aliases: delattr(process, a)
process.RandomNumberGeneratorService.restoreStateLabel=cms.untracked.string("randomEngineStateProducer")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '102X_upgrade2018_realistic_v9', '')

process.GlobalTag.toGet = cms.VPSet(
    cms.PSet(record = cms.string('SiPixelQualityFromDbRcd'),
        tag = cms.string('SiPixelQuality_ideal'),
        connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS"),
    ),
) 


# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)

process.PixelTree_step = cms.Path(process.siPixelRecHits*process.TrackRefitter*process.PixelTree)
process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step, process.PixelTree_step)
