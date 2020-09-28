'''
Created on 17 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from utils import out, wait_for_node_visible, touch_center, \
    wait_and_click_button, pos_scr2abs, pos_center
from airtest.core.api import time, snapshot, swipe
from test_utils import State, find_current_state, go_to_academia, rotate_cam_to


# ================================================================
def test_my(dev, poco):
    # '''
    node_path = 'Rank2(Clone)/MARKER_NEW(Clone)/4-PRECISSION'
    if not rotate_l_let_to(dev, poco, node_path, True): return False 
    
    '''
    node_path = 'Rank2(Clone)/MARKER_NEW(Clone)/10-MobileRelationsMark'

    if not rotate_cam_zoom_to(dev, poco, node_path, True):
        print('test fail')
        return False 
    
    print('test ok')
    # '''
        
    return True 


# =============================================================================
def test_tutorial_7(dev, poco):
    out('Tutorial_7 test started...')
    
    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test(dev, poco)
    out('Tutorial_7 test time: ' + str(time.time() - t0)) 

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
    path_quest_7 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (6)'
    path_quest_8 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (7)'
    path_accept_qst = 'H_Canvas/USER_Main_UI/EVENT_REVARD/Avr_paper/Avr_Accept'
    path_cancel_qst = 'H_Canvas/USER_Main_UI/EVENT_REVARD/Avr_paper/Avr_Decline'

    path_event_reward = 'H_Canvas/USER_Main_UI/EVENT_REVARD'
    
    precission_path = 'Rank2(Clone)/MARKER_NEW(Clone)/4-PRECISSION'
    
    ### ---------------------------------------   
    
    if not go_to_academia(dev, poco):
        return False
    time.sleep(1)

    ### ---------------------------------------   
    # идем в меню выбора квеста
    # out('нажимаем кнопку квестов')
    if not wait_and_click_button(dev, poco, path_quests_menu): return False
    # тыкаем первый квест
    if not wait_and_click_button(dev, poco, path_quest_7): return False
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

    tutorial_quest_7 = 'TutorialQuest7(Clone)'
    # ждём начала туториала сообщение "направление ветра"
    node = wait_for_node_visible(poco, tutorial_quest_7, 5)
    wait_cnt = 0
    while not node.exists():
        wait_cnt += 1
        if (wait_cnt > 3):
            out('долгое ожидание запуска обучения', 'что-то пошло не так')
            return False
        out('ждём запуска туториала (3 sec)')
        time.sleep(3)
        node = wait_for_node_visible(poco, tutorial_quest_7, 5)
    # сообщение 'нведите трубу на врага'
    node = wait_for_node_visible(poco, path_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'нведите трубу на врага')
        return False
    # тыкаем back
    if not wait_and_click_button(dev, poco, path_back): return False

    # поворачиваем камеру к кораблю
    node_path = 'Rank2(Clone)/MARKER_NEW(Clone)/10-MobileRelationsMark'
    if not rotate_cam_to(dev, poco, node_path, True): return False 

    # тыкаем Zoom
    node_path = 'H_Canvas/USER_Main_UI/CONTROLL_PANEL/ZOOM'
    if not wait_and_click_button(dev, poco, node_path): return False
    
    # поворачиваем камеру к кораблю
    # node_path = 'Rank2(Clone)/MARKER_NEW(Clone)/10-MobileRelationsMark'
    # if not rotate_cam_zoom_to(dev, poco, node_path, True): return False 

    # сообщение 'уничтожте карабль'
    node = wait_for_node_visible(poco, path_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'уничтожте карабль')
        return False
    # тыкаем back
    if not wait_and_click_button(dev, poco, path_back): return False

    node_path = 'H_Canvas/USER_Main_UI/CONTROLL_PANEL/TOGGLE_SPEED'
    if not wait_and_click_button(dev, poco, node_path): return False

    out('ожидаем подплытия')
    time.sleep(30)
    
    node_path = 'H_Canvas/USER_Main_UI/CONTROLL_PANEL/TOGGLE_SPEED'
    if not wait_and_click_button(dev, poco, node_path): return False

    # поворачиваем камеру к кораблю poco("4-PRECISSION")
    if not rotate_l_let_to(dev, poco, precission_path, True): return False 

    f_exit = False
    while not f_exit:
        node = wait_for_node_visible(poco, path_event_reward, 5)
        if not node.exists():
            node = wait_for_node_visible(poco, precission_path, 10)
            if not node.exists():
                out('долгое ожидание прицела', precission_path)
                return False
            node_path = 'H_Canvas/USER_Main_UI/FIGHT_PANEL/SHOOT_Manual'
            if not wait_and_click_button(dev, poco, node_path): return False
            time.sleep(4)  # задержка для перезарядки
        else :
            f_exit = True
    
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
        if not wait_and_click_button(dev, poco, path_quest_8): return False
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
# ================================================================
def rotate_cam_zoom_to(dev, poco, node_path, log_out=False):
    path_event_reward = 'H_Canvas/USER_Main_UI/EVENT_REVARD'
    pos_from = pos_scr2abs(dev, [0.5, 0.1])
    
    f_exit = False
    i = 0
    while not f_exit:
        pos_scr = [0, 0.2]
        # pos_abs = pos_scr2abs(dev, pos_scr)
        
        if wait_for_node_visible(poco, path_event_reward, 1).exists():
            out('event_reward')
            return True 
        
        node_case_lod = wait_for_node_visible(poco, node_path)
        if node_case_lod.exists():
            if log_out:
                out(node_path + ' exists...')
            pos_scr = pos_center(dev, node_case_lod, False)
            # pos_abs = pos_scr2abs(dev, pos_scr)
        
        step = 0.1

        if pos_scr[0] > 0.48 and pos_scr[0] < 0.52:
            step = 0.0
            f_exit = True
        
        if pos_scr[0] < 0.48 or pos_scr[0] > 0.52:
            step = 0.01
        if pos_scr[0] < 0.40 or pos_scr[0] > 0.60:
            step = 0.02
        if pos_scr[0] < 0.30 or pos_scr[0] > 0.70:
            step = 0.05
        
        print('position:' + str(pos_scr))
        
        if pos_scr[0] > 0.5:
            swipe(pos_from, vector=[step, 0], duration=1)
            if log_out:
                out('swipe to left on ' + str(step))
        if pos_scr[0] < 0.5:
            swipe(pos_from, vector=[-step, 0], duration=1)
            if log_out:
                out('swipe to right on ' + str(step))
        i += 1
        if i > 30:
            if log_out:
                out('долгое ожидание поворота к обьекту', node_path)
            return False 
        
    out('it: ' + str(i))
    return True 


# ================================================================
def rotate_l_let_to(dev, poco, node_path, log_out=False):
    path_rot_right = 'H_Canvas/USER_Main_UI/CONTROLL_PANEL/ROT_RIGHT'
    pos_abs_right = pos_center(dev, wait_for_node_visible(poco, path_rot_right))
    
    f_exit = False
    i = 0
    while not f_exit:
        swipe(pos_abs_right, pos_abs_right, duration=2)
        
        if wait_for_node_visible(poco, node_path, 1).exists():
            out('precision exists')
            f_exit = True
            return True 
        
        i += 1
        if i > 30:
            if log_out:
                out('долгое ожидание поворота к обьекту', node_path)
            return False 
        
    out('it: ' + str(i))
    return True 
