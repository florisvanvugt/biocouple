
import numpy as np


def make_windows(min_t,max_t,win_size,step_size):
    
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


