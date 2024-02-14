"""Classes for calculating connectivity between signals."""

from typing import Union
from numpy.typing import NDArray
import numpy as np

from coh_exceptions import ProcessingOrderError
from coh_connectivity_processing_methods import ProcMultivariateConnectivity
import coh_signal


class ConnectivityGranger(ProcMultivariateConnectivity):
    """Calculates multivariate spectral Granger causality between signals.

    PARAMETERS
    ----------
    signal : coh_signal.Signal
    -   The preprocessed data to analyse.

    verbose : bool; default True
    -   Whether or not to print information about the information processing.

    METHODS
    -------
    process
    -   Performs granger causality analysis.

    save_object
    -   Saves the object as a .pkl file.

    save_results
    -   Saves the results and additional information as a file.

    results_as_dict
    -   Returns the results and additional information as a dictionary.

    get_results
    -   Extracts and returns results.
    """

    def __init__(
        self, signal: coh_signal.Signal, verbose: bool = True
    ) -> None:
        super().__init__(signal, verbose)
        super()._sort_inputs()

        self.con_methods = ["gc", "net_gc", "trgc", "net_trgc"]

    def process(
        self,
        power_method: str,
        seeds: Union[str, list[str], dict],
        targets: Union[str, list[str], dict],
        fmin: Union[Union[float, tuple], None] = None,
        fmax: Union[float, tuple] = np.inf,
        fskip: int = 0,
        faverage: bool = False,
        tmin: Union[float, None] = None,
        tmax: Union[float, None] = None,
        mt_bandwidth: Union[float, None] = None,
        mt_adaptive: bool = False,
        mt_low_bias: bool = True,
        cwt_freqs: Union[NDArray, None] = None,
        cwt_n_cycles: Union[float, NDArray] = 7.0,
        n_components: Union[list[int], str] = "rank",
        n_lags: int = 20,
        average_windows: bool = False,
        average_timepoints: bool = False,
        block_size: int = 1000,
        n_jobs: int = 1,
    ):
        """Performs the Granger casuality (GC) analysis on the data, computing
        GC, net GC, time-reversed GC, and net time-reversed GC.

        PARAMETERS
        ----------
        power_method : str
        -   The spectral method for computing the cross-spectral density.
        -   Supported inputs are: "multitaper"; "fourier"; and "cwt_morlet".

        seeds : str | list[str] | dict
        -   The channels to use as seeds for the connectivity analysis.
            Connectivity is calculated from each seed to each target.
        -   If a string, can either be a single channel name, or a single
            channel type. In the latter case, the channel type should be
            preceded by 'type_', e.g. 'type_ecog'. In this case, channels
            belonging to each type with different epoch orders and
            rereferencing types will be handled separately.
        -   If a list of strings, each entry of the list should be a channel
            name.

        targets : str | list[str] | dict
        -   The channels to use as targets for the connectivity analysis.
            Connectivity is calculated from each seed to each target.
        -   If a string, can either be a single channel name, or a single
            channel type. In the latter case, the channel type should be
            preceded by 'type_', e.g. 'type_ecog'. In this case, channels
            belonging to each type with different epoch orders and
            rereferencing types will be handled separately.
        -   If a list of strings, each entry of the list should be a channel
            name.

        n_lags : int; default 20
        -   The number of lags to use when computing autocovariance. Currently,
            only positive-valued integers are supported.

        tmin : float | None; default None
        -   Time to start the connectivity estimation.
        -   If None, the data is used from the beginning.

        tmax : float | None; default None
        -   Time to end the connectivity estimation.
        -   If None, the data is used until the end.

        average_windows : bool; default True
        -   Whether or not to average connectivity results across windows.

        ensure_full_rank_data : bool; default True
        -   Whether or not to make sure that the data being processed has full
            rank by performing a singular value decomposition on the data of
            the seeds and targets and taking only the first n components, where
            n is equal to number of non-zero singluar values in the
            decomposition (i.e. the rank of the data).
        -   If this is not performed, errors can arise when computing Granger
            causality as assumptions of the method are violated.

        n_jobs : int; default 1
        -   The number of epochs to calculate connectivity for in parallel.

        cwt_freqs : list[int | float] | None; default None
        -   The frequencies of interest, in Hz.
        -   Only used if 'cs_method' is "cwt_morlet", in which case 'freqs'
            cannot be 'None'.

        cwt_n_cycles: int | float | array[int | float]; default 7
        -   The number of cycles to use when calculating connectivity.
        -   If an single integer or float, this number of cycles is for each
            frequency.
        -   If an array, the entries correspond to the number of cycles to use
            for each frequency being analysed.
        -   Only used if 'cs_method' is "cwt_morlet".

        cwt_use_fft : bool; default True
        -   Whether or not FFT-based convolution is used to compute the wavelet
            transform.
        -   Only used if 'cs_method' is "cwt_morlet".

        cwt_decim : int | slice; default 1
        -   Decimation factor to use during time-frequency decomposition to
            reduce memory usage. If 1, no decimation is performed.

        mt_bandwidth : float | None; default None
        -   The bandwidth, in Hz, of the multitaper windowing function.
        -   Only used if 'cs_method' is "multitaper".

        mt_adaptive : bool; default False
        -   Whether or not to use adaptive weights to comine the tapered
            spectra into power spectra.
        -   Only used if 'cs_method' is "multitaper".

        mt_low_bias : bool: default True
        -   Whether or not to only use tapers with > 90% spectral concentration
            within bandwidth.
        -   Only used if 'cs_method' is "multitaper".

        fmt_fmin : int | float; default 0
        -   The lower frequency of interest.
        -   If a float, this frequency is used.
        -   If a tuple, multiple bands are defined, with each entry being the
            lower frequency for that band. E.g. (8., 20.) would give two bands
            using 8 Hz and 20 Hz, respectively, as their lower frequencies.
        -   Only used if 'cs_method' is "fourier" or "multitaper".

        fmt_fmax : int | float; default infinity
        -   The higher frequency of interest.
        -   If a float, this frequency is used.
        -   If a tuple, multiple bands are defined, with each entry being the
            higher frequency for that band. E.g. (8., 20.) would give two bands
            using 8 Hz and 20 Hz, respectively, as their higher frequencies.
        -   If infinity, no higher frequency is used.
        -   Only used if 'cs_method' is "fourier" or "multitaper".

        fmt_n_fft : int | None; default None
        -   Length of the FFT.
        -   If 'None', the number of samples between 'tmin' and 'tmax' is used.
        -   Only used if 'cs_method' is "fourier" or "multitaper".
        """
        if self._processed:
            ProcessingOrderError(
                "The data in this object has already been processed. "
                "Initialise a new instance of the object if you want to "
                "perform other analyses on the data."
            )

        self.power_method = power_method
        self.seeds = seeds
        self.targets = targets
        self.fmin = fmin
        self.fmax = fmax
        self.fskip = fskip
        self.faverage = faverage
        self.tmin = tmin
        self.tmax = tmax
        self.mt_bandwidth = mt_bandwidth
        self.mt_adaptive = mt_adaptive
        self.mt_low_bias = mt_low_bias
        self.cwt_freqs = cwt_freqs
        self.cwt_n_cycles = cwt_n_cycles
        self.n_components = n_components
        self.n_lags = n_lags
        self.average_windows = average_windows
        self.average_timepoints = average_timepoints
        self.block_size = block_size
        self.n_jobs = n_jobs

        self._sort_processing_inputs()

        self._get_results()

    def _sort_processing_inputs(self) -> None:
        """Checks that inputs for processing the data are appropriate."""
        super()._sort_processing_inputs()
        self._sort_used_settings()

    def _sort_used_settings(self) -> None:
        """Collects the settings that are relevant for the processing being
        performed and adds only these settings to the 'processing_steps'
        dictionary."""
        used_settings = {
            "con_methods": self.con_methods,
            "power_method": self.power_method,
            "n_lags": self.n_lags,
            "n_components": self.n_components,
            "average_windows": self.average_windows,
            "average_timepoints": self.average_timepoints,
            "t_min": self.tmin,
            "t_max": self.tmax,
        }

        if self.power_method == "multitaper":
            add_settings = {
                "mt_bandwidth": self.mt_bandwidth,
                "mt_adaptive": self.mt_adaptive,
                "mt_low_bias": self.mt_low_bias,
            }
        elif self.power_method == "cwt_morlet":
            add_settings = {"cwt_n_cycles": self.cwt_n_cycles}
        used_settings.update(add_settings)

        self.processing_steps["spectral_connectivity"] = used_settings
