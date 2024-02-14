"""Processes ECoG and LFP data to generate Granger causality values."""


import os
import sys
from pathlib import Path

cd_path = Path(__file__).absolute().parent.parent
sys.path.append(os.path.join(cd_path, "coherence"))
from coh_connectivity_processing import granger_processing
from coh_loading import load_preprocessed_dict


### Info about the data to analyse
FOLDERPATH_PREPROCESSING = (
    "\\\\?\\C:\\Users\\tsbin\\OneDrive - Charité - "
    "Universitätsmedizin Berlin\\PROJECT ECOG-LFP Coherence\\Analysis\\"
    "Preprocessing"
)
FOLDERPATH_PROCESSING = (
    "\\\\?\\C:\\Users\\tsbin\\OneDrive - Charité - "
    "Universitätsmedizin Berlin\\PROJECT ECOG-LFP Coherence\\Analysis\\"
    "Processing"
)
DATASET = "BIDS_01_Berlin_Neurophys"
PREPROCESSING = "preprocessed-med_analysis-for_connectivity"
ANALYSIS = "con_granger_richard"
SUBJECT = "EL002"
SESSION = "EcogLfpMedOff03"
TASK = "SelfPacedRotationR"
ACQUISITION = "StimOff"
RUN = "1"

if __name__ == "__main__":
    preprocessing_analysis = PREPROCESSING[
        PREPROCESSING.index("-")
        + 1 : len(PREPROCESSING)
        - PREPROCESSING[::-1].index("-")
        - 1
    ]

    preprocessed = load_preprocessed_dict(
        folderpath_preprocessing=FOLDERPATH_PREPROCESSING,
        dataset=DATASET,
        preprocessing=PREPROCESSING,
        subject=SUBJECT,
        session=SESSION,
        task=TASK,
        acquisition=ACQUISITION,
        run=RUN,
        ftype=".pkl",
    )

    granger_processing(
        preprocessed,
        FOLDERPATH_PROCESSING,
        DATASET,
        preprocessing_analysis,
        ANALYSIS,
        SUBJECT,
        SESSION,
        TASK,
        ACQUISITION,
        RUN,
        verbose=True,
        save=True,
    )
