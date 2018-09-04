#include <stdlib.h> 
#include <algorithm>
#include <stdio.h>
#include <string.h>
#include <stddef.h>
#include <math.h>
#include <vector>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>
#include "TFile.h"
#include "TTree.h"

bool isMatched(float lx, float ly, float l1x, float l1y){
    return abs(lx -l1x) < 0.005 && abs(ly - l1y) < 0.005;
}


int main(int argc, char **argv){
    if(argc !=4){
        printf("takes 3 command line arguments PixelTree file, log file, and output filename \n");
        exit(1);
    }
    char* pTreeFile_name = argv[1];
    char* logFile_name = argv[2];
    char* outFile_name = argv[3];
    FILE *logFile = fopen(logFile_name, "r");
    if (logFile==NULL) {
        printf("can't find %s\n",logFile_name);
        return 1;
    }
    TFile *f_pTree = TFile::Open(pTreeFile_name);
    TTree *pTree = (TTree *)f_pTree->Get("pixelTree");

    Float_t ClRhLx[1000], ClRhLy[1000], ClSimTrEta[1000][10], ClSimHitLx[1000][10], ClSimHitLy[1000][10],
            TkEta[1000], TkPhi[1000], TkPt[1000];
    Int_t ClRhIsOnEdge[1000], ClN, ClSimHitN[1000], ClType[1000], event, ClDetId[1000], ClSizeX[1000], ClSizeY[1000];

    pTree->SetBranchAddress("event", &event);
    pTree->SetBranchAddress("ClN", &ClN);
    pTree->SetBranchAddress("ClSimHitN", &ClSimHitN);
    pTree->SetBranchAddress("ClType", &ClType);
    pTree->SetBranchAddress("ClSizeX", &ClSizeX);
    pTree->SetBranchAddress("ClSizeY", &ClSizeY);
    pTree->SetBranchAddress("ClRhIsOnEdge", &ClRhIsOnEdge);
    pTree->SetBranchAddress("ClRhLx", &ClRhLx);
    pTree->SetBranchAddress("ClRhLy", &ClRhLy);
    pTree->SetBranchAddress("ClSimHitLx", &ClSimHitLx);
    pTree->SetBranchAddress("ClSimHitLy", &ClSimHitLy);
    pTree->SetBranchAddress("TkEta", &TkEta);
    pTree->SetBranchAddress("TkPhi", &TkPhi);
    pTree->SetBranchAddress("TkPt", &TkPt);
    pTree->SetBranchAddress("ClDetId", &ClDetId);
    Long64_t pTree_size  =  pTree->GetEntries();
    pTree->GetEntry(0);
    int pTree_idx = 0;

    Int_t detID, onEdge, type, failType, used2D, tempID, spans2ROCs;
    Float_t SimHitLx, SimHitLy, CRLx, CRLy, GenericLx, GenericLy, ClsizeX, ClsizeY, TrackEta, TrackPhi, TrackPt, proby1d, nydiff;

    TFile *f_out = TFile::Open(outFile_name, "recreate");
    TTree *t_out = new TTree("pixelTree_plus", "Pixel Tree and dead pixel info");
    t_out->Branch("event", &event);
    t_out->Branch("failType", &failType);
    t_out->Branch("used2D", &used2D);
    t_out->Branch("ClSizeX", &ClsizeX);
    t_out->Branch("ClSizeY", &ClsizeY);
    t_out->Branch("SimHitLx", &SimHitLx);
    t_out->Branch("SimHitLy", &SimHitLy);
    t_out->Branch("GenericLx", &GenericLx);
    t_out->Branch("GenericLy", &GenericLy);
    t_out->Branch("TrackEta", &TrackEta);
    t_out->Branch("TrackPhi", &TrackPhi);
    t_out->Branch("TrackPt", &TrackPt);
    t_out->Branch("CRLx", &CRLx);
    t_out->Branch("CRLy", &CRLy);
    t_out->Branch("onEdge", &onEdge);
    t_out->Branch("detID", &detID);
    t_out->Branch("type", &type);
    t_out->Branch("nydiff", &nydiff);
    t_out->Branch("proby1d", &proby1d);

    char log_line[300];
    int roc_num;
    float percent;

    char detid_last[30];

    strcpy(detid_last, "\0");
    bool wrote_out = false;
    char * key = "123CRTEST456";
    int nMatched = 0;
    int nFail=0;
    int nDuplicates=0;
    std::vector<float> prev_hits;


    /*
    for(int j=0; j<pTree_size; j++){
        pTree->GetEntry(j);
        for(int i=0; i<ClN; i++){
            printf("Event %i Hit %i Pixel Tree Lx Ly = %.4f %.4f \n",j, i, ClRhLx[i], ClRhLy[i]);
        }
    }
    */

    int last_match_event=0;


    while (fgets(log_line, 300, logFile)) {
        //check if line starts with key
        if(strncmp(log_line, key, strlen(key)) == 0){
            //parse info
            fgets(log_line, 100, logFile);
            sscanf(log_line, "nydiff=%f proby1d=%f \n", &nydiff, &proby1d);
            printf("log_line = %s \nproby1d=%.2e \n", log_line, proby1d);
            fgets(log_line, 100, logFile);
            sscanf(log_line, "fail_mode=%i, on_edge=%i, used_2d=%i, spans_two_ROCs=%i, detID=%i \n", 
                    &failType, &onEdge, &used2D, &spans2ROCs, &tempID);

            //get next line and parse (final position, used to match to pixel
            //trees)
            fgets(log_line, 100, logFile);
            Float_t lx, ly;
            sscanf(log_line, "Local X, Local Y = %f, %f \n", &lx, &ly); 

            //get next two lines which have generic and CR positions
            fgets(log_line, 100, logFile);
            sscanf(log_line, "1D: X,Y = %f, %f", &GenericLx, &GenericLy); 
            fgets(log_line, 100, logFile);
            sscanf(log_line, "CR: X,Y = %f, %f", &CRLx, &CRLy); 
            if(std::find(prev_hits.begin(), prev_hits.end(), lx*ly) == prev_hits.end()){
                prev_hits.push_back(lx*ly);
            }
            else{
                nDuplicates++;
                continue;
            }

            int match_idx =-1;
            //Tries to match all events
            for(int nTry=0; nTry < pTree_size; nTry++){
                pTree_idx = (last_match_event + nTry) % pTree_size;

                bool found_match = false;
                pTree->GetEntry(pTree_idx);
                for(int i=0; i<ClN; i++){
                    if(isMatched(lx, ly, ClRhLx[i], ClRhLy[i])){
                        found_match = true;
                        match_idx = i;
                        last_match_event = pTree_idx;
                        //printf("Found Event %i Pixel Tree Lx Ly = %.4f %.4f \n", pTree_idx, ClRhLx[i], ClRhLy[i]);
                        break;
                    }
                }
                if(found_match) break;
            }

            //Version that tries to match to current event and next one only to
            //save time (seems to perform worse)
            //try to match hit to pixel tree
            /*
            int i=0;
            pTree->GetEntry(pTree_idx);
            for(i=0; i<ClN; i++){
                //printf("Event %i Pixel Tree Lx Ly = %.4f %.4f \n", pTree_idx, ClRhLx[i], ClRhLy[i]);
                if(isMatched(lx, ly, ClRhLx[i], ClRhLy[i])){
                    match_idx = i;
                    break;
                }

            }
            
            if(match_idx <0 && pTree_idx < pTree_size){
                //we didn't match in this event, try next one
                pTree_idx++;
                pTree->GetEntry(pTree_idx);
                for(i=0; i<ClN; i++){
                    //printf("Event %i Pixel Tree Lx Ly = %.4f %.4f \n", pTree_idx, ClRhLx[i], ClRhLy[i]);
                    if(isMatched(lx, ly, ClRhLx[i], ClRhLy[i])){
                        match_idx = i;
                        break;
                    }
                }
            }
            */
            if(match_idx < 0){
                //we still can't match. Something went wrong
                printf("Unable to match hit Lx, Ly = %.4f %.4f \n Likely in event %i or %i \n", lx,ly, pTree_idx -1 , pTree_idx);
                //go back 1 event to make sure
                pTree_idx--;
                pTree->GetEntry(pTree_idx);
                nFail++;
                continue;
            }
            //printf("found in event %i \n", pTree_idx);
            
            //
            //used matched pixeltree hit 
            if(match_idx >=0){
                ClsizeX = ClSizeX[match_idx];
                ClsizeY = ClSizeY[match_idx];
                SimHitLx = ClSimHitLx[match_idx][0];
                SimHitLy = ClSimHitLy[match_idx][0];
                detID = ClDetId[match_idx];
                type = ClType[match_idx];
                TrackEta = TkEta[match_idx];
                TrackPhi = TkPhi[match_idx];
                TrackPt = TkPt[match_idx];
                nMatched++;

                t_out->Fill();
            }
        }
    }
    printf("Exiting sucessfully, matched %i hits and failed on %i hits %i Duplicates \n", nMatched, nFail, nDuplicates);
    f_out->cd();
    t_out->Write();
    f_out->Close();
    return 0;
}




 





