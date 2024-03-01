
import numpy as np
import pandas as pd


def make_windows(min_t,max_t,win_size,step_size):
    # Create a set of windows over a given time interval (min_t,max_t)
    # of size win_size, and with the given step_size.
    
    win = []

    for i,onset_t in enumerate(np.arange(min_t,max_t-win_size,step_size)):
        offset_t = onset_t+win_size
        w = {
            'window_i':i, # window index
            't_min':onset_t, # used for cutting
            't_max':offset_t, # used for cutting
            't_size':win_size,
            't':np.mean([onset_t,offset_t])-min_t # window center        
        }
        win.append(w)
    return win





def window_map(rpeaks,win,fun):
    """
    Given a window definition win, apply the function fun to the
    given rpeaks within that window.
    rpeaks has to be a list of dicts (or a pandas data frame) where each
    dict contains a t key (for the time) and an nn key (for the nn-interval at that time).
    The fun should take the nn-intervals only and return
    a set of key-value properties.
    """
    
    t = win['t'] # this is the nominal t, we've already subtracted the average
    onset_t = win['t_min']
    offset_t = win['t_max']

    # Identify the window    
    res={'t':t,'t_size':win['t_size']}

    ## Extract the RR peaks in this time frame
    rr = rpeaks[ (rpeaks['t']>=onset_t) & (rpeaks['t']<offset_t) ]['nn']

    feats = fun(rr)
    for f in feats.keys():
        res[f] = feats[f]

    return res
    



def split_windows(
    peak,
    win_size,min_t,max_t,step_size,
    fun
):

    """ Split the data up into windows, and for each window,
    apply the function """
    
    wins = make_windows(min_t,max_t,win_size,step_size)

    res = []
    for w in wins:
        r = window_map(peak,w,fun)
        res.append(r)

    return pd.DataFrame(res)
