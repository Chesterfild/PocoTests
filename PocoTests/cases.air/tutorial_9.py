'''
Created on 20 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from utils import out, wait_for_node_visible, touch_center, \
    wait_and_click_button, pos_center, get_node_child
from airtest.core.api import time, snapshot, swipe
from test_utils import State, find_current_state, go_to_academia


# =============================================================================
def test_tutorial_9(dev, poco):
    out('Tutorial_9 test started...')
    
    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test(dev, poco)
    out('Tutorial_9 test time: ' + str(time.time() - t0)) 

    if not f_ret:
        out('last snapshot')
        snapshot()
    
    return f_ret


# =============================================================================
def run_test(dev, poco, big_test=False):
    path_point_to_buy = 'T_GLOBAL_MAP/EPTown_Black_skull'  # or EPTown_Mothers_TWN
    path_point_to_sell = 'T_GLOBAL_MAP/EPTown_Amelia'  # or EPTown_Grey_Land_CAP
    path_speed_up = 'H_Canvas/USER_Main_UI/SPEED_UP/BTN'
    
    path_back = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'
    path_map = 'H_Canvas/USER_Main_UI/SWITCH_TO_MAP/Button_exit'
    # path_map = 'H_Canvas/USER_Main_UI/MAP_ADDON/SWITCH_TO_WORLD'
    
    path_quests_menu = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_qwest'
    # path_quests_menu_lst = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg'
    path_quest_9 = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (8)'
    path_quest_X = 'H_Canvas/USER_Main_UI/CONFIG_QWESTS/AVR_bg_paper/AVR_bg/A1 (9)'
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
    if not wait_and_click_button(dev, poco, path_quest_9): return False
    # тыкаем принять
    if not wait_and_click_button(dev, poco, path_accept_qst): return False
    
    time.sleep(2)
    
    # сообщение "в городе с зеленым% товары со скидкой"
    node = wait_for_node_visible(poco, path_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'в городе с зеленым% товары со скидкой')
        return False
    if not wait_and_click_button(dev, poco, path_back): return False        

    # тыкаем на город с зеленый "%"
    if not wait_and_click_button(dev, poco, path_point_to_buy): return False        

    # тыкаем на "укорение"
    if not wait_and_click_button(dev, poco, path_speed_up): return False        

    # 10 секунд на доплыть к городу должно хватить
    time.sleep(10)

    # жёдм когда окажемся в городе, имя парсим из кода
    ns = path_point_to_buy.split('_')
    point_name = ns[len(ns) - 1]
    state = find_current_state(poco)
    while state != State.TOWN:
        out('ждём ' + point_name + ' (3 sec)')
        time.sleep(3)
        state = find_current_state(poco)

    # тыкаем "трюм"
    path_trum = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_trum'
    if not wait_and_click_button(dev, poco, path_trum): return False
    
    # тыкаем "магазин"
    path_market = 'H_Canvas/USER_Main_UI/' \
        +'TRUM_STORE_STORAGE/MARKET/CLICKABLE SIZE'
    if not wait_and_click_button(dev, poco, path_market): return False

    # подготавливаем swipe
    path_lst_root = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'ItemsWindow/ScroolArea/ItemList'
    my_swipe(dev, poco, path_lst_root, 'Item4' , 'Item1');

    # выбираем "винтажный портвейн" 
    path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'ItemsWindow/ScroolArea/ItemList/Item8'
    if not wait_and_click_button(dev, poco, path): return False

    # тыкаем купить 1 
    btn_path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'SellWindowBG/SellWindow/SellOne/SellOneBTN'
    if not wait_and_click_button(dev, poco, btn_path): return False

    time.sleep(2)
    
    # сообщение "в городе с красным % товары дороже"
    node = wait_for_node_visible(poco, path_event_reward, 5)
    if not node.exists():
        out('долгое ожидание сообщения', 'в городе с красным % товары дороже')
        return False
    if not wait_and_click_button(dev, poco, path_back): return False        
    
    # тыкаем на город с зеленый "%"
    if not wait_and_click_button(dev, poco, path_point_to_sell): return False        

    # тыкаем на "укорение"
    if not wait_and_click_button(dev, poco, path_speed_up): return False        

    # 10 секунд на доплыть к городу должно хватить
    time.sleep(10)

    # жёдм когда окажемся в городе, имя парсим из кода
    ns = path_point_to_sell.split('_')
    point_name = ns[len(ns) - 1]
    state = find_current_state(poco)
    while state != State.TOWN:
        out('ждём ' + point_name + ' (3 sec)')
        time.sleep(3)
        state = find_current_state(poco)

    # тыкаем "трюм"
    path_trum = 'H_Canvas/USER_Main_UI/CONFIG/AllButtons/Button_trum'
    if not wait_and_click_button(dev, poco, path_trum): return False
    
    # тыкаем на товары на корабле
    path_ship = 'H_Canvas/USER_Main_UI/TRUM_STORE_STORAGE/'\
        +'SHIP/CLICKABLE SIZE'
    if not wait_and_click_button(dev, poco, path_ship): return False

    # подготавливаем swipe
    path_lst_root = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'ItemsWindow/ScroolArea/ItemList'
    my_swipe(dev, poco, path_lst_root, 'Item4' , 'Item1');
    my_swipe(dev, poco, path_lst_root, 'Item7' , 'Item4');
    my_swipe(dev, poco, path_lst_root, 'Item10' , 'Item7');
    my_swipe(dev, poco, path_lst_root, 'Item13' , 'Item10');

    # выбираем "винтажный портвейн" 
    path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'ItemsWindow/ScroolArea/ItemList/Item16'
    if not wait_and_click_button(dev, poco, path): return False

    # тыкаем купить 1 
    btn_path = 'H_Canvas/USER_Main_UI/HOLD_WINDOW/'\
        +'SellWindowBG/SellWindow/SellOne/SellOneBTN'
    if not wait_and_click_button(dev, poco, btn_path): return False

    time.sleep(2)
    
    # out('---- конец теста, дальше недоделанно ----')
    # time.sleep(102);
    # return False

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

    # поплыли в академию
    if not go_to_academia(dev, poco):
        return False
    time.sleep(1)
    
    if big_test:    
        # идем в меню выбора квеста
        if not wait_and_click_button(dev, poco, path_quests_menu): return False
        # тыкаем третий квест
        if not wait_and_click_button(dev, poco, path_quest_X): return False
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
def my_swipe(dev, poco, path_root, subpath_from, subpath_to):
    node_root = wait_for_node_visible(poco, path_root)
    if not node_root.exists():
        out('not ready to swipe, can\'t find node', path_root)
        return False

    node_from = get_node_child(node_root, subpath_from)
    if not node_from.exists():
        out('not ready to swipe, can\'t find node', path_root + '/' + node_from)
        return False
    pos_from = pos_center(dev, node_from)

    node_to = get_node_child(node_root, subpath_to)
    if not node_to.exists():
        out('not ready to swipe, can\'t find node', path_root + '/' + node_to)
        return False
    pos_to = pos_center(dev, node_to)

    swipe(pos_from, pos_to, duration=2)

    return True
    
