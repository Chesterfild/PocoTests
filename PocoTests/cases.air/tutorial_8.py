'''
Created on 20 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from utils import out, wait_for_node_visible, touch_center, \
    wait_and_click_button
from airtest.core.api import time, snapshot
from test_utils import State, find_current_state, go_to_academia


# =============================================================================
def test_tutorial_8(dev, poco):
    out('Tutorial_8 test started...')
    
    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test(dev, poco)
    out('Tutorial_8 test time: ' + str(time.time() - t0)) 

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
    # path_quests_menu_lst = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg'
    path_quest_8 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (7)'
    path_quest_9 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (8)'
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
    if not wait_and_click_button(dev, poco, path_quest_8): return False
    # тыкаем принять
    if not wait_and_click_button(dev, poco, path_accept_qst): return False
    
    # выходим на глобальную карту 
    if not wait_and_click_button(dev, poco, path_map):
        return False
    
    # ждём перехода на глобальную карту
    state = find_current_state(poco)
    wait_cnt = 0
    while state != State.MAP:
        wait_cnt += 1
        if (wait_cnt > 3):
            out('долгое ожидание глобальной карты', 'что-то пошло не так')
            return False
        # out('wait')
        time.sleep(3)
        state = find_current_state(poco)
    
    # тыкаем в маркер btn_tut_marker
    btn_tut_marker = 'T_GLOBAL_MAP/Event_Radius(Clone)'
    if not wait_and_click_button(dev, poco, btn_tut_marker):
        return False

    tutorial_quest_8 = 'TutorialQuest8(Clone)'
    # ждём начала туториала сообщение "нажмите на знак артефакта"
    node = wait_for_node_visible(poco, tutorial_quest_8, 5)
    wait_cnt = 0
    while not node.exists():
        wait_cnt += 1
        if (wait_cnt > 3):
            out('долгое ожидание запуска обучения', 'что-то пошло не так')
            return False
        out('ждём запуска туториала (3 sec)')
        time.sleep(3)
        node = wait_for_node_visible(poco, tutorial_quest_8, 5)
        
    # сообщение 'нажмите на знак артефакта'
    node = wait_for_node_visible(poco, path_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'нажмите на знак артефакта')
        return False
    # тыкаем back
    if not wait_and_click_button(dev, poco, path_back): return False

    # жмём на использование артефакта
    path_artefact = 'H_Canvas/USER_Main_UI/ARTEFACT_BLOCK/Artefact1/ArtefactIcon'
    if not wait_and_click_button(dev, poco, path_artefact): return False
    time.sleep(10)
    
    # сообщение 'нужно время на востановление'
    node = wait_for_node_visible(poco, path_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'нужно время на востановление')
        return False
    # тыкаем back
    if not wait_and_click_button(dev, poco, path_back): return False
    time.sleep(5)

    # сообщение 'потопите 2 тренеровочных корабля'
    node = wait_for_node_visible(poco, path_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'потопите 2 тренеровочных корабля')
        return False
    # тыкаем back
    if not wait_and_click_button(dev, poco, path_back): return False
    time.sleep(10)

    # цикл потопления кораблей
    f_exit = False
    i = 10
    while not f_exit:
        node = wait_for_node_visible(poco, path_event_reward, 5)
        if node.exists():
            f_exit = True
        else:
            # жмём на использование артефакта
            path_artefact = 'H_Canvas/USER_Main_UI/ARTEFACT_BLOCK/Artefact1/ArtefactIcon'
            if not wait_and_click_button(dev, poco, path_artefact): return False
            time.sleep(10)
            if i < 1:
                out('долгое потопление кораблей', '')
                return False

    # сообщение "вот ваша награда"
    node = wait_for_node_visible(poco, path_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', '"вот ваша награда"')
        return False
    if not wait_and_click_button(dev, poco, path_back): return False        

    # поплыли в академию
    if not go_to_academia(dev, poco):
        return False
    time.sleep(1)

    if big_test:
        # идем в меню выбора квеста
        if not wait_and_click_button(dev, poco, path_quests_menu): return False
        # тыкаем третий квест
        if not wait_and_click_button(dev, poco, path_quest_9): return False
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
