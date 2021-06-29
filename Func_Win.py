# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import time, os, sys
from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.keys import Keys

#from Func_Common import NowTime
#from Func_Common import path_create

#https://github.com/microsoft/WinAppDriver/releases

__platform__ = 'Win'
__script_path__ = f'{os.path.dirname(os.path.abspath(__file__))}'
__time__ = time.strftime(f'%Y%m%d_%H%M%S',time.localtime(time.time()))

class Win:
    def __init__(self, WindowsHandle=None, DriverInfo={'ip':'127.0.0.1','port':'4723'}, Delay={'retry':5, 'after':1}, ClassOption={}):
        '''
            WindowsHandle = None or windows handle hex

            DriverInfo =
            {
                'ip': WinAppDriver ip,
                'port' : WinAppDriver port
            }

            Delay =
            {
                'retry' : if fail retry count,
                'after' : action delay second
            }

            ClassOption =
            {
                'screenshot_path' = save folder path,
                'log_file_path' = log file full path,
                'class_name' = class name > log > "{time} {class_name} {log_text}"
                'element_type' = accessibility id, xpath etc...
                'class_log' = True, class in func log write
            }
        '''

        if 'ip' in DriverInfo.keys():
            self.__driver_ip__ = DriverInfo['ip']
        else:
            self.__driver_ip__ = '127.0.0.1'

        if 'port' in DriverInfo.keys():
            self.__driver_port__ = DriverInfo['port']
        else:
            self.__driver_port__ = '4723'
    
        self.__driver_host__ = f'http://{self.__driver_ip__}:{self.__driver_port__}'

        if 'screenshot_path' in ClassOption.keys():
            self.__screenshot_path__ = ClassOption['screenshot_path']
        else:
            self.__screenshot_path__ = f'{__script_path__}/screenshot/{__time__}'

        if 'log_file_path' in ClassOption.keys():
            self.__log_file_path__ = ClassOption['log_file_path']
        else:
            self.__log_file_path__ = f'{__script_path__}/log/{__time__}.txt'

        if 'class_name' in ClassOption.keys():
            self.__class_name__ = ClassOption['class_name']
        else:
            self.__class_name__ = __platform__

        if 'element_type' in ClassOption.keys():
            self.__element_type__ = ClassOption['element_type']
        else:
            self.__element_type__ = 'accessibility id'

        if 'class_log' in ClassOption.keys():
            self.__class_log__ = ClassOption['class_log']
        else:
            self.__class_log__ = True

        if 'retry' in Delay:
            self.__retry__ = Delay['retry']
        else:
            self.__retry__ = 5

        if 'after' in Delay:
            self.__after__ = Delay['after']
        else:
            self.__after__ = 1

        self.__desktop_handle__ = None


        self.__error__ = ''
        self.class_data_01 = ''
        self.class_data_02 = ''
        self.class_data_03 = ''
        self.class_data_04 = ''

        self.path_create(os.path.dirname(self.__log_file_path__))
        self.path_create(os.path.dirname(self.__screenshot_path__))

        self.driver = None
        if WindowsHandle:
            self.Change_handle(WindowsHandle=WindowsHandle)
        else:
            self.__reset_handle__()
        
        #self.refresh_desktop_handle()

        self.ElementHandle = []
        self.ElementIndex = None
        self.ElementValue = None
        self.ElementValueType = None
        self.ElementValueList = []
        self.ElementAttribute = []

        
    def __reset_handle__(self):
        desired_caps = {}
        desired_caps["app"] = "Root"
        #desired_caps["platformName"] = "Windows"
        #desired_caps["deviceName"] = "WindowsPC"
        self.driver = webdriver.Remote(command_executor=self.__driver_host__,desired_capabilities=desired_caps)

    def __call__(self,Elements=None,WindowsHandle=None,Index=None,Value=None,ValueType=None):
        #input, output

        if WindowsHandle:
            self.Change_handle(WindowsHandle=WindowsHandle)

        self.ElementHandle = Elements
        self.ElementIndex = None
        self.ElementValue = None
        self.ElementValueType = None

        #only output
        self.ElementDisplay = False
        self.ElementValueList = []
        self.ElementAttribute = []

        if Index == None:
            if 'dict' in str(type(Elements)):
                try:
                    self.ElementIndex = Elements['Index']
                except:
                    self.ElementIndex = None
        else:
            self.__ElementIndex__(Elements,Index)
        
        if Value == None:
            if 'dict' in str(type(Elements)):
                try:
                    self.ElementValue = Elements['Value']
                except:
                    self.ElementValue = None
        else:
            self.__ElementValue__(Elements,Value)

        if ValueType == None:
            if 'dict' in str(type(Elements)):
                try:
                    self.ElementValueType = Elements['ValueType']
                except:
                    self.ElementValueType = None
        else:
            self.__ElementValueType__(Elements,ValueType)
        
        return self          

    def __ElementHandle__(self, Elements):
        if Elements != None:
            self.ElementHandle = Elements

    def __ElementIndex__(self, Elements, Index):
        '''
            Index : 찾은 Elements의 값중 몇번째 항목인지 선택 값이 없다면 0
            우선순위 : Index > ElementIndex > Elements > 0
            type : Number
        '''
        if Index == None:
            if self.ElementIndex == None:
                if 'dict' in str(type(Elements)) and 'Index' in Elements:
                    self.ElementIndex = Elements['Index']
                else:
                    self.ElementIndex = 0
        else:
            self.ElementIndex = Index

    def __ElementValue__(self, Elements, Value):
        '''
            Value : 찾은 Elements에서 비교할 값
            type :  str
            우선순위 : Value > ElementValue > Elements > None
        '''
        if Value == None:
            if self.ElementValue == None:
                if 'dict' in str(type(Elements)) and 'Value' in Elements:
                    self.ElementValue = Elements['Value']
                else:
                    self.ElementValue = None
        else:
            self.ElementValue = Value

    def __ElementValueType__(self, Elements, ValueType):
        '''
            ValueType : Value값의 종류
            type :  str
            우선순위 : Value > ElementValueType > Elements > 'textContent'
        '''

        if ValueType == None:
            if self.ElementValueType == None:
                if 'dict' in str(type(Elements)) and 'ValueType' in Elements:
                    self.ElementValueType = Elements['ValueType']
                else:
                    self.ElementValueType = 'textContent'
        else:
            self.ElementValueType = ValueType

    def now_time(self, return_type='text'):
        if return_type.lower() == 'file':
            return time.strftime(f'%Y%m%d_%H%M%S',time.localtime(time.time()))
        elif return_type.lower() == 'text':
            return time.strftime(f'%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    def find_key_in_dict_list(self, dict_list:list, key_name, key_value):
        for taget_dict in dict_list:
            key_list = taget_dict.keys()
            if key_name in key_list:
                find_key_value = taget_dict[key_name]
                if key_value == find_key_value:
                    return taget_dict
        return None

    def path_create(self, path):
        if not(os.path.isdir(path)):
            try:
                os.makedirs(os.path.join(path))
            except:
                print(sys.exc_info())

    def log(self, log_text, write_log=True, print_log:bool=True):
        if str(log_text)[0:5].lower() == 'error':
            self.__error__ = f'[{self.__class_name__}]\t{str(log_text)}'
            log_write = f'{self.now_time()}\t[{self.__class_name__}]\t{str(log_text)}\n'
        else:
            log_write = f'{self.now_time()}\t[{self.__class_name__}]\t{str(log_text)}\n'
        
        if print_log == True:
            print(log_write, end='')

        if write_log == True:
            log_file = open(self.__log_file_path__, "a", encoding="utf-16")
            log_file.write(f'{log_write}')
            log_file.close()

        if str(log_text)[0:5].lower() == 'error':
            raise Exception(f'{self.__error__}')

    def Run_app(self, file_path):
        desired_caps = {}
        desired_caps['platformName'] = 'Windows'
        desired_caps['deviceName'] = 'WindowsPC'
        desired_caps['app'] = file_path
        try:
            self.driver = webdriver.Remote(command_executor=self.__driver_host__, desired_capabilities=desired_caps)
        except:
            self.log(f'error : Run_app > "{file_path}"\n{sys.exc_info()}', write_log=self.__class_log__)

    def Change_handle(self,Elements=None, WindowsHandle=None):
        self.__reset_handle__()
        if not WindowsHandle:
            if Elements:
                if 'Type' in Elements:
                    ElementType = Elements['Type']
                else:
                    ElementType = 'xpath'
            
                if 'Taget' in Elements:
                    ElementTaget = Elements['Taget']
                else:
                    #self.screenshot(f'FindElements_Error')
                    self.log(f'Error : Change_handle > Element Taget > {Elements}', write_log=self.__class_log__)
                get_handle = self.driver.find_element(ElementType,ElementTaget).get_attribute('NativeWindowHandle')
                handle_hex = hex(int(get_handle))
        else:
            handle_hex = WindowsHandle
        #self.log(handle_hex)
        desired_caps = {}
        desired_caps["appTopLevelWindow"] = handle_hex
        self.driver = webdriver.Remote(command_executor=self.__driver_host__,desired_capabilities=desired_caps)
        return self

    def refresh_desktop_handle(self):
        desktop_handle = self.driver.find_elements_by_xpath('/*')
        if desktop_handle:
            self.__desktop_handle__ = desktop_handle
        else:
            self.log('Error : refresh_desktop_handle > not find desktop handle', write_log=self.__class_log__)

    def FindElements(self, Elements):
        """
            조건에 맞는 모든 Elements 핸들 집합 생성 후
            ElementHandle에 갱신

            Highlight : 찾은 Elements 강조 표시
            type :  bool
            https://github.com/microsoft/WinAppDriver/blob/master/Docs/AuthoringTestScripts.md
            Client API	Locator Strategy	Matched Attribute in inspect.exe	Example
            FindElementByAccessibilityId	accessibility id	AutomationId	AppNameTitle
            FindElementByClassName	class name	ClassName	TextBlock
            FindElementById	id	RuntimeId (decimal)	42.333896.3.1
            FindElementByName	name	Name	Calculator
            FindElementByTagName	tag name	LocalizedControlType (upper camel case)	Text
            FindElementByXPath	xpath	Any	//Button[0]
        """
        self.__ElementHandle__(Elements)
        TagetElement = self.ElementHandle
            
        if 'list' in str(type(TagetElement)):
            #이미 완성된 WebElement 집합
            self.ElementHandle = Elements
            return self

        elif 'dict' in str(type(TagetElement)):
            if 'Type' in TagetElement:
                ElementType = TagetElement['Type']
            else:
                ElementType = self.__element_type__
            
            if 'Taget' in TagetElement:
                ElementTaget = TagetElement['Taget']
            else:
                #self.screenshot(f'FindElements_Error')
                self.log(f'Error : FindElements > Element Taget > {TagetElement}', write_log=self.__class_log__)

            try:
                Result = self.driver.find_elements(ElementType, ElementTaget)
            except:
                self.log(f'Error : FindElements > Element Type : {TagetElement} [{str(type(TagetElement))}]\n{sys.exc_info()}', write_log=self.__class_log__)

            if len(Result) == 0:
                self.log(f'FindElements > Not Find >{TagetElement}', write_log=self.__class_log__)
                Result = []
            self.ElementHandle = Result
            return self
        else:
            #self.screenshot(f'FindElements_Error')
            self.log(f'Error : FindElements > Element Type : {TagetElement} [{str(type(TagetElement))}]', write_log=self.__class_log__)
    

    def WaitElement(self, Elements=None, Index=None, none_element:bool=False, none_error:bool=False, retry_count:int=-1):
        """
            Element가 나타날 때까지 대기 또는 사라질 때까지 대기
            다른 기본 함수에서 동작하기전 미리 선언하는 함수

            none_element : 나타날때 까지 True, 사라질때 까지 False
            type : bool

            none_error : Elements를 찾지 못한 경우에도 Error를 호출하지 않음
            type : bool

            Silent : log를 남기지 않음
            type : bool

            Highlight : 찾은 Elements 강조 표시
            type : bool
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle
        self.log(f'WaitElement [none_element:{none_element}] > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
        
        if retry_count > 0:
            retry = retry_count
        else:
            retry = self.__retry__
            
        for _ in range(retry):
            time.sleep(self.__after__)
            self.FindElements(TagetElement)
            if len(self.ElementHandle) > ElementIndex:
                ElementHandle = [self.ElementHandle[ElementIndex]]
            else:
                ElementHandle = []

            if none_element == False:
                if len(ElementHandle) == 1:
                    self.log(f' > Show', write_log=self.__class_log__)
                    return self
            else:
                if len(ElementHandle) == 0:
                    self.log(f' > Hide', write_log=self.__class_log__)
                    return self

        if none_error == False:
            #self.screenshot(f'WaitElement_Error')
            self.log(f'Error : WaitElement [none_element:{none_element}] > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
        else:
            #self.screenshot(f'WaitElement_Pass')
            self.log(f'WaitElement [none_element:{none_element}] > {TagetElement}[{ElementIndex}] > Pass', write_log=self.__class_log__)
            return self

    def Click(self, Elements=None, Index=None, control_click:bool=True, retry_count:int=-1):
        """
            찾은 Elements에서 Index 번째의 Element에 마우스 오버 및 클릭
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle

        self.WaitElement(TagetElement,Index=ElementIndex, retry_count=retry_count)
        #self.screenshot(f'Click')
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            for _ in range(3):
                try:
                    self.ElementDisplay = ElementHandle.is_displayed()
                except:
                    pass
            try:
                ElementHandle.location_once_scrolled_into_view
            except:
                pass
            try:
                if control_click == True:
                    ElementHandle.send_keys(Keys.SPACE)
                else:
                    ElementHandle.click()
                    
                self.log(f'Click > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
                return self
            except:
                self.log(f'Click Error > {TagetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        #self.screenshot(f'Click_Error')
        self.log(f'Error : Click > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)

    def Send(self, Elements=None, Value=None, Index=None, clear:bool=True, enter:bool=False, retry_count:int=-1):
        """
            찾은 Elements의 Index 번째의 Element에 Value값을 입력
        
            clear : Value값 입력 전 전부 지우기 True
            type : bool

            enter : Value값 입력 후 enter 입력 False
            type : bool
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementValue__(Elements,Value)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        ElementValue = self.ElementValue
        TagetElement = self.ElementHandle

        self.WaitElement(TagetElement,Index=Index, retry_count=retry_count)
        #self.screenshot(f'Send')
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            if clear == True:
                try:
                    ElementHandle.clear()
                    self.log(f'clear > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
                except:
                    self.log(f'clear Error > {TagetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
                time.sleep(self.__after__)
            try:
                if ElementValue != '':
                    ElementHandle.send_keys(ElementValue)
                    self.log(f'Send > {TagetElement}[{ElementIndex}] > "{ElementValue}"', write_log=self.__class_log__)
                if enter == True:
                    time.sleep(self.__after__)
                    ElementHandle.send_keys('\ue007')
                #self.screenshot(f'Send')
                return self
            except:
                self.log(f'Send Error > {TagetElement}[{ElementIndex}] > "{ElementValue}"\n{sys.exc_info()}', write_log=self.__class_log__)
        #self.screenshot(f'Send_Error')
        self.log(f'Error : Send > {TagetElement}[{ElementIndex}] > "{ElementValue}"', write_log=self.__class_log__)

    def FindValues(self, Elements=None, Value=None, ValueType=None, retry_count:int=-1):
        """
            찾은 Element의 구성요소 값을 찾아서 ElementValueList에 갱신
            만약 ElementValueList에 Value값이 존재 한다면 ElementIndex에 갱신
            만약 ElementValue가 None 이라면 ElementValueList[0]을 ElementValue에 갱신 > GetValue 펑션 기능
        """     
        self.__ElementValueType__(Elements,ValueType)
        self.__ElementValue__(Elements,Value)
        self.__ElementHandle__(Elements)
        ElementValue = self.ElementValue
        ElementValueType = self.ElementValueType
        TagetElement = self.ElementHandle
            
        self.WaitElement(TagetElement,none_error=True, retry_count=retry_count)
        ElementValueList = []
        ElementHandle = self.ElementHandle
        for Index in range(len(ElementHandle)):
            try:
                GetValue = ElementHandle[Index].get_attribute(ElementValueType)
                if GetValue != None:
                    if ElementValueType != 'textContent' or ElementValueType != 'text':
                        if GetValue == 'true':
                            GetValue = True
                        elif GetValue == 'false':
                            GetValue = False
                else:
                    if ElementValueType == 'textContent' or ElementValueType == 'text':
                        GetValue = ElementHandle[Index].text

                ElementValueList.append(GetValue)
            except:
                self.log(f'FindValues Error > {TagetElement}[{Index}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'FindValues > {TagetElement} > {ElementValueList}', write_log=self.__class_log__)
        self.ElementValueList = ElementValueList
        if ElementValue in ElementValueList:
            Index = ElementValueList.index(ElementValue)
            self.log(f' > {Index}', write_log=self.__class_log__)
            self.ElementIndex = Index
        else:
            self.ElementIndex = None
        
        if ElementValue == None:
            if ElementValueList:
                self.ElementValue = ElementValueList[0]
        return self

    def GetAttribute(self, Elements=None,
            attribute_list=['AcceleratorKey','AccessKey','AutomationId',
            'BoundingRectangle','ClassName','ControlType','FrameworkId',
            'HasKeyboardFocus','HelpText','IsContentElement','IsEnabled',
            'IsKeyboardFocusable','IsOffscreen','IsPassword','IsRequiredForForm',
            'ItemStatus','ItemType','LabeledBy','LocalizedControlType',
            'Name','NativeWindowHandle','Orientation','ProcessId'], retry_count:int=-1):
        """
        """
        self.__ElementHandle__(Elements)
        TagetElement = self.ElementHandle
        

        self.WaitElement(TagetElement,none_error=True, retry_count=retry_count)
        ElementAttribute = []
        ElementHandle = self.ElementHandle
        for Index in range(len(ElementHandle)):       
            get_attribute = {}
            for attribute in attribute_list:
                try:
                    get_value = ElementHandle[Index].get_attribute(attribute)
                    if get_value != None:
                        if attribute != 'textContent' or attribute != 'text':
                            if get_value == 'true':
                                get_attribute[attribute] = True
                            elif get_value == 'false':
                                get_attribute[attribute] = False
                            else:
                                get_attribute[attribute] = get_value
                        else:
                            get_attribute[attribute] = get_value
                    else:
                        if attribute == 'textContent' or attribute == 'text':
                            get_attribute[attribute] = ElementHandle[Index].text
                except:
                    self.log(f'GetAttribute Error > {TagetElement}[{Index}][{attribute}]\n{sys.exc_info()}', write_log=self.__class_log__)
            time.sleep(0.1)
            ElementAttribute.append(get_attribute)
    
        self.log(f'GetAttribute > {TagetElement} > {ElementAttribute}', write_log=self.__class_log__)
        self.ElementAttribute = ElementAttribute
        return self

    def action(self):
        return  ActionChains(self.driver)

    def touchaction(self):
        return TouchAction(self.driver)

    def Mouse_move(self, Elements=None, Index=None, point:dict={'x':0,'y':0}, wait=0.5, retry_count:int=-1):
        '''
            Elements = None > 데스크탑 화면 기준
        '''
        if Elements:
            self.__ElementIndex__(Elements,Index)
            self.__ElementHandle__(Elements)
        else:
            self.refresh_desktop_handle()
            self.__ElementIndex__(self.__desktop_handle__,Index)
            self.__ElementHandle__(self.__desktop_handle__)
        
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle

        self.WaitElement(TagetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                action = self.action()
                point_x = point['x']
                point_y = point['y']
                
                action.move_to_element_with_offset(to_element=ElementHandle, xoffset=point_x, yoffset=point_y)
                action.pause(wait*1)
                action.release()
                action.perform()
                time.sleep(self.__after__)
                self.log(f'Mouse_move > {TagetElement}[{ElementIndex}][{point}]', write_log=self.__class_log__)
                return self
            except:
                self.log(f'Mouse_move Error > {TagetElement}[{ElementIndex}][{point}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Mouse_move > {TagetElement}[{ElementIndex}][{point}]', write_log=self.__class_log__)

    def Mouse_left_click(self, Elements=None, Index=None, point:dict={'x':0,'y':0}, wait=0.5, retry_count:int=-1):
        '''
            Elements = None > 데스크탑 화면 기준
        '''
        if Elements:
            self.__ElementIndex__(Elements,Index)
            self.__ElementHandle__(Elements)
        else:
            self.refresh_desktop_handle()
            self.__ElementIndex__(self.__desktop_handle__,Index)
            self.__ElementHandle__(self.__desktop_handle__)
        
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle

        self.WaitElement(TagetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                action = self.action()
                point_x = point['x']
                point_y = point['y']
                
                action.move_to_element_with_offset(to_element=ElementHandle, xoffset=point_x, yoffset=point_y)
                action.click_and_hold()
                action.pause(wait*1)
                action.release()
                action.perform()
                
                time.sleep(self.__after__)
                self.log(f'Mouse_left_click > {TagetElement}[{ElementIndex}][{point}]', write_log=self.__class_log__)
                return self
            except:
                self.log(f'Mouse_left_click Error > {TagetElement}[{ElementIndex}][{point}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Mouse_left_click > {TagetElement}[{ElementIndex}][{point}]', write_log=self.__class_log__)


    def Mouse_right_click(self, Elements=None, Index=None, point:dict={'x':0,'y':0}, wait=0.5, retry_count:int=-1):
        '''
            Elements = None > 데스크탑 화면 기준
        '''
        if Elements:
            self.__ElementIndex__(Elements,Index)
            self.__ElementHandle__(Elements)
        else:
            self.refresh_desktop_handle()
            self.__ElementIndex__(self.__desktop_handle__,Index)
            self.__ElementHandle__(self.__desktop_handle__)
        
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle

        self.WaitElement(TagetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                action = self.action()
                point_x = point['x']
                point_y = point['y']
                
                action.move_to_element_with_offset(to_element=ElementHandle, xoffset=point_x, yoffset=point_y)
                action.context_click()
                action.pause(wait*1)
                action.release()
                action.perform()
                
                time.sleep(self.__after__)
                self.log(f'Mouse_right_click > {TagetElement}[{ElementIndex}][{point}]', write_log=self.__class_log__)
                return self
            except:
                self.log(f'Mouse_right_click Error > {TagetElement}[{ElementIndex}][{point}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Mouse_right_click > {TagetElement}[{ElementIndex}][{point}]', write_log=self.__class_log__)


    def Mouse_double_click(self, Elements=None, Index=None, point:dict={'x':0,'y':0}, wait=0.5, retry_count:int=-1):
        '''
            Elements = None > 데스크탑 화면 기준
        '''
        if Elements:
            self.__ElementIndex__(Elements,Index)
            self.__ElementHandle__(Elements)
        else:
            self.refresh_desktop_handle()
            self.__ElementIndex__(self.__desktop_handle__,Index)
            self.__ElementHandle__(self.__desktop_handle__)
        
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle

        self.WaitElement(TagetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                action = self.action()
                point_x = point['x']
                point_y = point['y']
                
                action.move_to_element_with_offset(to_element=ElementHandle, xoffset=point_x, yoffset=point_y)
                action.double_click()
                action.pause(wait*1)
                action.release()
                action.perform()
                
                time.sleep(self.__after__)
                self.log(f'Mouse_double_click > {TagetElement}[{ElementIndex}][{point}]', write_log=self.__class_log__)
                return self
            except:
                self.log(f'Mouse_double_click Error > {TagetElement}[{ElementIndex}][{point}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Mouse_double_click > {TagetElement}[{ElementIndex}][{point}]', write_log=self.__class_log__)

    def Mouse_drag(self, SourceElements=None, SourceIndex=None, TagetElements=None, Taget_index=None, source_offset={'x':None,'y':None}, taget_offset={'x':None,'y':None}, wait=1, retry_count:int=-1):
        """
            ElementHandle의 ElementIndex번째 Element를
            Taget_Element의 Taget_index번째 Element로 드래그엔 드랍
            ElementHandle은 TagetElement로 갱신됨
        """

        if 'x' in source_offset.keys():
            source_offset_x = source_offset['x']
        else:
            source_offset_x = None

        if 'y' in source_offset.keys():
            source_offset_y = source_offset['y']
        else:
            source_offset_y = None

        if 'x' in taget_offset.keys():
            taget_offset_x = taget_offset['x']
        else:
            taget_offset_x = None

        if 'y' in source_offset.keys():
            taget_offset_y = taget_offset['y']
        else:
            taget_offset_y = None

        if SourceElements:
            self.__ElementIndex__(SourceElements,SourceIndex)
            self.__ElementHandle__(SourceElements)
        else:
            self.refresh_desktop_handle()
            self.__ElementIndex__(self.__desktop_handle__,SourceIndex)
            self.__ElementHandle__(self.__desktop_handle__)

        SourceElement = self.ElementHandle
        SourceIndex = self.ElementIndex
        self.ElementIndex = None

        if TagetElements:
            self.__ElementIndex__(TagetElements,Taget_index)
            self.__ElementHandle__(TagetElements)
        else:
            self.refresh_desktop_handle()
            self.__ElementIndex__(self.__desktop_handle__,Taget_index)
            self.__ElementHandle__(self.__desktop_handle__)

        TagetElement = self.ElementHandle
        TagetIndex = self.ElementIndex

        self.WaitElement(SourceElement,Index=SourceIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            Sourece_ElementCheck = self.ElementHandle[SourceIndex]
            self.WaitElement(TagetElement,Index=TagetIndex, retry_count=retry_count)
            if len(self.ElementHandle) > 0:
                Taget_ElementCheck = self.ElementHandle[TagetIndex]
                try:
                    action = self.action()
                    Soureces = Sourece_ElementCheck
                    Taget = Taget_ElementCheck
                    action.move_to_element_with_offset(Soureces, xoffset=source_offset_x, yoffset=source_offset_y).click_and_hold().pause(wait*1).perform()
                    time.sleep(wait*1)
                    action.move_to_element_with_offset(Taget, xoffset=taget_offset_x, yoffset=taget_offset_y).pause(wait*1).release().perform()
                    self.log(f'Mouse_element_drag > {SourceElement}[{SourceIndex}][{source_offset}] > {TagetElement}[{TagetIndex}][{taget_offset}]', write_log=self.__class_log__)
                    return self
                except:
                    self.log(f'Mouse_element_drag error > {SourceElement}[{SourceIndex}][{source_offset}] > {TagetElement}[{TagetIndex}][{taget_offset}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Mouse_element_drag > {SourceElement}[{SourceIndex}][{source_offset}] > {TagetElement}[{TagetIndex}][{taget_offset}]', write_log=self.__class_log__)




'''
def FindImage(self):
    Finding = 0
    for _ in range(self.__retry__):
        imgpos = pyautogui.locateOnScreen(self.file_path, confidence=self.confidence, grayscale=True)
        if imgpos != None:
            break
        else:
            Finding += 1
            time.sleep(self.__after__)

    if imgpos == None:
        return None
    else:
        return imgpos
'''