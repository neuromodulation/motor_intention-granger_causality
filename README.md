## Scripts for computing multivariate, state-space Granger causality.

Used in the manuscript: Köhler _et al._ (Pre-print). Dopamine and neuromodulation accelerate the neural dynamics of volitional action in Parkinson’s disease. DOI: [10.1101/2023.10.30.564700](https://doi.org/10.1101/2023.10.30.564700).

Relies on a modified version of the MNE-Connectivity package, available here: [github.com/neuromodulation/mne-connectivity_tsbinns](https://github.com/neuromodulation/mne-connectivity_tsbinns/tree/1.0.0)

### Use

1. Preprocessed data can be converted from an MNE `Epochs` object to the custom `Signal` object using the script [`epochs_to_signal.py`](https://github.com/tsbinns/coherence/blob/motor_intention-granger_causality/processing/epochs_to_signal.py).
2. Granger causality can be computed from the `Signal` objects using the scripts in the [`processing` folder](https://github.com/tsbinns/coherence/tree/motor_intention-granger_causality/processing), e.g. [`data_processing_granger_causality_preset_hpc.py`](https://github.com/tsbinns/coherence/blob/motor_intention-granger_causality/processing/data_processing_granger_causality_preset_hpc.py) and [`run_gc.sh`](https://github.com/tsbinns/coherence/blob/motor_intention-granger_causality/processing/run_gc.sh) for computing connectivity on a high performance cluster.
