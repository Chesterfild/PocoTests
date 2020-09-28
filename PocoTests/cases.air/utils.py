'''
Created on 10 мар. 2020 г.

@author: _OttoVonChesterfild_
'''
# import sys
import traceback

from airtest.core.api import time, touch, pinch, swipe
from airtest.core.helper import log


# =============================================================================
def out(s, str_trace=''):
    print(s, str_trace)
    log(s, str_trace)

    
# =============================================================================
def get_trace():
    # traceback.print_stack()
    es = traceback.extract_stack()
    fl = traceback.format_list(es)
    s = ''
    for l in fl:
        s = s + l;
    return s


# =============================================================================
def print_attr(node, write_to_log=False):
    if not node.exists():
        e = get_trace()
        print('node not exists...\n' + e)
        log('node not exists...', e)
        return
    
    var_str = 'name: ' + node.attr('name') + '; '
    var_str = var_str + 'type: ' + node.attr('type') + '; '
    
    var_str = var_str + 'visible: '
    if node.attr('visible'): var_str = var_str + 'True; '
    else: var_str = var_str + 'False; '
    
    var_str = var_str + 'clickable: ' 
    if node.attr('clickable'): var_str = var_str + 'True; '
    else: var_str = var_str + 'False; '
    
    # _lst = node.attr('components')
    # if len(_lst) >= 0:
    #    var_str = var_str + 'components: ['
    #    first = True
    #    for component in _lst:
    #        if not first: var_str = var_str + ', '  
    #        first = False
    #        var_str = var_str + component
    #    var_str = var_str + ']; '
        
    print(var_str)
    if (write_to_log):
        log(var_str)

    
# =============================================================================
def is_tree_is_visible(frozen_poco, tree):
    '''
    Быстрая проверка дерева нод на видимость
    Args:
        frozen_poco: frozen_poco
        tree: список строк пути к нодам вида: ['Canvas/MainMenu/Button_Start', ".." ...]
            ноды из списка должны все существовать...
    Returns:
        вернёт True если все элементы присутствуют в дереве и все видимые
    '''
    for str_path in tree:
        first = True
        node = frozen_poco('')
        path = str_path.split('/')
        for n in path:
            if first:
                node = frozen_poco(n)
                first = False
            else:
                node = node.child(n)

            if node.exists():
                if not node.attr('visible'):
                    # print("__"+str_path+"__ "+n+" is not visible")
                    return False
            else:
                # print("__"+str_path+"__ "+n+" is not exists")
                return False
    return True

        
# =============================================================================
def get_node_quick(frozen_poco, str_path, log_out=True):
    '''
    Быстрое получение ноды
    Args:
        frozen_poco: frozen_poco
        str_path: строка пути к ноде вида: 'Canvas/MainMenu/Button_Start'
        log_out: флаг логирования при ошибке        
    Returns:
        вернёт ноду, которую можно проверить методом exists()
    '''      
    first = True
    node = frozen_poco('')
    path = str_path.split('/')
    for n in path:
        if first:
            node = frozen_poco(n)
            first = False
        else:
            node = node.child(n)
        if not node.exists():
            if log_out:
                print('error get node: \'' + n + '\' from: \'' + str_path + '\'', get_trace())
            return node
    return node


# =============================================================================
def get_node_child(root_node, str_path, log_out=True):
    '''
    Быстрое получение ноды
    Args:
        root_node: root_node
        str_path: строка пути к ноде вида: 'Canvas/MainMenu/Button_Start'
        log_out: флаг логирования при ошибке        
    Returns:
        вернёт ноду, которую можно проверить методом exists()
    '''      
    node = root_node
    path = str_path.split('/')
    for n in path:
        node = node.child(n)
        if not node.exists():
            if log_out:
                print('error get node: \'' + n + '\' from: \'' + str_path + '\'', get_trace())
            return node
    return node


# =============================================================================
def touch_center(dev, node, logout=False, times=1):
    np = pos_center(dev, node)
    if logout:
        out('touch: ' + str(np[0]) + ', ' + str(np[1]))
    touch(np, times)


# =============================================================================
def pos_center(dev, node, is_abs_value=True):
    '''
    получение координат центра ноды 
    Args:
        dev: dev
        node: node
        is_abs_value: True - значения в пикселях, False - [0..1, 0..1] от экрана
    Returns:
        вернёт [x,y]
    '''
    # resolution = device().get_current_resolution()
    # resolution = device().get_render_resolution()
    resolution = dev.get_render_resolution()
    if not is_abs_value:
        resolution = [0, 0, 1, 1]

    pos = node.attr('pos')
    size = node.attr('size')
    anchorPoint = node.attr('anchorPoint')
    offset = [size[0] * (0.5 - anchorPoint[0]), size[1] * (0.5 - anchorPoint[1])]
    np = [resolution[2] * (pos[0] + offset[0]), resolution[3] * (pos[1] + offset[1])]

    return np


# =============================================================================
def pos_scr2abs(dev, pos):
    resolution = dev.get_render_resolution()
    np = [resolution[2] * pos[0], resolution[3] * pos[1]]
    return np
    

# =============================================================================
def pos_abs2scr(dev, pos):
    resolution = dev.get_render_resolution()
    np = [pos[0] / resolution[2], pos[1] / resolution[3]]
    return np

# =============================================================================
'''
def pinch_center(dev, node, in_or_out='in', logout=False):
    # resolution = device().get_current_resolution()
    # resolution = device().get_render_resolution()

    pos = node.attr('pos')
    size = node.attr('size')
    anchorPoint = node.attr('anchorPoint')
    offset = [size[0] * (0.5 - anchorPoint[0]), size[1] * (0.5 - anchorPoint[1])]

    # out('try get device')
    # dev = device()
    # out('get device')
    #resolution = dev.get_render_resolution()
    # out('get resolution')
    
    np = [pos[0] + offset[0], pos[1] + offset[1]]

    if logout:
        out('pinch('+in_or_out+'): ' + str(np[0]) + ', ' + str(np[1]))
    pinch(in_or_out, np)
'''


# =============================================================================
def wait_for_node_visible(poco, str_node, timeout=1, clickable=False, logout=False):
    if logout:
        out('wait: ' + str_node)

    f_exit = False
    while not f_exit:
        # poco = UnityPoco()
        with poco.freeze() as frozen_poco:
            node = get_node_quick(frozen_poco, str_node, False)
            if node.exists():
                if node.attr('visible'):
                    if clickable:
                        if node.attr('clickable'):
                            f_exit = True
                    else :
                        f_exit = True
        
        if not f_exit:
            time.sleep(1)
            timeout = timeout - 1
            if (timeout < 1):
                if logout:
                    log('Node \'' + str_node + '\' is not visible, exit for timeout', get_trace())
                return node
        else:
            if logout:
                out('wait return: ' + str_node)
            return node


# =============================================================================
def wait_and_click_button(dev, poco, button):
    node = wait_for_node_visible(poco, button, 5)
    if not node.exists():
        out('Button not showed', button)
        return False
    touch_center(dev, node)
    time.sleep(1)
    return True
    
    
