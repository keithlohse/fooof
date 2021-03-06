"""Helper functions for running and working with FOOOF & FOOOFGroup objects."""

import numpy as np

from fooof import FOOOFGroup
from fooof.synth.gen import gen_freqs
from fooof.utils import get_settings, get_obj_desc, compare_settings, compare_data_info

###################################################################################################
###################################################################################################

def combine_fooofs(fooofs):
    """Combine a group of FOOOF and/or FOOOFGroup objects into a single FOOOFGroup object.

    Parameters
    ----------
    fooofs : list of FOOOF objects
        FOOOF objects to be concatenated into a FOOOFGroup.

    Returns
    -------
    fg : FOOOFGroup object
        Resultant FOOOFGroup object created from input FOOOFs.
    """

    # Compare settings
    if not compare_settings(fooofs) or not compare_data_info(fooofs):
        raise ValueError("These objects have incompatible settings or data," \
                         "and so cannot be combined.")

    # Initialize FOOOFGroup object, with settings derived from input objects
    fg = FOOOFGroup(**get_settings(fooofs[0]), verbose=fooofs[0].verbose)
    fg.power_spectra = np.empty([0, len(fooofs[0].freqs)])

    # Add FOOOF results from each FOOOF object to group
    for f_obj in fooofs:
        # Add FOOOFGroup object
        if isinstance(f_obj, FOOOFGroup):
            fg.group_results.extend(f_obj.group_results)
            fg.power_spectra = np.vstack([fg.power_spectra, f_obj.power_spectra])
        # Add FOOOF object
        else:
            fg.group_results.append(f_obj.get_results())
            fg.power_spectra = np.vstack([fg.power_spectra, f_obj.power_spectrum])

    # Add data information information
    for data_info in get_obj_desc()['freq_info']:
        setattr(fg, data_info, getattr(fooofs[0], data_info))
    fg.freqs = gen_freqs(fg.freq_range, fg.freq_res)

    return fg


def fit_fooof_group_3d(fg, freqs, power_spectra, freq_range=None, n_jobs=1):
    """Run FOOOFGroup across a 3D collection of power spectra.

    Parameters
    ----------
    fg : FOOOFGroup
        Fitting object, pre-initialized with desired settings, to fit with.
    freqs : 1d array
        Frequency values.
    power_spectra : 3d array
        Power values, in linear space, as [n_conditions, n_power_spectra, n_freqs].
    freq_range : list of [float, float], optional
        Desired frequency range to fit. If not provided, fits the entire given range.
    n_jobs : int, optional
        Number of jobs to run in parallel. default: 1
            1 is no parallelization. -1 uses all available cores.

    Returns
    -------
    fgs : list of FOOOFGroups
        Collected FOOOFGroups after fitting across power spectra, length of n_conditions.
    """

    fgs = []
    for cond_spectra in power_spectra:
        fg.fit(freqs, cond_spectra, freq_range, n_jobs)
        fgs.append(fg.copy())

    return fgs
