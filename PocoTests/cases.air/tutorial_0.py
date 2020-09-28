'''
Created on 20 мар. 2020 г.

@author: _OttoVonChesterfild_
'''

from airtest.core.api import time, snapshot
from utils import out, wait_for_node_visible, touch_center,\
    wait_and_click_button
from test_utils import State, find_current_state


# =============================================================================
def test_tutorial_0(dev, poco):
    out('Tutorial_0 test started...')

    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        if reset_progress(dev, poco):
            f_ret = run_test_tutorial(dev, poco)
    else :
        if state == State.TUTORIAL:
            f_ret = run_test_tutorial(dev, poco)
            
    out("Tutorial_0 test time: " + str(time.time() - t0)) 
    
    if not f_ret:
        out('last snapshot')
        snapshot()
    
    if not f_ret:
        skip_tutorial_0(dev, poco)

    return f_ret


# =============================================================================
def skip_tutorial_0(dev, poco):
    out('try go to global map...')
    skip_btn = 'H_Canvas/USER_Main_UI/SKIP_TUTOR_BTN'
    node = wait_for_node_visible(poco, skip_btn, 5)
    if not node.exists():
        out('Button not showed', skip_btn)
    else: 
        touch_center(dev, node)
        apply_btn = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'
        node = wait_for_node_visible(poco, apply_btn, 5)
        if not node.exists():
            out('Button not showed', apply_btn)
        else: 
            touch_center(dev, node)
    

# =============================================================================
def run_test_tutorial(dev, poco):
    
    info_wnd = 'H_Canvas/USER_Main_UI/EVENT_REVARD'
    back_btn = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'
    shoot_btn = 'H_Canvas/USER_Main_UI/FIGHT_PANEL/SHOOT_Manual'
    shoot_hilighter = 'H_Canvas/USER_Main_UI/HIGHLIGHT_INTERFACE' 
    
    out("... На горизонте появилось судно")
    time.sleep(15)
    node = wait_for_node_visible(poco, info_wnd, 5)
    if not node.exists():
        out('долгое ожидание сообщения', '... На горизонте появилось судно')
        return False
    if not wait_and_click_button(dev, poco, back_btn): return False
    
    time.sleep(10)

    out("Чтобы выстрелить, нажмите на подсвеченную кнопку.")
    node = wait_for_node_visible(poco, info_wnd, 5)
    if not node.exists():
        out('долгое ожидание сообщения', "Чтобы выстрелить, нажмите на подсвеченную кнопку.")
        return False
    if not wait_and_click_button(dev, poco, back_btn): return False

    out("тыкаем кнопку стрельбы 1 раз")
    node = wait_for_node_visible(poco, shoot_btn, 5, True)
    node_a = wait_for_node_visible(poco, shoot_hilighter, 5)
    if not node.exists() or not node_a.exists():
        out('Button ' + shoot_btn + ' not showed', 'тыкаем кнопку стрельбы 1 раз')
        return False
    touch_center(dev, node)
    
    time.sleep(3)
    
    out("Противник обездвижен! ...")
    node = wait_for_node_visible(poco, info_wnd, 5)
    if not node.exists():
        out('долгое ожидание сообщения', "Противник обездвижен! ...")
        return False
    if not wait_and_click_button(dev, poco, back_btn): return False
    
    out("ждём перезарядки")
    time.sleep(5)
    
    out("тыкаем кнопку стрельбы")
    node = wait_for_node_visible(poco, shoot_btn, 5, True)
    node_a = wait_for_node_visible(poco, shoot_hilighter, 5)
    if not node.exists() or not node_a.exists():
        out('Button ' + shoot_btn + ' not showed', 'тыкаем кнопку стрельбы')
        return False
    touch_center(dev, node)

    time.sleep(5)

    out("Чем дольше враг остается в зоне прицеливания, тем точнее выстрел.")
    node = wait_for_node_visible(poco, info_wnd, 5)
    if not node.exists():
        out('долгое ожидание сообщения', "Чем дольше враг остается в зоне прицеливания, тем точнее выстрел.")
        return False
    if not wait_and_click_button(dev, poco, back_btn): return False

    time.sleep(5)

    out("Мы потопили врага, но капитан пиратского судна перед смертью призвал жуткую тварь из глубин океана.")
    node = wait_for_node_visible(poco, info_wnd, 5)
    if not node.exists():
        out('долгое ожидание сообщения', "Мы потопили врага")
        return False
    if not wait_and_click_button(dev, poco, back_btn): return False

    out("ждём на потопление корабля и загрузку в глобальную карту 20 сек")
    time.sleep(20)
    
    out("проверяем что оказались на глобальной карте")
    state = find_current_state(poco)
    while state == State.NONE or state == State.TUTORIAL:
        time.sleep(3)
        state = find_current_state(poco)
        out('state: ' + state)
        
    if state == State.MAP or state == State.MAP_EVENT_REWARD: 
        out('Tutorial Complete')
    else :
        out('Incorrect state on exit tutorial', "tutorial test failed")
        return False

    return True


# =============================================================================
def wait_for_button_and_touch(dev, poco, path):
    node = wait_for_node_visible(poco, path, 5)
    if node.exists():
        # тыкаем в кнопку
        touch_center(dev, node)
        time.sleep(1)
    else:
        out('Can\'t press button', path)
        return False

    return True


# =============================================================================
def reset_progress(dev, poco):
    out('Reset progress test started...')
    
    path = 'H_Canvas/USER_Main_UI/BASE_MENU+CHAT/Avr_bg/Avr_pause'
    if not (wait_for_button_and_touch(dev, poco, path)):
        return False
    
    path = 'H_Canvas/Settings_mobile SYS NEAR END/AVR_bg/ButtonsPanel/ResetSaveButton'
    if not (wait_for_button_and_touch(dev, poco, path)):
        return False
    
    # надо подтвердить сброс прогресса
    path = 'H_Canvas/Message - MUST BE NEAR END/AVR_bg_paper/AVR_bg/BtnPanel/Btn_1'
    if not (wait_for_button_and_touch(dev, poco, path)):
        return False
    
    # ждём на загрузку тутора 10 сек 
    out('Wait for Loading Tutor 10 sec.')
    time.sleep(10)
    
    out('Reset progress test complete.')
    return True
