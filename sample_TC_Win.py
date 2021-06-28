# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os, time
import unittest # https://docs.python.org/ko/3/library/unittest.html

from Func_Win import Win
import sample_Element as element

__platform__ = 'Win'
__script_path__ = f'{os.path.dirname(os.path.abspath(__file__))}'
__time__ = time.strftime(f'%Y%m%d_%H%M%S',time.localtime(time.time()))

driver_info = {}
driver_info['ip'] = '127.0.0.1'
driver_info['port'] = '4723'

class_option = {}
class_option['screenshot_path'] = f'{__script_path__}/screenshot/{__time__}'
class_option['log_file_path'] = f'{__script_path__}/log/{__time__}.txt'
class_option['recording'] = False
class_option['class_name'] = __platform__
class_option['element_type'] = 'accessibility id'
class_option['class_log'] = True

delay = {}
delay['retry'] = 5
delay['after'] = 0

class TestCase(unittest.TestCase):
    def setUp(self):
        self.win_driver = Win(DriverInfo=driver_info, ClassOption=class_option, Delay=delay)
    
    def test_case(self):
        win_driver = self.win_driver
        win_driver.Run_app(file_path='Microsoft.WindowsCalculator_8wekyb3d8bbwe!App')

        win_driver(element.calculator_bt_number9_xpath).Click(control_click=False)
        win_driver(element.calculator_bt_number8).Click()
        win_driver(element.calculator_bt_number7).Click()
        win_driver(element.calculator_bt_number6).Click()
        win_driver(element.calculator_bt_number5).Click()
        win_driver(element.calculator_bt_number4).Click(control_click=False)
        win_driver(element.calculator_bt_number3).Click()
        win_driver(element.calculator_bt_number2).Click(control_click=True)
        win_driver(element.calculator_bt_number1).Click()
        win_driver(element.calculator_bt_number0).Click()
        result_text = win_driver(element.calculator_label_result).GetAttribute().ElementAttribute
        win_driver(element.calculator_bt_clear).Click()

        result_text2 = win_driver(element.calculator_label_result,ValueType='Name').FindValues().ElementValueList
        win_driver.log(f'result_text "{result_text}"')
        win_driver.log(f'result_text[0]["Name"] "{result_text[0]["Name"]}"')
        win_driver.log(f'result_text2 "{result_text2}"')
        
        self.win_driver.driver.quit()
        
        win_driver.Run_app(file_path=element.file_path_notepad)
        win_driver(element.notepad_input_text).Send(Value='Test Text')
        notepad_text = win_driver(element.notepad_input_text).FindValues().ElementValue
        win_driver.log(notepad_text)
        
        time.sleep(10)


    def tearDown(self):
        self.win_driver.driver.quit()
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)