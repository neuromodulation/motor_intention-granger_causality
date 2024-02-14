"""Processes ECoG and LFP data to generate Granger causality values."""


import os
import sys
from pathlib import Path

cd_path = Path(__file__).absolute().parent.parent
sys.path.append(os.path.join(cd_path, "coherence"))
from coh_connectivity_processing import granger_processing
from coh_handle_files import load_file
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
PRESET = "Richard_StimOffOn_Unpaired"
PREPROCESSING = "preprocessed-richard-epo"
ANALYSIS = "con_granger_richard"

if __name__ == "__main__":
    preset_fpath = (
        f"{FOLDERPATH_PROCESSING}\\Settings\\Generic\\Data File Presets\\"
        f"{PRESET}.json"
    )
    recordings = load_file(preset_fpath)

    preprocessing_analysis = PREPROCESSING[
        PREPROCESSING.index("-")
        + 1 : len(PREPROCESSING)
        - PREPROCESSING[::-1].index("-")
        - 1
    ]

    for recording in recordings:
        DATASET = recording["cohort"]
        SUBJECT = recording["sub"]
        SESSION = recording["ses"]
        TASK = recording["task"]
        ACQUISITION = recording["acq"]
        RUN = recording["run"]

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
            save=True,
        )
