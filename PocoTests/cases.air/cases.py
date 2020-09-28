'''
Created on 10 мар. 2020 г.

@author: _OttoVonChesterfild_
'''
import time
from os.path import os
# import os

# from airtest.core.api import time
from poco.drivers.unity3d import UnityPoco
from airtest.core.api import shell, clear_app, device, stop_app, wake, start_app,\
    init_device
from airtest.core.android import Android
from airtest.core.helper import set_logdir
from airtest.utils.compat import script_dir_name
from airtest.report.report import simple_report

from utils import out, get_node_quick, touch_center
from test_utils import State, find_current_state

# ## тесты, импортируем только самые главные методы 
# ## (чтобы скрыть внутринности тестов)
from z_sleep_test import test_z_sleep_test

from daily_rewards import test_daily_rewards
from journal import test_journal
from faction import test_faction

from tutorial_0 import test_tutorial_0
from tutorial_1 import test_tutorial_1
from tutorial_2 import test_tutorial_2
from tutorial_3 import test_tutorial_3
from tutorial_5 import test_tutorial_5
from tutorial_6 import test_tutorial_6
from tutorial_7 import test_tutorial_7
from tutorial_8 import test_tutorial_8
from tutorial_9 import test_tutorial_9
from tutorial_10 import test_tutorial_10


# =============================================================================
class Cases:
    DAILY_REWARDS = 'daily_rewards'
    JOURNAL = 'journal'
    FACTION = 'faction'
    
    TUTORIAL_0 = 'tutorial_0'
    
    TUTORIAL_1 = 'tutorial_1'
    TUTORIAL_2 = 'tutorial_2'
    TUTORIAL_3 = 'tutorial_3'
    # TUTORIAL_4 = 'tutorial_4'
    TUTORIAL_5 = 'tutorial_5'
    TUTORIAL_6 = 'tutorial_6'
    TUTORIAL_7 = 'tutorial_7'
    TUTORIAL_8 = 'tutorial_8'
    TUTORIAL_9 = 'tutorial_9'
    TUTORIAL_10 = 'tutorial_10'

    Z_SLEEP_TEST = 'z_sleep_test'

        
# =============================================================================
# тесты 
# =============================================================================
def tests_runner(main_script, file_config):
    # читаем конфиг из config-файла
    package, data_config = read_data_from_config(file_config)
    gl_report = []

    # на сколько я понял это каждый раз открывает новое соединение
    
    '''
    # подключаемся к девайсу
    if run_on_emulator: # для эмулятора
        init_device(platform='Android', cap_method='JAVACAP', ori_method='ADBORI')
    else: # для девайса
        init_device(platform='Android')
        log('Init Device')
    '''
    init_device(platform='Android')
    dev = device()
    poco = UnityPoco()

    # вроде всё готово для тестов:
    t0 = time.time();
    out('Cases::tests_runner()... started')
    
    # выставляем значения по умолчанию потому что предыдущего теста не было
    last_test_stop_app = False
    need_wake = True
    # for line in data_csv:
    for line in data_config:
        # из config-файла
        test_id, f_wake, f_stop_before, f_clear_app, f_push_saves, \
        f_start_app, f_stop_after = parse_line_from_config(line)
    
        if need_wake:
            f_wake = True
            need_wake = False
    
        if last_test_stop_app:
            f_stop_before = True
            f_start_app = True
            last_test_stop_app = False
    
        # создаём логирование
        log_path = 'report(' + test_id + ')'
        set_logdir(log_path)
    
        #  пробуждаем устройство
        if f_wake: 
            wake()
            
        #  останавливаем приложение
        if f_stop_before: 
            stop_app(package);
            time.sleep(1)

        #  отчистить даные приложения            
        if f_clear_app: 
            clear_app(package)
            
        #  подсовываем сэйвы
        if f_push_saves != '': 
            push_my_saves(f_push_saves, package)
            
        #  стартуем приложение
        if f_start_app: 
            start_app(package)
            time.sleep(10)
            poco = UnityPoco()

        # запускаем тест
        tt0 = time.time();
        result, runned = test_runner(dev, poco, test_id)
        dtt = time.time() - tt0
        print('test: ' + test_id + '; ' + \
              'runned: ' + str(runned) + '; ' + \
              'result: ' + str(result) + '; ' + \
              'time(sec): ' + str(int(dtt)))
        print('-----------------------')
        if not result:
            last_test_stop_app = True
            f_stop_after = True
        gl_report.append([test_id, runned, result, dtt])
        
        #  останавливаем приложение
        if f_stop_after: 
            last_test_stop_app = True
            stop_app(package)
            
        # далее обязательная секция чтобы сгенерить отчёт
        report_path = get_log_path(main_script, log_path)
        print(report_path)
        simple_report(main_script, report_path, output='report(' + test_id + ').html')

    t1 = time.time()
    out('Cases::tests_runner()... complete (' + str(t1 - t0) + ' sec)')

    # заключительный репорт gl_report
    log_path = 'report'
    set_logdir(log_path)

    for gl_data in gl_report:
        txt = gl_data[0] + ' '
        prop = ''
        if not gl_data[1]:
            prop += 'тест не найден'
        else:
            txt += '(' + str(int(gl_data[3])) + ' sec)'
            if not gl_data[2]:
                prop += 'тест не пройден'
        out(txt, prop)

    # далее обязательная секция чтобы сгенерить отчёт
    report_path = get_log_path(main_script, log_path)
    print(report_path)
    simple_report(main_script, report_path, output='global_report.html')


# =============================================================================
# запуск теста 
# =============================================================================
def test_runner(dev, poco, test_id):
    
    f_exit = False
    while not f_exit:
        state = find_current_state(poco)
        print('test_runner()::state: ' + state)
        if state == State.NONE:
            time.sleep(10)

        if state == State.LOGO_1 or state == State.LOGO_2:
            time.sleep(1)
             
        if state == State.TERMS_WND: 
            # touch_node(dev, poco, 'H_logos_Canvas/TermsOfUseWindow/AcceptButton')
            poco('AcceptButton').click()
            time.sleep(1)
            
        if state == State.LOADING: 
            time.sleep(10)
            
        if state == State.MAIN_MENU:
            time.sleep(5)
            
        if state == State.SETTINGS:
            touch_node(dev, poco, 'H_Canvas/USER_Main_UI/BASE_MENU+CHAT/Avr_bg/Avr_pause');

        if state == State.MAP_EVENT_REWARD:
            touch_node(dev, poco, 'H_Canvas/USER_Main_UI/BASE_MENU+CHAT/Avr_bg/Avr_pause');
            time.sleep(1)

        if state == State.DAILY_REWARDS:
            touch_node(dev, poco, 'H_Canvas/USER_Main_UI/BASE_MENU+CHAT/Avr_bg/Avr_pause');
            time.sleep(1)

        # пока единственное исключение из правил
        if state == State.TUTORIAL and test_id == Cases.TUTORIAL_0:
            # считаем что мы готовы к запуску теста
            result, runned = run_test(dev, poco, test_id)
            if not runned:
                out('тест не найден', 'test_id: ' + test_id)
            return result, runned
            
        # --------------------------------------
        if state == State.MAP:
            # считаем что мы готовы к запуску теста
            result, runned = run_test(dev, poco, test_id)
            if not runned:
                out('тест не найден', 'test_id: ' + test_id)
            return result, runned
            
            
# ================================================================
def run_test(dev, poco, test_id):
    out('test_id: ' + test_id)
    if test_id == Cases.Z_SLEEP_TEST: return test_z_sleep_test(dev, poco), True
    
    if test_id == Cases.DAILY_REWARDS: return test_daily_rewards(dev, poco), True
    if test_id == Cases.JOURNAL: return test_journal(dev, poco), True
    if test_id == Cases.FACTION: return test_faction(dev, poco), True

    if test_id == Cases.TUTORIAL_0: return test_tutorial_0(dev, poco), True
    if test_id == Cases.TUTORIAL_1: return test_tutorial_1(dev, poco), True
    if test_id == Cases.TUTORIAL_2: return test_tutorial_2(dev, poco), True
    if test_id == Cases.TUTORIAL_3: return test_tutorial_3(dev, poco), True
    # if test_id == Cases.TUTORIAL_4: return test_tutorial_4(dev, poco), True
    if test_id == Cases.TUTORIAL_5: return test_tutorial_5(dev, poco), True
    if test_id == Cases.TUTORIAL_6: return test_tutorial_6(dev, poco), True
    if test_id == Cases.TUTORIAL_7: return test_tutorial_7(dev, poco), True
    if test_id == Cases.TUTORIAL_8: return test_tutorial_8(dev, poco), True
    if test_id == Cases.TUTORIAL_9: return test_tutorial_9(dev, poco), True
    if test_id == Cases.TUTORIAL_10: return test_tutorial_10(dev, poco), True
    
    return False, False


# =============================================================================
def touch_node(dev, poco, str_node):
    with poco.freeze() as frozen_poco:
        node = get_node_quick(frozen_poco, str_node, False)
        touch_center(dev, node)


# ================================================================
def get_log_path(filepath, logpath):
    path, name = script_dir_name(filepath)
    print(path + ' ' + name)
    logpath = os.path.join(path, logpath)
    return logpath 


# ================================================================
def push_my_saves(saves_name, package):
    save_from = './saves/' + saves_name

    '''
    save_from = './saves/save_common'
    if test_id == Cases.TUTORIAL_1: save_from = './saves/save_tutorial_1'
    if test_id == Cases.TUTORIAL_2: save_from = './saves/save_tutorial_2'
    if test_id == Cases.TUTORIAL_3: save_from = './saves/save_tutorial_3'
    # if test_id == Cases.TUTORIAL_4: save_from = './saves/save_tutorial_4'
    if test_id == Cases.TUTORIAL_5: save_from = './saves/save_tutorial_5'
    if test_id == Cases.TUTORIAL_6: save_from = './saves/save_tutorial_6'
    if test_id == Cases.TUTORIAL_7: save_from = './saves/save_tutorial_7'
    if test_id == Cases.TUTORIAL_8: save_from = './saves/save_tutorial_8'
    if test_id == Cases.TUTORIAL_9: save_from = './saves/save_tutorial_9'
    if test_id == Cases.TUTORIAL_10: save_from = './saves/save_tutorial_10'
    '''

    clear_app(package)
    
    full_path_to = 'sdcard/Android/data/' + package
    shell('mkdir ' + full_path_to)
    full_path_to = 'sdcard/Android/data/' + package + "/files"
    shell('mkdir ' + full_path_to)
    shell('mkdir ' + full_path_to + '/2020-04-09-17-10-42')
    shell('mkdir ' + full_path_to + '/Settings')
    a = Android()
    a.adb.push(save_from + '/events.tsf', full_path_to + '/2020-04-09-17-10-42/')
    a.adb.push(save_from + '/profile.tsf', full_path_to + '/2020-04-09-17-10-42/')
    a.adb.push('./saves/Settings/settings.tsf', full_path_to + '/Settings/')
    a.adb.push('./saves/nw_save10.save', full_path_to + '/')


# ================================================================
def read_data_from_config(file_name):
    # значение по умолчанию
    package = 'com.herocraft.game.tempest.lite'

    print('load config: ' + file_name)
    data = []
    with open(file_name, 'rt', encoding='utf-8') as f:
        for line in f:
            parts = line.split(' ')
    
            if parts[0].startswith('package:'):
                cmds = line.split(':')
                package = cmds[1].strip('\n').strip()
                print('package: \'' + package + '\'')
            
            if parts[0].startswith('stop'):
                print_config_data(data)
                return package, data;
            
            if parts[0] == 'run':
                cmds = line.split('#')
                data.append(cmds[0].lower())
                
    print_config_data(data)
    return package, data


# ================================================================
def print_config_data(data):
    print('------------------')
    print('loaded config: ')
    for line in data:
        print(line)
    print('------------------')


# ================================================================
def parse_line_from_config(line):
    test_id = ''
    f_push_saves = ''
    f_wake = False
    f_stop_before = False
    f_clear_app = False
    f_start_app = False
    f_stop_after = False
    
    parts = line.split(' ')
    for c in parts:
        c = c.strip('\n').strip()
        if c != 'run':
            if c.startswith('-push_saves:'):
                f_stop_before = True; 
                f_clear_app = True
                f_start_app = True 
                f_push_saves = c[12:]
                print('saves: ' + f_push_saves)

            test_id = parts[1]
            
            if c == '-wake': 
                f_wake = True
                
            if c == '-stop_app_before': 
                f_stop_before = True 
                f_start_app = True
                
            if c == '-clear_app': 
                f_stop_before = True 
                f_clear_app = True
                f_start_app = True
                
            if c == '-start_app': 
                # f_stop_before = True 
                f_start_app = True
                
            if c == '-stop_after': 
                f_stop_after = True
                
    return test_id, \
        f_wake, f_stop_before, \
        f_clear_app, f_push_saves, \
        f_start_app, f_stop_after

