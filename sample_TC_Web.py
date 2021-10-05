# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os, time
import unittest # https://docs.python.org/ko/3/library/unittest.html

from Func_Web import Web
import sample_Element as element
import chromedriver_autoinstaller
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

chromedriver_path = chromedriver_autoinstaller.install()

__platform__ = 'Web'
__script_path__ = f'{os.path.dirname(os.path.abspath(__file__))}'
__time__ = time.strftime(f'%Y%m%d_%H%M%S',time.localtime(time.time()))

chrome_options = webdriver.ChromeOptions()
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities['goog:loggingPrefs'] = {"browser": "ALL", 'performance': 'ALL'}
#{"driver": "ALL", "browser": "ALL", 'performance': 'ALL'} > browser : 콘솔 로그 / performance : Network

driver_info = {}
driver_info['ip'] = None
driver_info['port'] = None
driver_info['executable_path'] = chromedriver_path
driver_info['location'] = None
driver_info['chrome_options'] = chrome_options
driver_info['desired_capabilities'] = desired_capabilities

class_option = {}
class_option['element_highlight'] = False
class_option['screenshot_path'] = f'{__script_path__}/screenshot/{__time__}'
class_option['log_file_path'] = f'{__script_path__}/log/{__time__}.txt'
class_option['class_name'] = __platform__
class_option['element_type'] = 'css selector'
class_option['class_log'] = True

delay = {}
delay['retry'] = 5
delay['after'] = 1

class TestCase(unittest.TestCase):
    def setUp(self):
        self.web_driver = Web(DriverInfo=driver_info,ClassOption=class_option, Delay=delay)
    
    def test_case(self):
        web_driver = self.web_driver
        web_driver.driver.get(element.url_google)
        web_driver(element.google_main_input_search).Send(Value='python',enter=True)
        
        FindValue1 = web_driver(element.google_search_list_href).FindValues()
        ElementHandle1 = FindValue1.ElementHandle
        ElementValue1 = FindValue1.ElementValue
        ElementValueList1 = FindValue1.ElementValueList
        
        FindValue2 = web_driver(element.google_search_list).FindValues()
        ElementHandle2 = FindValue2.ElementHandle
        ElementValue2 = FindValue2.ElementValue
        ElementValueList2 = FindValue2.ElementValueList
        
        FindValue3 = web_driver(element.google_search_list, ValueType='href').FindValues()
        ElementHandle3 = FindValue3.ElementHandle
        ElementValue3 = FindValue3.ElementValue
        ElementValueList3 = FindValue3.ElementValueList

        FindValue4 = web_driver(element.google_search_list_href_value).FindValues()
        ElementHandle4 = FindValue4.ElementHandle
        ElementValue4 = FindValue4.ElementValue
        ElementValueList4 = FindValue4.ElementValueList

        web_driver.log(f'ElementHandle1 : {ElementHandle1}')
        web_driver.log(f'ElementValue1 : {ElementValue1}')
        web_driver.log(f'ElementValueList1 : {ElementValueList1}')

        web_driver.log(f'ElementHandle2 : {ElementHandle2}')
        web_driver.log(f'ElementValue2 : {ElementValue2}')
        web_driver.log(f'ElementValueList2 : {ElementValueList2}')

        web_driver.log(f'ElementHandle3 : {ElementHandle3}')
        web_driver.log(f'ElementValue3 : {ElementValue3}')
        web_driver.log(f'ElementValueList3 : {ElementValueList3}')

        web_driver.log(f'ElementHandle4 : {ElementHandle4}')
        web_driver.log(f'ElementValue4 : {ElementValue4}')
        web_driver.log(f'ElementValueList4 : {ElementValueList4}')

        FindElement = web_driver(element.google_search_list_href_value).FindValues().ElementValueList
        web_driver.log(f'FindElement : {FindElement}')
        web_driver.log(f'element.url_python_doc : {element.url_python_doc}')
        if element.url_python_doc in FindElement:
            element_index = FindElement.index(element.url_python_doc)
            web_driver.log(f'element_index : {element_index}')
            web_driver(element.google_search_list_href_value).Click(Index=element_index)
        else:
            web_driver.log(f'error : not find "{element.url_python_doc}"')

        time.sleep(10)

    def tearDown(self):
        self.web_driver.driver.quit()
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)