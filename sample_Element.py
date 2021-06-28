# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
from selenium.webdriver.common.by import By
    Web Element Type

    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"
'''

url_google = 'https://google.co.kr'
url_python_doc = 'https://www.python.org/doc/'

google_main_input_search = {'Taget':'input[title="검색"]'}
google_search_list = {'Taget':'div#search > div > div > div.g h3.r a'}
google_search_list_href = {'Taget':'div#search > div > div > div.g h3.r a', 'ValueType':'href'}
google_search_list_href_value = {'Taget':'div#search > div > div > div.g h3.r a', 'ValueType':'href', 'Value':url_python_doc}
google_search_list_click = {'Taget':'div#search > div > div > div.g h3.r'}

file_path_notepad = r'C:\Windows\System32\notepad.exe'
notepad_input_text = {'Type':'accessibility id', 'Taget':'15'}

file_path_calculator = 'Microsoft.WindowsCalculator_8wekyb3d8bbwe!App'
calculator_bt_number0 = {'Taget':'num0Button'}
calculator_bt_number1 = {'Type':'accessibility id','Taget':'num1Button'}
calculator_bt_number2 = {'Type':'accessibility id','Taget':'num2Button'}
calculator_bt_number3 = {'Type':'accessibility id','Taget':'num3Button'}
calculator_bt_number4 = {'Type':'accessibility id','Taget':'num4Button'}
calculator_bt_number5 = {'Type':'accessibility id','Taget':'num5Button'}
calculator_bt_number6 = {'Type':'accessibility id','Taget':'num6Button'}
calculator_bt_number7 = {'Type':'accessibility id','Taget':'num7Button'}
calculator_bt_number8 = {'Type':'accessibility id','Taget':'num8Button'}

calculator_bt_number9_xpath = {'Type':'xpath','Taget':'//*[@AutomationId="num9Button"]'}

calculator_bt_divide = {'Type':'accessibility id','Taget':'divideButton'}
calculator_bt_multiply = {'Type':'accessibility id','Taget':'multiplyButton'}
calculator_bt_minus = {'Type':'accessibility id','Taget':'minusButton'}
calculator_bt_plus = {'Type':'accessibility id','Taget':'plusButton'}
calculator_bt_equal = {'Type':'accessibility id','Taget':'equalButton'}
calculator_label_result = {'Type':'accessibility id','Taget':'CalculatorResults'}
calculator_bt_clear = {'Type':'accessibility id','Taget':'clearButton'}



