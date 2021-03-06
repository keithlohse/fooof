"""
01: Model Description
=====================
"""

###############################################################################
#
# This tutorial provides a more theoretical / mathematical description of the FOOOF model and parameters.
#

###############################################################################
# Introduction
# ------------
#
# A neural power spectrum is fit as a combination of the aperiodic signal and periodic oscillations.
#
# The aperiodic component of the signal displays 1/f like properties, and is referred to in the code as the 'background'.
#
# Putative oscillations (hereafter referred to as 'peaks'), are frequency regions in which there are 'bumps' of power over and above the aperiodic signal.
#
# This formulation roughly translates to fitting the power spectrum as:
#
# .. math::
#    P = L + \sum_{n=0}^{N} G_n
#
# Where `P` is the power spectrum, `L` is the aperiodic signal, and each :math:`G_n` is a Gaussian fit to a peak, for `N` total peaks extracted from the power spectrum.

###############################################################################
# Aperiodic ('background') Fit
# ----------------------------
#
# The aperiodic fit uses an exponential function, fit on the semilog power spectrum (linear frequencies and $log10$ power values).
#
# The exponential is of the form:
#
# .. math::
#    L = 10^b * \frac{1}{(k + F^\chi)}
#
# Or, equivalently:
#
# .. math::
#    L = b - \log(k + F^\chi)
#
# In this formulation, the 3 parameters `b`, `k`, and :math:`\chi` define the aperiodic signal, as:
#
# - `b` is the broadband 'offset'
# - `k` relates to the 'knee'
# - :math:`\chi` is the 'slope'
# - `F` is the vector of input frequencies
#
# Note that fitting the knee parameter is optional. If used, the knee defines a bend in the 1/f.
#
# By default the aperiodic signal is fit with the 'knee' parameter set to zero. This fits the aperiodic signal equivalently to fitting a linear fit in log-log space.
#
# Broader frequency ranges typically do not display a single 1/f like characteristic, and so for these cases fitting with the knee parameter allows for modelling bends in the aperiodic signal.

###############################################################################
# Peaks
# -----
#
# Regions of power over above this aperiodic signal, as defined above, are considered to be putative oscillations and are fit in the model by a Gaussian.
#
# For each Gaussian, :math:`G_n`, with the form:
#
# .. math::
#    G_n = a * exp (\frac{- (F - c)^2}{2 * w^2})
#
# Each peak is defined in terms of parameters `a`, `c` and `w`, where:
#
# - `a` is the amplitude of the peak, over and above the aperiodic signal
# - `c` is the center frequency of the peak
# - `w` is the width of the peak
# - `F` is the vector of input frequencies
#
# The full power spectrum fit is therefore the combination of the aperiodic fit, `L` defined by the exponential fit, and `N` peaks, where each :math:`G_n` is formalized as a Gaussian process.
#
# Full method details are available in the paper: https://www.biorxiv.org/content/early/2018/04/11/299859

###############################################################################
# Algorithmic Description
# -----------------------
#
# Briefly, the algorithm proceeds as such:
#
# - An initial fit of the aperiodic 'background' signal is taken across the power spectrum
# - This aperiodic fit is subtracted from the power spectrum, creating a flattened spectrum
# - Peaks are iteratively found in this flattened spectrum
# - A full peak fit is created of all peak candidates found
# - The peak fit is subtracted from the original power spectrum, creating a peak-removed power spectrum
# - A final fit of the aperiodic signal is taken of the peak-removed power spectrum

###############################################################################
#
# This procedure is able to create a model of the neural power spectrum, that is fully described mathematical by the mathematical model from above:
#
#.. image:: ../../img/FOOOF_model_pic.png

###############################################################################
# FOOOF Parameters
# ----------------
#
# There are a number of parameters that control the FOOOF fitting algorithm.
#
# Parameters that are exposed in the API and that can be set by the user are explained in detail below.
#
#
# Controlling Peak Fits
# ~~~~~~~~~~~~~~~~~~~~~
#
# **peak_width_limits (Hz)**
#
# Enforced limits on the minimum and maximum widths of extracted peaks, given as a list of [minimum bandwidth, maximum bandwidth]. We recommend bandwidths be set to be at last twice the frequency resolution of the power spectrum.
#
# Default: [0.5, 12]
#
# Peak Search Stopping Criteria
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# An iterative procedures searches for candidate peaks in the flattened spectrum. Candidate peaks are extracted in order of decreasing amplitude, until some stopping criterion is met, which is controlled by the following parameters:
#
# **max_n_peaks (int)**
#
# The maximum number of peaks that can be extracted from a given power spectrum. FOOOF will halt searching for new peaks when this number is reached. Note that FOOOF extracts peaks iteratively by amplitude (over and above the aperiodic signal), and so this approach will extract (up to) the _n_ largest peaks.
#
# Default: infinite
#
# **peak_threshold (in units of standard deviation)**
#
# The threshold, in terms of standard deviation of the aperiodic signal-removed power spectrum, above which a data point must pass to be considered a candidate peak. Once a candidate peak drops below this threshold, the peak search is halted (without including the most recent candidate).
#
# Default: 2.0
#
# **min_peak_amplitude (units of power - same as the input spectrum)**
#
# The minimum amplitude, above the aperiodic fit, that a peak must have to be extracted in the initial fit stage. Once a candidate peak drops below this threshold, the peak search is halted (without including the most recent candidate). Note that because this constraint is enforced during peak search, and prior to final peak fit, returned peaks are not guaranteed to surpass this value in amplitude.
#
# Default: 0
#
# Note: there are two different amplitude-related halting conditions for the peak searching. By default, the relative (standard-deviation based) threshold is defined, whereas the absolute threshold is set to zero (this default is because there is no general way to set this value without knowing the scale of the data). If both are defined, both are used and the peak search will halt when a candidate peak fails to pass either the absolute, or relative threshold.
#
# Aperiodic Signal Fitting Approach
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# **background_mode (string)**
#
# The fitting approach to use for the aperiodic 'background' signal.
#
# Options:
#   - 'fixed' : fits without a knee parameter (with the knee parameter 'fixed' at 0)
#   - 'knee' : fits the full exponential equation, including the 'knee' parameter. (experimental)
#
# Default='fixed'
