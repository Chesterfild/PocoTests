'''
Created on 9 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from utils import out, wait_for_node_visible, touch_center, \
    wait_and_click_button
from airtest.core.api import time, snapshot
from test_utils import State, find_current_state, go_to_academia


# =============================================================================
def test_tutorial_3(dev, poco):
    out('Tutorial_3 test started...')
    
    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test(dev, poco)
    out('Tutorial_3 test time: ' + str(time.time() - t0)) 

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
    btn_quest_3 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (2)'
    btn_quest_4 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (3)'
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
    if not wait_and_click_button(dev, poco, btn_quest_3): return False
    # тыкаем принять
    if not wait_and_click_button(dev, poco, btn_accept_qst): return False
    
    # тыкаем 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_trum'
    btn_trum = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_trum'
    if not wait_and_click_button(dev, poco, btn_trum): return False
    
    # тыкаем купить ядра
    btn_path = 'H_Canvas/USER_Main_UI/TRUM_STORE_STORAGE/'\
        +'MARKET/M_Button_buy_Canonballs'
    if not wait_and_click_button(dev, poco, btn_path): return False

    # выбираем ядра 
    btn_path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'ItemsWindow/ScroolArea/ItemList/Item1'
    if not wait_and_click_button(dev, poco, btn_path): return False

    # выбираем х10 
    btn_path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'SellWindowBG/SellWindow/AmountSelector/Center'
    if not wait_and_click_button(dev, poco, btn_path): return False

    # тыкаем купить 10 
    btn_path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'SellWindowBG/SellWindow/SellOne/SellOneBTN'
    if not wait_and_click_button(dev, poco, btn_path): return False

    # покидаем режим магазина 
    if not wait_and_click_button(dev, poco, btn_back): return False        

    # сообщение "товары можно переместить на склад или продать"
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'товары можно переместить на склад или продать')
        return False
    if not wait_and_click_button(dev, poco, btn_back): return False        

    # тыкаем ядра в трюме
    btn_path = 'H_Canvas/USER_Main_UI/TRUM_STORE_STORAGE/'\
        +'SHIP/T_Button_buy_Canonballs'
    if not wait_and_click_button(dev, poco, btn_path): return False

    # выбираем ядра 
    btn_path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'ItemsWindow/ScroolArea/ItemList/Item1'
    if not wait_and_click_button(dev, poco, btn_path): return False

    # выбираем х10 
    btn_path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'SellWindowBG/SellWindow/AmountSelector/Center'
    if not wait_and_click_button(dev, poco, btn_path): return False

    # тыкаем на склад 10 
    btn_path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'SellWindowBG/SellWindow/SellTen/SellTenBTN'
    if not wait_and_click_button(dev, poco, btn_path): return False

    # сообщение "также можно продать любую вещь"
    node = wait_for_node_visible(poco, wnd_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'также можно продать любую вещь')
        return False
    if not wait_and_click_button(dev, poco, btn_back): return False        
    
    # выбираем ядра 
    btn_path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'ItemsWindow/ScroolArea/ItemList/Item1'
    if not wait_and_click_button(dev, poco, btn_path): return False

    # выбираем х1
    btn_path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'SellWindowBG/SellWindow/AmountSelector/Left'
    if not wait_and_click_button(dev, poco, btn_path): return False

    # тыкаем продать 1 
    btn_path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'SellWindowBG/SellWindow/SellOne/SellOneBTN'
    if not wait_and_click_button(dev, poco, btn_path): return False

    # покидаем режим трюма 
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
        if not wait_and_click_button(dev, poco, btn_quest_4): return False
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
