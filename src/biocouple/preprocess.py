
import hrvanalysis as hrva



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
