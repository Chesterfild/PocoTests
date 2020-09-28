'''
Created on 8 апр. 2020 г.

@author: _OttoVonChesterfild_
'''

from airtest.core.api import time, snapshot
from utils import out, wait_for_node_visible, touch_center, get_node_child
from test_utils import State, find_current_state

# =============================================================================
btn_journal = 'H_Canvas/USER_Main_UI/JOURN_BTN/Avr_bg/AVR_Journal'
btn_back = 'H_Canvas/USER_Main_UI/BACK_BUTTON_MOBILE'

wnd_journal = 'H_Canvas/USER_Main_UI/JOURNAL'
# poco("Btn_Qwests")poco("Btn_Legend")poco("Btn_Immuschestwo")poco("Btn_Status")poco("Btn_Stats")
btn_quests = 'Btn_Qwests'
btn_legends = 'Btn_Legend'
btn_goods = 'Btn_Immuschestwo'
btn_status = 'Btn_Status'
btn_stats = 'Btn_Stats'

wnd_quests = 'Current_Tasks'
wnd_legends = 'Legends_log'
wnd_goods = 'Immuschestwo'
wnd_status = 'Status'
wnd_stats = 'Statistic'

js_unknow = 'STATE_UNKNOW' 
js_quests = 'STATE_QUESTS' 
js_legends = 'STATE_LEGENDS' 
js_goods = 'STATE_GOODS'
js_status = 'STATE_STATUS' 
js_stats = 'STATE_STATS' 


# =============================================================================
def test_journal(dev, poco):
    out('Journal test started...')

    f_ret = False
    t0 = time.time();
    state = find_current_state(poco)
    if state == State.MAP: 
        f_ret = run_test_journal(dev, poco)
    out('Journal test time: ' + str(time.time() - t0)) 
    
    if not f_ret:
        out('last snapshot')
        snapshot()
    
    return f_ret


# =============================================================================
def run_test_journal(dev, poco):
    
    out("нажимаем кнопку journal")
    node = wait_for_node_visible(poco, btn_journal, 5)
    if not node.exists():
        out('Button not showed', btn_journal)
        return False
    touch_center(dev, node)
    time.sleep(1)

    # проверочка
    node = wait_for_node_visible(poco, wnd_journal, 2)
    if not node.exists():
        out('Window not showed', wnd_journal)
        return False

    ### ---------------------------------------   

    # '''    
    out('Тестируем вкладку Квестов')
    if not test_journal_quests(dev, poco):
        return False

    out('Тестируем вкладку Легенд')
    if not test_journal_legends(dev, poco):
        return False
    
    out('Тестируем вкладку имущества')
    if not test_journal_goods(dev, poco):
        return False
    # '''

    out('Тестируем вкладку статуса игрока')
    if not test_journal_status(dev, poco):
        return False

    out('Тестируем вкладку статистики')
    if not test_journal_stats(dev, poco):
        return False

    ### ---------------------------------------    
        
    out('нажимаем кнопку выхода из окна журнала')
    node = wait_for_node_visible(poco, btn_back, 5)
    if not node.exists():
        out('Button not showed', btn_back)
        return False
    touch_center(dev, node)
    time.sleep(1)

    return True


# =============================================================================
def get_journal_state(node_wnd_journal):
    if get_node_child(node_wnd_journal, wnd_quests, False).exists():
        return js_quests;
    if get_node_child(node_wnd_journal, wnd_legends, False).exists():
        return js_legends;
    if get_node_child(node_wnd_journal, wnd_goods, False).exists():
        return js_goods;
    if get_node_child(node_wnd_journal, wnd_status, False).exists():
        return js_status;
    if get_node_child(node_wnd_journal, wnd_stats, False).exists():
        return js_stats;

    return js_unknow


# =============================================================================
def test_journal_quests(dev, poco):
    
    node_wnd_journal = wait_for_node_visible(poco, wnd_journal, 2)
    if not node_wnd_journal.exists():
        out('Window not showed', wnd_journal)
        return False    
    
    if get_journal_state(node_wnd_journal) != js_quests:
        out('переходим во вкладку квестов')
        touch_center(dev, get_node_child(node_wnd_journal, btn_quests))
        time.sleep(1)

    # получаем заново, т.к. сцена обновилась
    node_wnd_journal = wait_for_node_visible(poco, wnd_journal, 2)
    if not node_wnd_journal.exists():
        out('Window not showed', wnd_journal)
        return False    

    if get_journal_state(node_wnd_journal) != js_quests:
        out('не перешли во вкладку квестов', '')
        return False

    ### ------------------------------------------------------------

    node_tasks_list = get_node_child(node_wnd_journal, wnd_quests)

    # перебераем всё по замороженной структуре
    i = 0
    for node_quest in node_tasks_list.child():
        if node_quest.attr('type') == 'Button':
            i = i + 1
            out('quest[' + str(i) + ']: ' + node_quest.attr('text'))
            touch_center(dev, node_quest)
            time.sleep(0.5)
            # новый экземпляр ибо опять всё обновилось
            # journal = wait_for_node_visible(poco, wnd_journal, 2)
            # node = get_node_child(journal, wnd_descr)
            # out('quest descr: ' + node.attr('text'))

    return True


# =============================================================================
def test_journal_legends(dev, poco):

    node_wnd_journal = wait_for_node_visible(poco, wnd_journal, 2)
    if not node_wnd_journal.exists():
        out('Window not showed', wnd_journal)
        return False    
    
    if get_journal_state(node_wnd_journal) != js_legends:
        out('переходим во вкладку легенд')
        touch_center(dev, get_node_child(node_wnd_journal, btn_legends))
        time.sleep(1)

    # получаем заново, т.к. сцена обновилась
    node_wnd_journal = wait_for_node_visible(poco, wnd_journal, 2)
    if not node_wnd_journal.exists():
        out('Window not showed', wnd_journal)
        return False    

    if get_journal_state(node_wnd_journal) != js_legends:
        out('не перешли во вкладку легенд', '')
        return False

    ### ------------------------------------------------------------

    node_legends_list = get_node_child(node_wnd_journal, wnd_legends)

    # перебераем всё по замороженной структуре
    i = 0
    for node_quest in node_legends_list.child():
        if node_quest.attr('type') == 'Button':
            i = i + 1
            out('legend[' + str(i) + ']: ' + node_quest.attr('text'))
            touch_center(dev, node_quest)
            time.sleep(0.5)
            # новый экземпляр ибо опять всё обновилось
            # journal = wait_for_node_visible(poco, wnd_journal, 2)
            # node = get_node_child(journal, wnd_descr)
            # out('quest descr: ' + node.attr('text'))

    return True


# =============================================================================
def test_journal_goods(dev, poco):

    node_btn_back = wait_for_node_visible(poco, btn_back, 2)
    wnd_goods_opt = wnd_journal + '/' + wnd_goods
    
    node_wnd_journal = wait_for_node_visible(poco, wnd_journal, 2)
    if not node_wnd_journal.exists():
        out('Window not showed', wnd_journal)
        return False    
    
    if get_journal_state(node_wnd_journal) != js_goods:
        out('переходим во вкладку имущества')
        touch_center(dev, get_node_child(node_wnd_journal, btn_goods))
        time.sleep(1)

    # получаем заново, т.к. сцена обновилась
    node_wnd_journal = wait_for_node_visible(poco, wnd_journal, 2)
    if not node_wnd_journal.exists():
        out('Window not showed', wnd_journal)
        return False    

    if get_journal_state(node_wnd_journal) != js_goods:
        out('не перешли во вкладку имущества', '')
        return False

    ### ------------------------------------------------------------
    node_wnd_goods = wait_for_node_visible(poco, wnd_goods_opt, 2)
    node_btn_trum = get_node_child(node_wnd_goods, 'Trum')
    # node_btn_sklads = get_node_child(node_wnd_goods, 'Sklads')
    # node_btn_WhereToBuy = get_node_child(node_wnd_goods, 'WhereToBuy')

    # out('click:' + node_btn_trum.attr('text'))
    touch_center(dev, node_btn_trum)

    node_wnd_goods = wait_for_node_visible(poco, wnd_goods_opt, 2)
    items = node_wnd_goods.offspring('Towars')
    if len(items) > 0:
        i = 0
        for item in items:
            i = i + 1
            if i < 3:
                touch_center(dev, item)
                time.sleep(0.5)
                touch_center(dev, node_btn_back)
                time.sleep(0.5)
    else:
        out('trum list is empty')

    ### ------------------------------------------------------------
    node_wnd_goods = wait_for_node_visible(poco, wnd_goods_opt, 2)
    # node_btn_trum = get_node_child(node_wnd_goods, 'Trum')
    node_btn_sklads = get_node_child(node_wnd_goods, 'Sklads')
    # node_btn_WhereToBuy = get_node_child(node_wnd_goods, 'WhereToBuy')

    # out('click:' + node_btn_trum.attr('text'))
    touch_center(dev, node_btn_sklads)

    node_wnd_goods = wait_for_node_visible(poco, wnd_goods_opt, 2)
    items = node_wnd_goods.offspring('Towars')
    if len(items) > 0:
        i = 0
        for item in items:
            i = i + 1
            if i < 3:
                touch_center(dev, item)
                time.sleep(0.5)
                touch_center(dev, node_btn_back)
                time.sleep(0.5)
    else:
        out('sklads list is empty')

    ### ------------------------------------------------------------
    node_wnd_goods = wait_for_node_visible(poco, wnd_goods_opt, 2)
    # node_btn_trum = get_node_child(node_wnd_goods, 'Trum')
    # node_btn_sklads = get_node_child(node_wnd_goods, 'Sklads')
    node_btn_WhereToBuy = get_node_child(node_wnd_goods, 'WhereToBuy')

    # out('click:' + node_btn_trum.attr('text'))
    touch_center(dev, node_btn_WhereToBuy)

    node_wnd_goods = wait_for_node_visible(poco, wnd_goods_opt, 2)
    items = node_wnd_goods.offspring('Towars')
    if len(items) > 0:
        i = 0
        for item in items:
            i = i + 1
            if i < 3:
                touch_center(dev, item)
                time.sleep(0.5)
                touch_center(dev, node_btn_back)
                time.sleep(0.5)
    else:
        out('WhereToBuy list is empty')

    return True


# =============================================================================
def test_journal_status(dev, poco):
    
    btn_hawk = 'HAWK'
    btn_baran = 'BARAN'
    btn_spider = 'SPIDER'
    btn_rabbit = 'RABBIT'
    btn_snake = 'SNAKE'
    
    node_wnd_journal = wait_for_node_visible(poco, wnd_journal, 2)
    if not node_wnd_journal.exists():
        out('Window not showed', wnd_journal)
        return False    
    
    if get_journal_state(node_wnd_journal) != js_status:
        out('переходим во вкладку статуса игрока')
        touch_center(dev, get_node_child(node_wnd_journal, btn_status))
        time.sleep(1)

    # получаем заново, т.к. сцена обновилась
    node_wnd_journal = wait_for_node_visible(poco, wnd_journal, 2)
    if not node_wnd_journal.exists():
        out('Window not showed', wnd_journal)
        return False    

    if get_journal_state(node_wnd_journal) != js_status:
        out('не перешли во вкладку статуса игрока', '')
        return False

    ### ------------------------------------------------------------

    node_wnd_status = get_node_child(node_wnd_journal, wnd_status)

    touch_center(dev, get_node_child(node_wnd_status, btn_hawk))
    time.sleep(0.5)
    touch_center(dev, get_node_child(node_wnd_status, btn_baran))
    time.sleep(0.5)
    touch_center(dev, get_node_child(node_wnd_status, btn_spider))
    time.sleep(0.5)
    touch_center(dev, get_node_child(node_wnd_status, btn_rabbit))
    time.sleep(0.5)
    touch_center(dev, get_node_child(node_wnd_status, btn_snake))
    time.sleep(0.5)

    return True


# =============================================================================
def test_journal_stats(dev, poco):
    
    node_wnd_journal = wait_for_node_visible(poco, wnd_journal, 2)
    if not node_wnd_journal.exists():
        out('Window not showed', wnd_journal)
        return False    
    
    if get_journal_state(node_wnd_journal) != js_stats:
        out('переходим во вкладку статистики')
        touch_center(dev, get_node_child(node_wnd_journal, btn_stats))
        time.sleep(1)

    # получаем заново, т.к. сцена обновилась
    node_wnd_journal = wait_for_node_visible(poco, wnd_journal, 2)
    if not node_wnd_journal.exists():
        out('Window not showed', wnd_journal)
        return False    

    if get_journal_state(node_wnd_journal) != js_stats:
        out('не перешли во вкладку статистики', '')
        return False

    ### ------------------------------------------------------------
    # тут тестов по сути нет, просто переход на вкладку

    return True

