'''
Created on 15 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from utils import out, wait_for_node_visible, touch_center, \
    wait_and_click_button, get_node_child
from airtest.core.api import time, snapshot
from test_utils import State, find_current_state, go_to_academia


# =============================================================================
def test_tutorial_6(dev, poco):
    out('Tutorial_6 test started...')
    
    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test(dev, poco)
    out('Tutorial_6 test time: ' + str(time.time() - t0)) 

    if not f_ret:
        out('last snapshot')
        snapshot()
    
    return f_ret


# =============================================================================
def run_test(dev, poco, big_test=False):
    path_back = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'
    path_map = 'H_Canvas/USER_Main_UI/SWITCH_TO_MAP/Button_exit'
    # path_map = 'H_Canvas/USER_Main_UI/MAP_ADDON/SWITCH_TO_WORLD'
    
    path_quests_menu = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_qwest'
    # wnd_quests_menu_lst = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg'
    path_quest_6 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (5)'
    path_quest_7 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (6)'
    path_spec_pirate = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/SPEC_Panel/SPEC_pirate'
    path_accept_qst = 'H_Canvas/USER_Main_UI/EVENT_REVARD/Avr_paper/Avr_Accept'
    path_cancel_qst = 'H_Canvas/USER_Main_UI/EVENT_REVARD/Avr_paper/Avr_Decline'

    path_event_reward = 'H_Canvas/USER_Main_UI/EVENT_REVARD'
    
    ### ---------------------------------------   
    
    if not go_to_academia(dev, poco):
        return False
    time.sleep(1)

    ### ---------------------------------------   
    # идем в меню выбора квеста
    # out('нажимаем кнопку квестов')
    if not wait_and_click_button(dev, poco, path_quests_menu): return False
    # тыкаем первый квест
    if not wait_and_click_button(dev, poco, path_quest_6): return False
    # тыкаем принять
    if not wait_and_click_button(dev, poco, path_accept_qst): return False

    # нажимаем кнопку выхода из города на карту
    node = wait_for_node_visible(poco, path_map, 5)
    if not node.exists():
        out('Button not showed', path_map)
        return False
    touch_center(dev, node)
    time.sleep(1)    
    
    # поплыли на жанетту
    path = 'T_GLOBAL_MAP/EPTown_Janetta'
    node = wait_for_node_visible(poco, path, 5)
    touch_center(dev, node)
    
    # '''
    user_main_ui = 'H_Canvas/USER_Main_UI'
    fights = ['NEW_FIGHT/AUTOFIGHT', 'NEW_FIGHT (1)/AUTOFIGHT', 'NEW_FIGHT (2)/AUTOFIGHT']
    f_exit = False
    i = 50
    while not f_exit:
        i -= 1
        if i < 0:
            out('долгое ожидание сообщения', 'корабль достаточно потрепало...')
            return False
        node = wait_for_node_visible(poco, user_main_ui)
        wnd_reward = get_node_child(node, 'EVENT_REVARD', False)
        if wnd_reward.exists():
            # по идее дождались сообщения о повреждённости корабля
            out('корабль достаточно потрепало...')
            if not wait_and_click_button(dev, poco, path_back): return False        
            f_exit = True
        else :
            touched = False
            for fight in fights:
                node_fight = get_node_child(node, fight, False)
                if node_fight.exists() and not touched:
                    out('автобой... ' + fight)
                    touch_center(dev, node_fight)
                    touched = True
        if not f_exit:        
            time.sleep(0.5)
        
    state = find_current_state(poco)
    while state != State.TOWN:
        out('ждём Жанетту (3 sec)')
        time.sleep(3)
        state = find_current_state(poco)
    # '''
    
    # идем в меню выбора квеста
    out('нажимаем кнопку квестов')
    if not wait_and_click_button(dev, poco, path_quests_menu): return False

    # чинимся за счёт пиратов
    out('чинимся за счёт пиратов')
    if not wait_and_click_button(dev, poco, path_spec_pirate): return False

    # сообщение "вот ваша награда"
    node = wait_for_node_visible(poco, path_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', '"вот ваша награда"')
        return False
    if not wait_and_click_button(dev, poco, path_back): return False        

    out('нажимаем кнопку выхода из города на карту')
    node = wait_for_node_visible(poco, path_map, 5)
    if not node.exists():
        out('Button not showed', path_map)
        return False
    touch_center(dev, node)
    time.sleep(1)

    out('плывём в академию')
    if not go_to_academia(dev, poco):
        return False
    
    time.sleep(2);
    
    if big_test:
        # идем в меню выбора квеста
        if not wait_and_click_button(dev, poco, path_quests_menu): return False
        # тыкаем третий квест
        if not wait_and_click_button(dev, poco, path_quest_7): return False
        # тыкаем отменить
        if not wait_and_click_button(dev, poco, path_cancel_qst): return False
        # тыкаем назад из меню квестов
        if not wait_and_click_button(dev, poco, path_back): return False
    ### ---------------------------------------    
        
    out('нажимаем кнопку выхода из города на карту')
    node = wait_for_node_visible(poco, path_map, 5)
    if not node.exists():
        out('Button not showed', path_map)
        return False
    touch_center(dev, node)
    time.sleep(1)

    return True

# =============================================================================
