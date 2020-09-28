'''
Created on 10 мар. 2020 г.

@author: _OttoVonChesterfild_
'''
from utils import out, wait_for_node_visible, touch_center, is_tree_is_visible, get_node_quick,\
    pos_scr2abs, pos_center
from airtest.core.api import time, swipe


# =============================================================================
# =============================================================================
class State:
    NONE = 'NONE'
    LOGO_1 = 'LOGO_1'
    LOGO_2 = 'LOGO_2'
    TERMS_WND = 'TERMS_WND'
    LOADING = 'LOADING'
    MAIN_MENU = 'MAIN_MENU'
    
    SETTINGS = 'SETTINGS'
    SETTINGS_RESET_PROGRESS = 'SETTINGS_RESET_PROGRESS'
    SETTINGS_ACHIVES = 'SETTINGS_ACHIVES'
    
    TUTORIAL = 'TUTORIAL'
    SHOP = 'SHOP'
    
    MAP = 'MAP'
    DAILY_REWARDS = 'DAILY_REWARDS'
    MAP_EVENT_REWARD = 'MAP_EVENT_REWARD'  # окошко задания на глобальной карте
    MAP_JOURNAL = 'MAP_JOURNAL'
    
    TOWN = 'TOWN'

    # SEA = 'SEA'
    # №BATTLE = 'BATTLE'


# =============================================================================
def find_current_state_with_frozen_poco(frozen_poco):
    # меню настроек ставим на первую очередь проверки
    if get_node_quick(frozen_poco, 'H_Canvas/Settings_mobile SYS NEAR END', False).exists():
        if get_node_quick(frozen_poco, 'H_Canvas/Message - MUST BE NEAR END', False).exists():
            return State.SETTINGS_RESET_PROGRESS
        if get_node_quick(frozen_poco, 'H_Canvas/Achieves - SYS NEAR END', False).exists():
            return State.SETTINGS_RESET_PROGRESS
        return State.SETTINGS

    if get_node_quick(frozen_poco, 'H_Canvas/USER_Main_UI/ShopDialog(Clone)', False).exists():
        return State.SHOP

    skip_tutor = get_node_quick(frozen_poco, 'H_Canvas/USER_Main_UI/SKIP_TUTOR_BTN', False)
    if skip_tutor.exists():
        if skip_tutor.attr('visible'):
            return State.TUTORIAL

    map__vt = ['H_Canvas/USER_Main_UI/SPEED_UP',
               'H_Canvas/USER_Main_UI/MAP_ADDON',
               'H_Canvas/USER_Main_UI/BASE_MENU+CHAT',
               'H_Canvas/USER_Main_UI/BASE_PANEL_UP',
               # 'H_Canvas/USER_Main_UI/DailyRewardsContainer',
               'H_Canvas/USER_Main_UI/Daily_Reward_And_Help_Button']    
    if is_tree_is_visible(frozen_poco, map__vt):
        # print("find in MAP")
        # --- находимся в режиме карты, проверим дополнительные окна которые тут бывают
        dr_vt = 'H_Canvas/USER_Main_UI/DailyRewardsContainer/DR_Window(Clone)'
        if get_node_quick(frozen_poco, dr_vt, False):
            return State.DAILY_REWARDS

        if get_node_quick(frozen_poco, 'H_Canvas/USER_Main_UI/EVENT_REVARD', False).exists():
            return State.MAP_EVENT_REWARD

        if get_node_quick(frozen_poco, 'H_Canvas/USER_Main_UI/JOURNAL', False).exists():
            return State.MAP_JOURNAL
        
        return State.MAP

    town__vt = ['H_Canvas/USER_Main_UI/COMPASS',
                'H_Canvas/USER_Main_UI/FRACTION',
                'H_Canvas/USER_Main_UI/INFO_BAR_MOBILE',
                'H_Canvas/USER_Main_UI/SWITCH_TO_MAP',
                'H_Canvas/USER_Main_UI/TOWN_SERVICES',
                'H_Canvas/USER_Main_UI/CONFIG',
                'H_Canvas/USER_Main_UI/JOURN_BTN',
                'H_Canvas/USER_Main_UI/TOP_TITLE',
                'H_Canvas/USER_Main_UI/BASE_MENU+CHAT',
                'H_Canvas/USER_Main_UI/BASE_PANEL_UP',
                'H_Canvas/USER_Main_UI/Daily_Reward_And_Help_Button']    
    if is_tree_is_visible(frozen_poco, town__vt):
        return State.TOWN

    # --- секция начальной загрузки, в конце ибо оптимизация
    menu_cond = get_node_quick(frozen_poco, 'H_Canvas', False).exists()
    menu_cond = menu_cond and not get_node_quick(frozen_poco, 'H_Canvas/USER_Main_UI', False).exists()
    if menu_cond:
        return State.MAIN_MENU
        
    loading__vt = ['H_logos_Canvas/LoadingScreen', 'H_logos_Canvas/ProgressBar']    
    if is_tree_is_visible(frozen_poco, loading__vt):
        return State.LOADING

    terms__vt = ['H_logos_Canvas/TermsOfUseWindow']    
    if is_tree_is_visible(frozen_poco, terms__vt):
        return State.TERMS_WND
    
    logo2__vt = ['H_logos_Canvas/Image_logo_2']    
    if is_tree_is_visible(frozen_poco, logo2__vt):
        return State.LOGO_2

    logo1__vt = ['H_logos_Canvas/Image_logo_1']    
    if is_tree_is_visible(frozen_poco, logo1__vt):
        return State.LOGO_1
    
    return State.NONE


# =============================================================================
def find_current_state(poco):
    # poco = UnityPoco()
    if poco == None:
        return State.NONE
    with poco.freeze() as frozen_poco:
        state = find_current_state_with_frozen_poco(frozen_poco)
        return state    


# =============================================================================
# =============================================================================
btn_academy_on_map = 'T_GLOBAL_MAP/EPTown_t_academy_name'

btn_mail = 'H_Canvas/USER_Main_UI/TOWN_SERVICES/MAIL'
btn_back = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'


# =============================================================================
def go_to_academia(dev, poco):
    out('нажимаем кнопку Академия')
    node = wait_for_node_visible(poco, btn_academy_on_map, 5)
    if not node.exists():
        out('Button not showed', btn_academy_on_map)
        return False
    touch_center(dev, node)
    time.sleep(1)
    
    state = find_current_state(poco)
    while state != State.TOWN:
        out('ждём академию (3 sec)')
        time.sleep(3)
        state = find_current_state(poco)

    # todo: иногда бывает сообщение о жаловании для команды
    # потом отловить момент и сделать тест
    
    # если почта, собираем
    node = wait_for_node_visible(poco, btn_mail, 1)
    if node.exists():
        touch_center(dev, node)
        time.sleep(1)
        node = wait_for_node_visible(poco, btn_back, 5)
        if not node.exists():
            out('Button not showed', btn_back)
            return False
        touch_center(dev, node)
        time.sleep(1)
        
    return True
    
# ================================================================
def rotate_cam_to(dev, poco, node_path, log_out=False):
    #node_path = 'Rank2(Clone)/MARKER_NEW(Clone)/10-MobileRelationsMark'
    pos_from = pos_scr2abs(dev, [0.5, 0.1])
    
    f_exit = False
    i = 0
    while not f_exit:
        pos_scr = [0,0.2]
        #pos_abs = pos_scr2abs(dev, pos_scr)

        node_case_lod = wait_for_node_visible(poco, node_path)
        if node_case_lod.exists():
            if log_out:
                out(node_path+' exists...')
            pos_scr = pos_center(dev, node_case_lod, False)
            #pos_abs = pos_scr2abs(dev, pos_scr)
        
        step = 0.1

        if pos_scr[0]>0.48 and pos_scr[0]<0.52:
            step = 0.0
            f_exit = True
        
        if pos_scr[0]<0.48 or pos_scr[0]>0.52:
            step = 0.03
        if pos_scr[0]<0.40 or pos_scr[0]>0.60:
            step = 0.05
        if pos_scr[0]<0.30 or pos_scr[0]>0.70:
            step = 0.1
        
        print('position:'+str(pos_scr))
        
        if pos_scr[0] > 0.5:
            swipe(pos_from, vector=[step,0], duration=1)
            if log_out:
                out('swipe to left on '+str(step))
        if pos_scr[0] < 0.5:
            swipe(pos_from, vector=[-step,0], duration=1)
            if log_out:
                out('swipe to right on '+str(step))
        i += 1
        if i>30:
            if log_out:
                out('долгое ожидание поворота к обьекту', node_path)
            return False 
        
        
    out('it: '+str(i))
    return True 


