'''
Created on 15 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from utils import out, wait_for_node_visible, touch_center, \
    wait_and_click_button, pos_center
from airtest.core.api import time, snapshot, swipe
from test_utils import State, find_current_state, go_to_academia


# =============================================================================
def test_tutorial_5(dev, poco):
    out('Tutorial_5 test started...')
    
    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test(dev, poco)
    out('Tutorial_5 test time: ' + str(time.time() - t0)) 

    if not f_ret:
        out('last snapshot')
        snapshot()
    
    return f_ret


# =============================================================================
def run_test(dev, poco, big_test=False):
    btn_back = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'
    btn_map = 'H_Canvas/USER_Main_UI/SWITCH_TO_MAP/Button_exit'
    # btn_map = 'H_Canvas/USER_Main_UI/MAP_ADDON/SWITCH_TO_WORLD'
    
    btn_quests_menu = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_qwest'
    # wnd_quests_menu_lst = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg'
    btn_quest_5 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (4)'
    btn_quest_6 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (5)'
    btn_accept_qst = 'H_Canvas/USER_Main_UI/EVENT_REVARD/Avr_paper/Avr_Accept'
    btn_cancel_qst = 'H_Canvas/USER_Main_UI/EVENT_REVARD/Avr_paper/Avr_Decline'

    wnd_event_reward = 'H_Canvas/USER_Main_UI/EVENT_REVARD'
    
    ### ---------------------------------------   
    
    if not go_to_academia(dev, poco):
        return False
    time.sleep(1)

    ### ---------------------------------------   
    # идем в меню выбора квеста
    # out('нажимаем кнопку квестов')
    if not wait_and_click_button(dev, poco, btn_quests_menu): return False
    # тыкаем первый квест
    if not wait_and_click_button(dev, poco, btn_quest_5): return False
    # тыкаем принять
    if not wait_and_click_button(dev, poco, btn_accept_qst): return False
    
    # тыкаем 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_equip'
    btn_path = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_equip'
    if not wait_and_click_button(dev, poco, btn_path): return False
    time.sleep(2)
    
    # подготавливаемся к свайпу
    sn_item_list = 'H_Canvas/USER_Main_UI/CONFIG_EQUIP_MAIN/'\
        +'ItemsBG/ScrollItems/Viewport/ItemList'
    sn_slot_canon = 'H_Canvas/USER_Main_UI/CONFIG_EQUIP_MAIN/Slots/Canon_1'
    sn_slot_canon_sub = 'H_Canvas/USER_Main_UI/CONFIG_EQUIP_MAIN/Slots/Canon_1/sub_1'
    node_slot = wait_for_node_visible(poco, sn_slot_canon, 5) 
    node_slot_sub = wait_for_node_visible(poco, sn_slot_canon_sub, 5)

    # перетаскиваем пушку в слот 
    node_item_list = wait_for_node_visible(poco, sn_item_list, 5)
    node_from = node_item_list.child()[0]
    pos_abs_from = pos_center(dev, node_from)
    pos_from = pos_center(dev, node_from, False)
    pos_to = pos_center(dev, node_slot, False)
    vec = [pos_to[0] - pos_from[0], pos_to[1] - pos_from[1]]
    print('vector ', pos_abs_from, vec)
    swipe(pos_abs_from, vector=vec, duration=3)
    time.sleep(1)

    # перетаскиваем улучшение в слот 
    node_item_list = wait_for_node_visible(poco, sn_item_list, 5)
    node_from = node_item_list.child()[0]
    pos_abs_from = pos_center(dev, node_from)
    pos_from = pos_center(dev, node_from, False)
    pos_to = pos_center(dev, node_slot_sub, False)
    vec = [pos_to[0] - pos_from[0], pos_to[1] - pos_from[1]]
    print('vector ', pos_abs_from, vec)
    swipe(pos_abs_from, vector=vec, duration=3)
    time.sleep(1)
    
    # выходим из окна улучшений
    if not wait_and_click_button(dev, poco, btn_back): return False        

    time.sleep(2);

    # сообщение "вот ваша награда"
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', '"вот ваша награда"')
        return False
    if not wait_and_click_button(dev, poco, btn_back): return False        
    
    if big_test:
        # идем в меню выбора квеста
        if not wait_and_click_button(dev, poco, btn_quests_menu): return False
        # тыкаем третий квест
        if not wait_and_click_button(dev, poco, btn_quest_6): return False
        # тыкаем отменить
        if not wait_and_click_button(dev, poco, btn_cancel_qst): return False
        # тыкаем назад из меню квестов
        if not wait_and_click_button(dev, poco, btn_back): return False
    ### ---------------------------------------    
        
    out('нажимаем кнопку выхода из города на карту')
    node = wait_for_node_visible(poco, btn_map, 5)
    if not node.exists():
        out('Button not showed', btn_map)
        return False
    touch_center(dev, node)
    time.sleep(1)

    return True

# =============================================================================
