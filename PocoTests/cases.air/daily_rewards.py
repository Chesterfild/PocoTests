'''
Created on 6 апр. 2020 г.

@author: _OttoVonChesterfild_
'''
# from poco.drivers.unity3d import UnityPoco
from airtest.core.api import time, snapshot
from utils import out, wait_for_node_visible, touch_center, get_node_child
from test_utils import State, find_current_state

# from airtest.core.helper import set_logdir
# from airtest.report.report import simple_report

dr_btn = 'H_Canvas/USER_Main_UI/Daily_Reward_And_Help_Button/DAILY_REWARD_BUTTON'
dr_wnd = 'H_Canvas/USER_Main_UI/DailyRewardsContainer/DR_Window(Clone)'
content = 'DailyRewardPanel/Scroll View/Viewport/Content'
back_descr_bg = 'H_Canvas/USER_Main_UI/Slot_Descr_BG'

back_btn = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'


# =============================================================================
def test_daily_rewards(dev, poco):
    out('Daily Rewards test started...')

    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test_daily_rewards(dev, poco)
    out('Daily Rewards test time: ' + str(time.time() - t0))
    
    if not f_ret:
        out('last snapshot')
        snapshot()
    
    return f_ret


# =============================================================================
def run_test_daily_rewards(dev, poco):
    
    out("нажимаем кнопку награды")
    node = wait_for_node_visible(poco, dr_btn, 5)
    if not node.exists():
        out('Button not showed', back_btn)
        return False
    touch_center(dev, node)

    time.sleep(1)

    ### ---------------------------------------   
    # ## пробегаемся по первой страничке
    if not test_reward_packages(poco, dev, 0, 0):  # 0,4
        return False
    
    if not test_swipe_reward_packages(poco, 4, 0):
        return False
    # ## пробегаемся по второй страничке
    if not test_reward_packages(poco, dev, 5, 5):  # 5,10
        return False
    
    if not test_swipe_reward_packages(poco, 9, 5):
        return False

    # ## пробегаемся по последней страничке
    if not test_reward_packages(poco, dev, 11, 13):  # 11,13
        return False
    ### ---------------------------------------    
        
    out('нажимаем кнопку выхода из окна наград')
    node = wait_for_node_visible(poco, back_btn, 5)
    if not node.exists():
        out('Button not showed', back_btn)
        return False
    touch_center(dev, node)
    time.sleep(1)

    # дополнительная проверка на выход из окна наград
    node = wait_for_node_visible(poco, dr_wnd, 2)
    while node.exists():
        out("window not closed", dr_wnd);
        node = wait_for_node_visible(poco, back_btn, 5)
        if not node.exists():
            out('Button not showed', back_btn)
            return False
        touch_center(dev, node)
        time.sleep(1)
        node = wait_for_node_visible(poco, dr_wnd, 2)
        
    return True


# =============================================================================
def test_reward_packages(poco, dev, row0, row1):
    # ## tood: вынести в отдельную функцию 
    i = row0
    while i <= row1:
        time.sleep(1)
        # это обновляем постоянно
        node = wait_for_node_visible(poco, dr_wnd, 5)
        if not node.exists():
            out('Window not showed', dr_wnd)
            return False
        node = get_node_child(node, content)
        lst_days = node.child()

        # в общемто тут все элементы надо получать заново        
        lst_rewards = lst_days[i].child('Rewards')
        ii = 0
        for btn in lst_rewards.child():
            out('touch reward[' + str(i) + '][' + str(ii) + ']')
            touch_center(dev, btn)
            time.sleep(1)
            node = wait_for_node_visible(poco, back_descr_bg, 0)
            if node.exists():
                touch_center(dev, wait_for_node_visible(poco, back_btn, 5))
            ii = ii + 1
        i = i + 1

    return True


# =============================================================================
def test_swipe_reward_packages(poco, row_from, row_to):
    node = wait_for_node_visible(poco, dr_wnd, 5)
    if not node.exists():
        out('Window not showed', dr_wnd)
        return False
    node = get_node_child(node, content)
    lst_days = node.child()

    out('свайпаем экран с колонки ' + str(row_from + 1) + ' до колонки ' + str(row_to + 1))
    lst_days[row_from].drag_to(lst_days[row_to])
    return True
