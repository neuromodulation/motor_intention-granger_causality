"""Converts an MNE Epochs object to a Signal object."""


import os
import sys
from pathlib import Path

cd_path = Path(__file__).absolute().parent.parent
sys.path.append(os.path.join(cd_path, "coherence"))
from coh_handle_files import generate_sessionwise_fpath
from coh_handle_files import load_file
from coh_loading import load_preprocessed_epochs


### Info about the data to analyse
FOLDERPATH_PREPROCESSING = (
    "\\\\?\\C:\\Users\\tsbin\\Charité - Universitätsmedizin Berlin\\"
    "Interventional Cognitive Neuromodulation - PROJECT ECOG-LFP Coherence\\"
    "Analysis\\Preprocessing"
)
PRESET = "Richard_StimOffOn_Unpaired"
PREPROCESSING = "richard-epo"
EPOCHS_FTYPE = ".fif.gz"

N_BOOTSTRAPS = 50
N_EPOCHS_PER_BOOTSTRAP = 30
RANDOM_SEED = 44

if __name__ == "__main__":
    preset_fpath = (
        f"{FOLDERPATH_PREPROCESSING}\\Settings\\Generic\\Data File Presets\\"
        f"{PRESET}.json"
    )

    recordings = load_file(preset_fpath)

    for recording in recordings:
        DATASET = recording["cohort"]
        SUBJECT = recording["sub"]
        SESSION = recording["ses"]
        TASK = recording["task"]
        ACQUISITION = recording["acq"]
        RUN = recording["run"]

        if "Off" in SESSION:
            MED = "Off"
        elif "On" in SESSION:
            MED = "On"
        else:
            raise ValueError(
                "The medication state of the session cannot be identified"
            )

        if "Off" in ACQUISITION:
            STIM = "Off"
        elif "On" in ACQUISITION:
            STIM = "On"
        else:
            raise ValueError(
                "The medication state of the session cannot be identified"
            )

        extra_info = {
            "metadata": {
                "cohort": DATASET,
                "sub": SUBJECT,
                "med": MED,
                "stim": STIM,
                "ses": SESSION,
                "task": TASK,
                "run": RUN,
            }
        }

        preprocessed = load_preprocessed_epochs(
            folderpath_preprocessing=FOLDERPATH_PREPROCESSING,
            dataset=DATASET,
            preprocessing=PREPROCESSING,
            subject=SUBJECT,
            session=SESSION,
            task=TASK,
            acquisition=ACQUISITION,
            run=RUN,
            ftype=EPOCHS_FTYPE,
            processing_steps=None,
            extra_info=extra_info,
            epochs_as_windowed_data=False,
        )

        preprocessed.bootstrap(
            n_bootstraps=N_BOOTSTRAPS,
            n_epochs_per_bootstrap=N_EPOCHS_PER_BOOTSTRAP,
            random_seed=RANDOM_SEED,
        )

        preprocessed_data_fpath = generate_sessionwise_fpath(
            os.path.join(FOLDERPATH_PREPROCESSING, "Data"),
            DATASET,
            SUBJECT,
            SESSION,
            TASK,
            ACQUISITION,
            RUN,
            f"preprocessed-{PREPROCESSING}",
            ".pkl",
        )
        preprocessed.save_as_dict(
            preprocessed_data_fpath, ask_before_overwrite=False
        )
