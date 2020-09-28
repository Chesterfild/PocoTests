# -*- encoding=utf8 -*-
__author__ = "_OttoVonChesterfild_"

from airtest.core.helper import using


using("cases.air")
from cases import tests_runner

# -------------------------------------------------------------------
# -------------------------------------------------------------------
file_config = 'cases.config'

tests_runner(__file__, file_config)

# -------------------------------------------------------------------
# -------------------------------------------------------------------


'''
Место для мусора при генерации ссылок:


poco("H_logos_Canvas")poco("H_logos_Canvas")
poco("TermsOfUseWindow")poco("TermsOfUseWindow")poco("AcceptButton")
poco("SHOOT_Manual")poco("FIGHT_PANEL")


'''

