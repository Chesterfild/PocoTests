'''
Created on 9 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from utils import out, wait_for_node_visible, touch_center, \
    wait_and_click_button, get_node_child, pos_center
from airtest.core.api import time, swipe, snapshot
from test_utils import State, find_current_state, go_to_academia
from time import sleep


# =============================================================================
def test_tutorial_2(dev, poco):
    out('Tutorial_2 test started...')
    
    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test_tutorial_2(dev, poco)
    out('Tutorial_2 test time: ' + str(time.time() - t0)) 

    if not f_ret:
        out('last snapshot')
        snapshot()
    
    return f_ret


# =============================================================================
def run_test_tutorial_2(dev, poco, big_test=False):
    btn_back = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'
    btn_map = 'H_Canvas/USER_Main_UI/SWITCH_TO_MAP/Button_exit'
    # btn_map = 'H_Canvas/USER_Main_UI/MAP_ADDON/SWITCH_TO_WORLD'
    
    btn_quests_menu = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_qwest'
    # wnd_quests_menu_lst = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg'
    btn_quest_2 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (1)'
    btn_quest_3 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (2)'
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
    if not wait_and_click_button(dev, poco, btn_quest_2): return False
    # тыкаем принять
    if not wait_and_click_button(dev, poco, btn_accept_qst): return False
    
    # тыкаем 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_team'
    btn_team = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_team'
    if not wait_and_click_button(dev, poco, btn_team): return False
    
    # сообщение "Сначала наймем команду"
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'нет сообщения "Сначала наймем команду"')
        return False
    if not wait_and_click_button(dev, poco, btn_back): return False

    # тыкаем 'H_Canvas/USER_Main_UI/CONFIG_TEAM_MOBILE/TeamManageShipMobile/ScrollingPanel/TavernButton'
    btn_tavern = 'H_Canvas/USER_Main_UI/CONFIG_TEAM_MOBILE/'\
        +'TeamManageShipMobile/ScrollingPanel/TavernButton'
    if not wait_and_click_button(dev, poco, btn_tavern): return False

    # сообщение "Найми 7 салаг."
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'нет сообщения "Найми 7 салаг."')
        return False
    if not wait_and_click_button(dev, poco, btn_back): return False

    # тыкаем 7 раз на салагу "+" 
    # 'H_Canvas/USER_Main_UI/CONFIG_TEAM_MOBILE/TeamManageShipMobile/ScrollingPanel/TavernButton'
    btn_crewman_hire_0 = 'H_Canvas/USER_Main_UI/CONFIG_TEAM_MOBILE/'\
        +'TeamManageTavernMobile/TavernBgImage/Crewman_Hire_0/ActionButton'
    i = 7
    while i > 0:
        if not wait_and_click_button(dev, poco, btn_crewman_hire_0): return False
        i -= 1
    # тыкаем кнопку назад
    if not wait_and_click_button(dev, poco, btn_back): return False
        
    # сообщение "перетащите 2х матросов на паруса"
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'перетащите 2х матросов на паруса')
        return False
    if not wait_and_click_button(dev, poco, btn_back): return False        
        
    # подготавливаемся к свайпам
    sn_tmp = 'H_Canvas/USER_Main_UI/CONFIG_TEAM_MOBILE/'\
        +'TeamManageShipMobile/ScrollingPanel/ShipDecks'
    sn_parus = 'ParuDeck/CrewmanDeck_Paru_3'
    sn_aboard = 'AboardDeck/CrewmanDeck_Aboard_3'
    sn_cannon = 'CanonDeck/CrewmanDeck_Canon_3'
    sn_from = 'AboardDeck/CrewmanDeck_Aboard_0'

    node_tmp = wait_for_node_visible(poco, sn_tmp, 5)
    pos_parus = get_node_child(node_tmp, sn_parus).attr('pos')
    pos_aboard = get_node_child(node_tmp, sn_aboard).attr('pos')
    pos_cannon = get_node_child(node_tmp, sn_cannon).attr('pos')
    
    pos_abs_from = pos_center(dev, get_node_child(node_tmp, sn_from))
    
    # перетаскиваем 2х матросов на паруса
    vec = [0, pos_parus[1] - pos_aboard[1]]
    print('vector ', pos_abs_from, vec)
    swipe(pos_abs_from, vector=vec, duration=3)
    sleep(1)
    swipe(pos_abs_from, vector=vec, duration=3)
    sleep(1)

    # сообщение "перетащите 2х матросов на паруса"
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'перетащите 2х матросов на пушки')
        return False
    if not wait_and_click_button(dev, poco, btn_back): return False        

    # перетаскиваем 2х матросов на пушки
    vec = [0, pos_cannon[1] - pos_aboard[1]]
    print('vector ', pos_abs_from, vec)
    swipe(pos_abs_from, vector=vec, duration=3)
    sleep(1)
    swipe(pos_abs_from, vector=vec, duration=3)
    sleep(1)

    # сообщение "больше матросов на палубе, больше эффективность"
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'больше матросов на палубе, больше эффективность')
        return False
    if not wait_and_click_button(dev, poco, btn_back): return False        

    # тыкаем на кнопку "Раненые" 
    btn_med = 'H_Canvas/USER_Main_UI/CONFIG_TEAM_MOBILE/'\
        +'TeamManageShipMobile/ScrollingPanel/MedbayButton'
    if not wait_and_click_button(dev, poco, btn_med): return False

    # тыкаем на кнопку "лечить матроса" 
    btn_med = 'H_Canvas/USER_Main_UI/CONFIG_TEAM_MOBILE/'\
        +'TeamManageShipMobile/ScrollingPanel/ShipDecks/'\
        +'Medbay/Crewman_Wounded_1/ActionButton'
    if not wait_and_click_button(dev, poco, btn_med): return False

    # сообщение "про офицеров, выбрать"
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'про офицеров, выбрать')
        return False
    if not wait_and_click_button(dev, poco, btn_back): return False        

    # тыкаем на кнопку "слот офицера 1" 
    btn_med = 'H_Canvas/USER_Main_UI/CONFIG_TEAM_MOBILE/'\
        +'TeamManageShipMobile/ScrollingPanel/RightPanel/'\
        +'DeckStats_Paru/BorderImage/OfficerSlotsPanel/OfficerSlot1'
    if not wait_and_click_button(dev, poco, btn_med): return False
    
    # тыкаем на кнопку "боцман" 
    btn_med = 'H_Canvas/USER_Main_UI/CONFIG_TEAM_MOBILE/'\
        +'TeamManageShipMobile/OfficersWindow/BgImage/'\
        +'BorderImage/SlotsPanel/OfficerSlot1'
    if not wait_and_click_button(dev, poco, btn_med): return False

    # тыкаем на кнопку "назначить" 
    btn_med = 'H_Canvas/USER_Main_UI/CONFIG_TEAM_MOBILE/'\
        +'TeamManageShipMobile/OfficersWindow/BgImage/'\
        +'BorderImage/ActionButton(Clone)'
    if not wait_and_click_button(dev, poco, btn_med): return False

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
        if not wait_and_click_button(dev, poco, btn_quest_3): return False
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
