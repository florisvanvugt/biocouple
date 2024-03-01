

import hrvanalysis as hrva

import numpy as np


def does_overlap(intv1,intv2):
    # Return whether the two intervals overlap
    (a1,b1)=intv1
    (a2,b2)=intv2
    overlapmin = max([a1,a2])
    overlapmax = min([b1,b2])
    return overlapmin<=overlapmax



def get_valid_RR_intervals(validpeaks,invalid):
    """ 
    Given a set of R-peak time points (in seconds),
    and a set of artefactual time ranges (_,(t0,t1)) indicating that the time interval [t0,t1] of the signal
    should not be used,
    compute the list of valid intervals (i.e. ones that do not overlap with an artefactual time range.
    R-peak intervals which overlap with an artefactual (invalid) region are replaced with NA.
    Return a list of (t,rr) tuples indicating that at time t an RR-interval of duration rr initiated.
    """
    
    validpeaks.sort()
    inv = invalid # the regions marked as invalid
    united = []

    for i,t in enumerate(validpeaks[:-1]):
        nextpeak_t = validpeaks[i+1]

        ## Check that this does not fall into regions marked as artefactual
        accepted = True
        for (_,t0,t1) in inv:   ## This is assuming that the artefactual regions provided are *only* for the signal we are interested in
            if does_overlap((t0,t1),(t,nextpeak_t)):
                ## Oops, this falls into the invalid range!
                accepted = False

        t = np.around(t,5)                
        if accepted:
            rr_intvl = np.around(nextpeak_t-t,5)
            united.append((t,rr_intvl))
        else:
            united.append((t,np.nan))
    
    return united






MIN_RR_INTVL = 300
MAX_RR_INTVL = 2000

# https://aura-healthcare.github.io/hrv-analysis/hrvanalysis.html



def preprocess_ecg(intvl):
    # Given a set of RR-intervals, in ms, preprocess them
    
    # This remove outliers from signal
    rr = hrva.remove_outliers(rr_intervals=intvl, 
                         low_rri=MIN_RR_INTVL, 
                         high_rri=MAX_RR_INTVL)
    
    # This replace outliers nan values with linear interpolation
    rr = hrva.interpolate_nan_values(rr_intervals=rr, interpolation_method="linear")
    
    # This remove ectopic beats from signal
    rr = hrva.remove_ectopic_beats(rr_intervals=rr, method="malik")

    # This replace ectopic beats nan values with linear interpolation
    rr = hrva.interpolate_nan_values(rr_intervals=rr)
    
    return rr




