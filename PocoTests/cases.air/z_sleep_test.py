'''
Created on 22 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from airtest.core.api import time, snapshot, sleep
from utils import out
from test_utils import State, find_current_state


# =============================================================================
def test_z_sleep_test(dev, poco):
    out('z_slepp_test test started...')
    
    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test(dev, poco)
    out('z_slepp_test test time: ' + str(time.time() - t0)) 

    if not f_ret:
        out('last snapshot')
        snapshot()
    
    return f_ret


# =============================================================================
def run_test(dev, poco):

    sleep(2);

    return True

# =============================================================================
