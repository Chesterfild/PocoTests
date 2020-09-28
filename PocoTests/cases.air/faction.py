'''
Created on 9 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from airtest.core.api import time, snapshot
from utils import out, wait_for_node_visible, touch_center, get_node_child
from test_utils import State, find_current_state

# =============================================================================
btn_back = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'

btn_faction = 'H_Canvas/USER_Main_UI/FRACTION'
wnd_faction = 'H_Canvas/USER_Main_UI/FACTION_CHANGE_MOBILE'

_faction_lst = 'BgImage/BorderImage/FactionsPanel'


# =============================================================================
def test_faction(dev, poco):
    out('Faction test started...')
    
    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test_faction(dev, poco)
    out('Faction test time: ' + str(time.time() - t0))
    
    if not f_ret:
        out('last snapshot')
        snapshot()
    
    return f_ret


# =============================================================================
def run_test_faction(dev, poco):
    
    out("нажимаем кнопку Fraction")
    node = wait_for_node_visible(poco, btn_faction, 5)
    if not node.exists():
        out('Button not showed', btn_faction)
        return False
    touch_center(dev, node)
    time.sleep(1)

    # проверочка
    node_wnd_faction = wait_for_node_visible(poco, wnd_faction, 2)
    if not node_wnd_faction.exists():
        out('Window not showed', wnd_faction)
        return False

    ### ---------------------------------------   

    node_lst = get_node_child(node_wnd_faction, _faction_lst)
    if not node_lst.exists():
        out('Window not showed', node_lst)
        return False

    for item in node_lst.child():
        touch_center(dev, item)
        time.sleep(0.5)

    ### ---------------------------------------    
        
    out('нажимаем кнопку выхода из окна выбора фракции')
    node = wait_for_node_visible(poco, btn_back, 5)
    if not node.exists():
        out('Button not showed', btn_back)
        return False
    touch_center(dev, node)
    time.sleep(1)

    return True

