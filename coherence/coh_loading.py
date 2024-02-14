"""Methods for loading files and handling the resulting objects."""

import os
from typing import Union
from mne import read_epochs
from coh_handle_files import generate_sessionwise_fpath, load_file
from coh_signal import data_dict_to_signal, Signal


def load_preprocessed_dict(
    folderpath_preprocessing: str,
    dataset: str,
    preprocessing: str,
    subject: str,
    session: str,
    task: str,
    acquisition: str,
    run: str,
    ftype: str,
) -> Signal:
    """Loads preprocessed data saved as a dictionary and converts it to a Signal
    object.

    PARAMETERS
    ----------
    folderpath_preprocessing : str
    -   Path to the preprocessing folder where the data and settings are found.

    dataset : str
    -   Name of the dataset to analyse.

    preprocessing : str
    -   Name of the preprocessing type to analyse.

    subject : str
    -   Name of the subject to analyse.

    session : str
    -   Name of the session to analyse.

    task : str
    -   Name of the task to analyse.

    acquisition : str
    -   Name of the acquisition to analyse.

    run : str
    -   Name of the run to analyse.

    ftype : str
    -   Filetype of the file.

    RETURNS
    -------
    signal : Signal
    -   The preprocessed data converted from a dictionary to a Signal object.
    """

    fpath = generate_sessionwise_fpath(
        folderpath=os.path.join(folderpath_preprocessing, "Data"),
        dataset=dataset,
        subject=subject,
        session=session,
        task=task,
        acquisition=acquisition,
        run=run,
        group_type=preprocessing,
        filetype=ftype,
    )

    data_dict = load_file(fpath=fpath)
    signal = data_dict_to_signal(data=data_dict)

    return signal


def load_preprocessed_epochs(
    folderpath_preprocessing: str,
    dataset: str,
    preprocessing: str,
    subject: str,
    session: str,
    task: str,
    acquisition: str,
    run: str,
    ftype: str,
    processing_steps: Union[dict, None] = None,
    extra_info: Union[dict, None] = None,
    epochs_as_windowed_data: bool = False,
) -> Signal:
    """Loads preprocessed data saved as an MNE epochs object and converts it to
    a Signal object.

    PARAMETERS
    ----------
    folderpath_preprocessing : str
    -   Path to the preprocessing folder where the data and settings are found.

    dataset : str
    -   Name of the dataset to analyse.

    preprocessing : str
    -   Name of the preprocessing type to analyse.

    subject : str
    -   Name of the subject to analyse.

    session : str
    -   Name of the session to analyse.

    task : str
    -   Name of the task to analyse.

    acquisition : str
    -   Name of the acquisition to analyse.

    run : str
    -   Name of the run to analyse.

    ftype : str
    -   Name of the filetype in which the epochs data is saved, with a leading
        period, e.g. ".fif".

    processing_steps : dict | None; default None
    -   Information about the processing that has been applied to the data.

    extra_info : dict | None; default None
    -   Additional information about the data not included in the MNE objects.

    epochs_as_windowed_data : bool; default False
    -   Whether or not the epochs should be placed into a window when loaded
        into the Signal object. If False, data will have dimensions [epochs x
        channels x timepoints]. If True, data will have dimensions [windows x
        epochs x channels x timepoints].

    RETURNS
    -------
    signal : Signal
    -   The preprocessed data converted from an MNE epochs object to a Signal
        object.
    """

    fpath = generate_sessionwise_fpath(
        folderpath=os.path.join(folderpath_preprocessing, "Data"),
        dataset=dataset,
        subject=subject,
        session=session,
        task=task,
        acquisition=acquisition,
        run=run,
        group_type=preprocessing,
        filetype=ftype,
    )

    epochs = read_epochs(fpath)

    ch_subregions = {
        "EL002": ["Parietal", "Parietal", "Sensory", "Sensorimotor"],
        "EL003": ["Parietal", "Sensory", "Sensorimotor", "Motor", "Motor"],
        "EL004": [
            "Parietal",
            "Parietal",
            "Sensory",
            "Sensory",
            "Motor",
        ],
        "EL005": ["Parietal", "Parietal", "Sensory", "Sensorimotor", "Motor"],
        "EL006": ["Sensory", "Sensorimotor", "Motor", "Motor", "Prefrontal"],
        "EL007": ["Sensory", "Sensory", "Sensorimotor", "Motor", "Motor"],
        "EL008": ["Parietal", "Sensory", "Sensory", "Sensorimotor", "Motor"],
        "EL009": ["Sensorimotor", "Motor", "Motor", "Motor", "Prefrontal"],
        "EL010": ["Sensory", "Sensory", "Sensorimotor", "Motor"],
        "EL011": ["Parietal", "Parietal", "Sensory", "Sensorimotor", "Motor"],
        "EL012": ["Motor", "Motor", "Prefrontal", "Prefrontal"],
        "EL013": ["Sensory", "Sensory", "Sensorimotor", "Motor", "Prefrontal"],
        "EL014": ["Parietal", "Parietal", "Sensory", "Sensorimotor", "Motor"],
        "EL015": ["Parietal", "Sensory", "Sensory", "Sensorimotor", "Motor"],
        "EL016": ["Parietal", "Parietal", "Sensory", "Sensorimotor", "Motor"],
        "EL017": ["Parietal", "Parietal", "Sensory", "Sensorimotor", "Motor"],
        "FOG006": [
            "Sensory",
            "Sensory",
            "Sensorimotor",
            "Motor",
            "Prefrontal",
            "Prefrontal",
            "Prefrontal",
        ],
        "FOG008": [
            "Sensory",
            "Sensorimotor",
            "Motor",
            "Motor",
            "Prefrontal",
            "Prefrontal",
            "Prefrontal",
        ],
        "FOG010": [
            "Sensorimotor",
            "Motor",
            "Motor",
            "Prefrontal",
            "Prefrontal",
            "Prefrontal",
            "Prefrontal",
        ],
        "FOG012": [
            "Parietal",
            "Parietal",
            "Sensory",
            "Sensory",
            "Sensorimotor",
            "Motor",
            "Prefrontal",
        ],
        "FOG014": [
            "Parietal",
            "Sensory",
            "Sensory",
            "Sensorimotor",
            "Motor",
            "Prefrontal",
            "Prefrontal",
        ],
        "FOG016": [
            "Parietal",
            "Sensory",
            "Sensorimotor",
            "Motor",
            "Motor",
            "Prefrontal",
            "Prefrontal",
        ],
        "FOG021": [
            "Parietal",
            "Parietal",
            "Parietal",
            "Sensory",
            "Sensorimotor",
            "Motor",
            "Motor",
        ],
        "FOG022": [
            "Parietal",
            "Parietal",
            "Sensory",
            "Sensory",
            "Sensorimotor",
            "Motor",
            "Motor",
        ],
        "FOGC001": [
            "Parietal",
            "Sensory",
            "Sensorimotor",
            "Motor",
            "Motor",
            "Prefrontal",
            "Prefrontal",
        ],
    }
    import numpy as np

    n_ecog = len([name for name in epochs.ch_names if "ECOG" in name])
    n_lfp = len([name for name in epochs.ch_names if "LFP" in name])
    assert n_ecog == len(ch_subregions[subject])
    assert np.all(["ECOG" in name for name in epochs.ch_names[:n_ecog]])

    if epochs_as_windowed_data:
        epochs = [epochs]

    ch_subregions = [
        *ch_subregions[subject],
        *["all" for _ in range(n_lfp)],
    ]

    extra_info["ch_subregions"] = {
        name: subregion
        for name, subregion in zip(epochs.ch_names, ch_subregions)
    }

    signal = Signal()
    signal.data_from_objects(epochs, processing_steps, extra_info)

    return signal
