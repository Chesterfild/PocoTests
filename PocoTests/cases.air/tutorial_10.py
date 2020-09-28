'''
Created on 21 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from utils import out, wait_for_node_visible, touch_center, \
    wait_and_click_button, get_node_child
from airtest.core.api import time, snapshot
from test_utils import State, find_current_state, go_to_academia


# =============================================================================
def test_tutorial_10(dev, poco):
    out('Tutorial_10 test started...')
    
    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test(dev, poco)
    out('Tutorial_10 test time: ' + str(time.time() - t0)) 

    if not f_ret:
        out('last snapshot')
        snapshot()
    
    return f_ret


# =============================================================================
def run_test(dev, poco):
    path_back = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'
    path_map = 'H_Canvas/USER_Main_UI/SWITCH_TO_MAP/Button_exit'
    # path_map = 'H_Canvas/USER_Main_UI/MAP_ADDON/SWITCH_TO_WORLD'
    
    path_quests_menu = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_qwest'
    # path_quests_menu_lst = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg'
    path_quest_10 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (9)'
    path_accept_qst = 'H_Canvas/USER_Main_UI/EVENT_REVARD/Avr_paper/Avr_Accept'
    #path_cancel_qst = 'H_Canvas/USER_Main_UI/EVENT_REVARD/Avr_paper/Avr_Decline'

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
    if not wait_and_click_button(dev, poco, path_quest_10): return False
    # тыкаем принять
    if not wait_and_click_button(dev, poco, path_accept_qst): return False
    
    # тыкаем 'умения капитана'
    path_node = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_Xp_captain'
    if not wait_and_click_button(dev, poco, path_node): return False
    time.sleep(1);

    # сообщение 'выбрать умение чтобы его изучить'
    node = wait_for_node_visible(poco, path_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'выбрать умение чтобы его изучить')
        return False
    if not wait_and_click_button(dev, poco, path_back): return False        
    time.sleep(1);

    # пробежимся по всем скилам
    path_root_skills = 'H_Canvas/USER_Main_UI/CONFIG_SKILLS'
    path_learn = 'H_Canvas/USER_Main_UI/CONFIG_SKILLS/Learn(Clone)'
    subpath_skills = ['Some Skill', 'Some Skill (14)', \
                      'Some Skill (1)', 'Some Skill (15)', \
                      'Some Skill (6)', 'Some Skill (20)', \
                      'Some Skill (3)', 'Some Skill (17)', \
                      'Some Skill (4)', 'Some Skill (18)', \
                      'Some Skill (5)', 'Some Skill (19)']
    
    node_root_skills = wait_for_node_visible(poco, path_root_skills, 5)
    if not node_root_skills.exists():
        out('долгое ожидание ноды списка', path_root_skills)
        return False
    
    for subpath in subpath_skills:
        # node = wait_for_node_visible(poco, path_root_skills + '/' + subpath)
        node = get_node_child(node_root_skills, subpath)
        if not node.exists():
            out('скилл не найден', path_root_skills + ' ' + subpath)
            return False
        touch_center(dev, node)
        # snapshot()
        time.sleep(0.5);

    # тыкаем "изучить"
    if not wait_and_click_button(dev, poco, path_learn): return False        

    time.sleep(2);

    # сообщение "вот ваша награда"
    node = wait_for_node_visible(poco, path_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', '"вот ваша награда"')
        return False
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
