'''
Created on 9 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from utils import out, wait_for_node_visible, touch_center, \
    wait_and_click_button
from airtest.core.api import time, snapshot
from test_utils import State, find_current_state, go_to_academia
from time import sleep


# =============================================================================
def test_tutorial_1(dev, poco):
    out('Tutorial_1 test started...')
    
    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test_tutorial_1(dev, poco)
    out('Tutorial_1 test time: ' + str(time.time() - t0))
    
    if not f_ret:
        out('last snapshot')
        snapshot()
    
    return f_ret


# =============================================================================
def run_test_tutorial_1(dev, poco, big_test=False):
    btn_back = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'
    btn_map = 'H_Canvas/USER_Main_UI/SWITCH_TO_MAP/Button_exit'
    # btn_map = 'H_Canvas/USER_Main_UI/MAP_ADDON/SWITCH_TO_WORLD'
    
    # btn_academy = 'T_GLOBAL_MAP/EPTown_t_academy_name'
    btn_tut_marker = 'T_GLOBAL_MAP/Event_Radius(Clone)'
    
    btn_quests_menu = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_qwest'
    # wnd_quests_menu_lst = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg'
    btn_quest_1 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (0)'
    btn_quest_2 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (1)'
    btn_accept_qst = 'H_Canvas/USER_Main_UI/EVENT_REVARD/Avr_paper/Avr_Accept'
    btn_cancel_qst = 'H_Canvas/USER_Main_UI/EVENT_REVARD/Avr_paper/Avr_Decline'
    
    wnd_event_reward = 'H_Canvas/USER_Main_UI/EVENT_REVARD'
    tutorial_quest_1 = 'TutorialQuest1(Clone)'
    
    btn_rot_left = 'H_Canvas/USER_Main_UI/CONTROLL_PANEL/ROT_LEFT'
    # btn_rot_right = 'H_Canvas/USER_Main_UI/CONTROLL_PANEL/ROT_RIGHT'
    btn_speed = 'H_Canvas/USER_Main_UI/CONTROLL_PANEL/TOGGLE_SPEED'
    btn_speed_up = 'H_Canvas/USER_Main_UI/SPEED_UP/BTN'
    ### ---------------------------------------   
    
    if not go_to_academia(dev, poco):
        return False
    time.sleep(1)

    ### ---------------------------------------   
    # идем в меню выбора квеста
    # out('нажимаем кнопку квестов')
    if not wait_and_click_button(dev, poco, btn_quests_menu):
        return False

    # тыкаем первый квест
    if not wait_and_click_button(dev, poco, btn_quest_1):
        return False
    
    # тыкаем принять
    if not wait_and_click_button(dev, poco, btn_accept_qst):
        return False
    
    # выходим на глобальную карту 
    if not wait_and_click_button(dev, poco, btn_map):
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
        sleep(3)
        state = find_current_state(poco)
    
    # тыкаем в маркер btn_tut_marker
    if not wait_and_click_button(dev, poco, btn_tut_marker):
        return False

    # ждём начала туториала сообщение "направление ветра"
    node = wait_for_node_visible(poco, tutorial_quest_1, 5)
    wait_cnt = 0
    while not node.exists():
        wait_cnt += 1
        if (wait_cnt > 3):
            out('долгое ожидание запуска обучения', 'что-то пошло не так')
            return False
        # out('wait')
        sleep(3)
        node = wait_for_node_visible(poco, tutorial_quest_1, 5)
        
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'что-то пошло не так, нет сообщения "направление ветра"')
        return False

    if not wait_and_click_button(dev, poco, btn_back):
        return False

    # поворачиваемся по ветру до появления "следуйте до следующего маркера"
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    wait_cnt = 0
    while not node.exists():
        wait_cnt += 1
        if (wait_cnt > 10):
            out('долгое ожидание сообщения', 'нет сообщения "следуйте до следующего маркера"')
            return False
        out('press rot_left')
        node = wait_for_node_visible(poco, btn_rot_left, 5)
        # touch_center(dev, node, logout=False, times=5)
        node.swipe([0, 0], duration=6)  # костыль на зажатие
        node = wait_for_node_visible(poco, wnd_event_reward, 5)
    # закрываем диалог
    if not wait_and_click_button(dev, poco, btn_back):
        return False
    
    # тыкаем на кнопку "паруса"
    if not wait_and_click_button(dev, poco, btn_speed):
        return False
    
    # следуем до появление про ускорение
    sleep(5)
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    wait_cnt = 0
    while not node.exists():
        wait_cnt += 1
        if (wait_cnt > 10):
            out('долгое ожидание сообщения', 'нет сообщения про ускорение')
            return False
        sleep(5)
        node = wait_for_node_visible(poco, wnd_event_reward, 5)
    # закрываем диалог
    if not wait_and_click_button(dev, poco, btn_back):
        return False
    
    # тыкаем "ускорение"
    if not wait_and_click_button(dev, poco, btn_speed_up):
        return False
    
    # ждём перехода на глобальную карту
    state = find_current_state(poco)
    wait_cnt = 0
    while state != State.MAP_EVENT_REWARD:
        wait_cnt += 1
        if (wait_cnt > 3):
            out('долгое ожидание глобальной карты', 'что-то пошло не так')
            return False
        out('wait')
        time.sleep(3)
        state = find_current_state(poco)
    
    # сообщение "ускорение работает на карте тоже"
    if not wait_and_click_button(dev, poco, btn_back):
        return False
    
    # тыкаем "ускорение"
    if not wait_and_click_button(dev, poco, btn_speed_up):
        return False
    
    # сообщение "отлично, вот твоя награда"
    if not wait_and_click_button(dev, poco, btn_back):
        return False
    
    # переходим в "академию"
    if not go_to_academia(dev, poco):
        return False
    time.sleep(1)
    
    if big_test:
        # идем в меню выбора квеста
        if not wait_and_click_button(dev, poco, btn_quests_menu): return False
        # тыкаем второй квест
        if not wait_and_click_button(dev, poco, btn_quest_2): return False
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
