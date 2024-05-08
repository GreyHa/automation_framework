# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#https://fenderist.tistory.com/168
#https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions

import time, os, sys
import SupportModule
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
import selenium.common.exceptions as selenium_exception

# chrome.exe --remote-debugging-port=9223 --user-data-dir=c:\test
# /Applications//Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9223 --user-data-dir="~/Chrome/Chrome-user01"

class Web(SupportModule.module):
    def __init__(self, clientinfo):
        '''
            clientinfo =
            {
                'executable_path' : chromedriver path,
                'ip': None or ip,
                'port' : None or port,
                'location' : None or dict
                {
                    'width': window size or None,
                    'height': window size or None,
                    'x': window position or None,
                    'y':window position or None
                },
                'chrome_options' : chrome_options,
                'desired_capabilities' : desired_capabilities,
                'retry' : if fail retry count,
                'after' : action delay second,
                'element_highlight' = bool,
                'screenshot_path' = save folder path,
                'log_file_path' = log file full path,
                'class_name' = class name > log > "{time} {class_name} {log_text}"
                'element_type' = css selector, xpath etc...
                'class_log' = True, class in func log write
            }
        '''
        
        self.__platform__ = 'Web'
        self.__script_path__ = f'{os.path.dirname(os.path.abspath(__file__))}'
        self.__start_time__ = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))

        self.__client_info__:dict = clientinfo
        self.__driver_path__:str = self.__client_info__['executable_path']

        self.__driver_ip__ = self.dict_value(self.__client_info__, key='ip', not_find_data=None)
        self.__driver_port__ = self.dict_value(self.__client_info__, key='port', not_find_data=None)
        self.__driver_location__ = self.dict_value(self.__client_info__, key='location', not_find_data=None)
        self.__screenshot_path__ = self.dict_value(self.__client_info__, key='screenshot_path', not_find_data=f'{self.__script_path__}/screenshot/{self.__start_time__}')
        self.__log_file_path__ = self.dict_value(self.__client_info__, key='log_file_path', not_find_data=f'{self.__script_path__}/log/{self.__start_time__}.txt')
        
        self.__class_name__ = self.dict_value(self.__client_info__, key='class_name', not_find_data=self.__platform__)
        self.__element_type__ = self.dict_value(self.__client_info__, key='element_type', not_find_data='css selector')
        self.__class_log__ = self.dict_value(self.__client_info__, key='class_log', not_find_data=True)
        self.__print_log__ = self.dict_value(self.__client_info__, key='print_log', not_find_data=True)        
        self.__log_collection__ = self.dict_value(self.__client_info__, key='log collection', not_find_data=True)

        self.__retry__ = self.dict_value(self.__client_info__, key='retry', not_find_data=5)
        self.__after__ = self.dict_value(self.__client_info__, key='after', not_find_data=1)

        self.__error__ = ''
        self.all_log_list = []
        self.func_log_list = []

        self.path_create(self.__log_file_path__)
        self.path_create(self.__screenshot_path__)

        chrome_options:webdriver.ChromeOptions = self.dict_value(self.__client_info__, key='chrome_options', not_find_data=webdriver.ChromeOptions(), not_find_error=False)
            
        if self.__driver_ip__ != None:
            chrome_options.add_experimental_option("debuggerAddress", f"{self.__driver_ip__}:{self.__driver_port__}")
            chrome_options.set_capability('loggingPrefs',{"browser": "ALL", 'performance': 'ALL'})
        
        service = Service(executable_path=self.__driver_path__)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)# service_args=["--verbose"] goog:loggingPrefs "--log-path=/qc1.txt"
        self.__debuggerAddress__ = self.driver.capabilities['goog:chromeOptions']['debuggerAddress'].split(':')
        self.__debugger_ip__ = self.__debuggerAddress__[0]
        self.__debugger_port__ = self.__debuggerAddress__[-1]
        self.Change_location(location=self.__driver_location__)
               
        self.ElementHandle = []
        self.ElementIndex = None
        self.ElementValue = None
        self.ElementValueType = None
        self.ElementValueList = []
        self.ElementAttribute = []
        self.ElementDisplay = False


    def __call__(self,Elements,Index=None,Value=None,ValueType=None):
        #input, output
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

    def Change_location(self, location):
        if location:
            key_list = location.keys()         
            if 'width' in key_list:
                width = location["width"]
            else:
                width = 0
            
            if 'height' in key_list:
                height = location["height"]
            else:
                height = 0
    
            if 'x' in key_list:
                location_x = location["x"]
            else:
                location_x = None

            if 'y' in key_list:
                location_y = location["y"]
            else:
                location_y = None
        
            if width != 0 and height != 0:
                self.driver.set_window_size(width=width,height=height)

            if location_x != None and location_y != None:
                self.driver.set_window_position(x=location_x,y=location_y)

    def FindElements(self, Elements=None):
        """
            조건에 맞는 모든 Elements 핸들 집합 생성 후
            ElementHandle에 갱신

            Highlight : 찾은 Elements 강조 표시
            type :  bool
        """
        #<class 'selenium.webdriver.remote.webelement.WebElement'>
        #<class 'dict'>
        
        self.__ElementHandle__(Elements)
        TargetElement = self.ElementHandle
            
        if 'list' in str(type(TargetElement)):
            #이미 완성된 WebElement 집합
            self.ElementHandle = Elements
            return self

        elif 'dict' in str(type(TargetElement)):
            if 'Type' in TargetElement:
                ElementType = TargetElement['Type']
            else:
                ElementType = self.__element_type__
            
            if 'Target' in TargetElement:
                ElementTarget = TargetElement['Target']
            else:
                self.log(f'Error : FindElements > Element Target > {TargetElement}', write_log=self.__class_log__)

            try:
                FindResult = self.driver.find_elements(ElementType, ElementTarget)
            except:
                self.log(f'Error : FindElements > Element Type : {TargetElement} [{str(type(TargetElement))}]\n{sys.exc_info()}', write_log=self.__class_log__)
            
            if len(FindResult) == 0:
                self.log(f'FindElements > Not Find > {TargetElement}', write_log=self.__class_log__)
                FindResult = []

            self.ElementHandle = FindResult
            return self
        else:
            self.log(f'Error : FindElements > Element Type : {TargetElement} [{str(type(TargetElement))}]', write_log=self.__class_log__)

    def WaitElement(self, Elements=None, Index=None, none_element:bool=False, none_error:bool=False, retry_count:int=-1):
        """
            Element가 나타날 때까지 대기 또는 사라질 때까지 대기
            다른 기본 함수에서 동작하기전 미리 선언하는 함수

            none_element : 나타날때 까지 True, 사라질때 까지 False
            type : bool

            none_error : Elements를 찾지 못한 경우에도 Error를 호출하지 않음
            type : bool
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TargetElement = self.ElementHandle
        self.log(f'WaitElement [none_element:{none_element}] > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)

        if retry_count > 0:
            retry = retry_count
        else:
            retry = self.__retry__
            
        for _ in range(retry):
            time.sleep(self.__after__)
            self.FindElements(TargetElement)
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
            self.log(f'Error : WaitElement [none_element:{none_element}] > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)
        else:
            self.log(f'WaitElement [none_element:{none_element}] > {TargetElement}[{ElementIndex}] > Pass', write_log=self.__class_log__)
            return self

    def FindValues(self, Elements=None, Value=None, ValueType=None, not_find_error=False, strip_value:bool=False, retry_count:int=-1):
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
        TargetElement = self.ElementHandle
            
        self.WaitElement(TargetElement,none_error=True, retry_count=retry_count)
        ElementValueList = []
        ElementHandle = self.ElementHandle
        for Index in range(len(ElementHandle)):
            try:
                if ElementValueType != 'text':
                    GetValue = ElementHandle[Index].get_attribute(ElementValueType)
                    if not GetValue:
                        if ElementValueType == 'checked' or ElementValueType == 'selected':
                            GetValue = ElementHandle[Index].is_selected()
                        elif ElementValueType == 'displayed':
                            GetValue = ElementHandle[Index].is_displayed()
                        elif ElementValueType == 'enabled':
                            GetValue = ElementHandle[Index].is_enabled()
                else:
                    GetValue = ElementHandle[Index].text
                    
                if strip_value == True:
                    GetValue = GetValue.strip()

                ElementValueList.append(GetValue)
            except:
                self.log(f'FindValues Error > {TargetElement}[{Index}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'FindValues > {TargetElement} > {ElementValueList}', write_log=self.__class_log__)
        self.ElementValueList = ElementValueList
        if ElementValue in ElementValueList:
            Index = ElementValueList.index(ElementValue)
            self.log(f' > {Index}', write_log=self.__class_log__)
            self.ElementIndex = Index
        else:
            if not_find_error == True:
                self.log(f'ElementValueList : {ElementValueList}', write_log=self.__class_log__)
                self.log(f'ElementValue : "{ElementValue}"', write_log=self.__class_log__)
                self.log(f'Error : FindValues > not find value', write_log=self.__class_log__)
            else:
                self.ElementIndex = None
        
        if ElementValue == None:
            if ElementValueList:
                self.ElementValue = ElementValueList[0]
        return self

    def DisplayElement(self, Elements=None, Index=None, retry_count:int=-1):
        '''
            찾은 Element가 실제로 보이는지 확인 ElementDisplay에 갱신
        '''
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TargetElement = self.ElementHandle

        self.WaitElement(TargetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                ElementDisplay = ElementHandle.is_displayed()
                self.log(f'DisplayElement > {TargetElement}[{ElementIndex}] > {ElementDisplay}', write_log=self.__class_log__)
                self.ElementDisplay = ElementDisplay
                return self
            except:
                self.ElementDisplay = False
                self.log(f'DisplayElement Error > {TargetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : DisplayElement > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)

    def Click(self, Elements=None, Index=None, auto_scroll:bool=True, offset=(0,0), retry_count:int=-1):
        """
            찾은 Elements에서 Index 번째의 Element에 마우스 오버 및 클릭
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TargetElement = self.ElementHandle
        offset_x, offset_y = offset 
        
        self.WaitElement(TargetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            for _ in range(3):
                try:
                    self.ElementDisplay = ElementHandle.is_displayed()
                except:
                    pass
            if auto_scroll == True:
                try:
                    ElementHandle.location_once_scrolled_into_view
                except:
                    pass

            try:
                #https://stackoverflow.com/questions/11908249/debugging-element-is-not-clickable-at-point-error
                #일부 Elemet 클릭시 마우스 오버 동작이 필요한 경우가 있습니다.
                if offset_x == 0 and offset_y == 0:
                    ActionChains(self.driver).move_to_element(ElementHandle).perform()

                    try:
                        ElementHandle.click()
                    except selenium_exception.ElementClickInterceptedException:
                            ElementHandle.send_keys(Keys.ENTER)
                    except:
                            self.log(f'Error > {sys.exc_info()}', write_log=self.__class_log__)

                    self.log(f'Click > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)
                else:
                    ActionChains(self.driver).move_to_element(ElementHandle).move_by_offset(offset_x, offset_y).click().perform()
                    self.log(f'Click[{offset_x},{offset_y}] > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)

                return self
            except:
                self.log(f'Click Error > {TargetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Click > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)

    def Select(self, Elements=None, Value=None, Index=None, retry_count:int=-1):
        """
            찾은 Elements에서 Index 번째의 Element에 Value를 Select
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        self.__ElementValue__(Elements,Value)
        ElementIndex = self.ElementIndex
        TargetElement = self.ElementHandle
        ElementValue = self.ElementValue

        self.WaitElement(TargetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                Select(ElementHandle).select_by_value(value=ElementValue)                
                return self
            except:
                self.log(f'Select Error > {TargetElement}[{ElementIndex}][{ElementValue}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Select > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)

    def MouseOver(self, Elements=None, Index=None, auto_scroll:bool=True, retry_count:int=-1):
        """
            찾은 Elements에서 Index 번째의 Element에 마우스 오버 이벤트
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TargetElement = self.ElementHandle

        self.WaitElement(TargetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            if auto_scroll == True:
                try:
                    ElementHandle.location_once_scrolled_into_view
                except:
                    pass
            try:
                ActionChains(self.driver).move_to_element(ElementHandle).perform()
                self.log(f'MouseOver > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)
                return self
            except:
                self.log(f'MouseOver Error > {TargetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : MouseOver > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)

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
        TargetElement = self.ElementHandle

        if clear == True:
            self.WaitElement(TargetElement,Index=Index, retry_count=retry_count)
            if len(self.ElementHandle) > 0:
                ElementHandle = self.ElementHandle[ElementIndex]
                try:
                    #ElementHandle.clear()
                    #체크리스트를 수정 할 때 클리어를 사용시 에러가 나지 않으면서 지워지지도 않음 그래서 전체 선택 > 백스페이스 이벤트로 변경
                    #전체 선택이 먹지 않음.. 텍스트수 확인후 제거필요할듯?
                    #컨텐츠텍스트가 아닌 경우가 존재해서 사이즈가 없으면 클리어처리
                    text_size = len(ElementHandle.get_attribute('textContent'))
                    for _ in range(text_size):
                        ActionChains(self.driver).send_keys(u'\ue003').send_keys(u'\ue017').perform()
                    if text_size == 0:
                        ElementHandle.clear()
                    self.log(f'Send > clear > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)
                except:
                    self.log(f'Send > clear Error > {TargetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
                time.sleep(self.__after__)

        self.WaitElement(TargetElement,Index=Index, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                if ElementValue != '':
                    ElementHandle.send_keys(ElementValue)
                    self.log(f'Send > {TargetElement}[{ElementIndex}] > "{ElementValue}"', write_log=self.__class_log__)
                if enter == True:
                    time.sleep(self.__after__)
                    ElementHandle.send_keys('\ue007')
                return self
            except:
                self.log(f'Send Error > {TargetElement}[{ElementIndex}] > "{ElementValue}"\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Send > {TargetElement}[{ElementIndex}] > "{ElementValue}"', write_log=self.__class_log__)

    def Scrolle(self, Elements=None, Index=-1, retry_count:int=-1):
        """
            찾은 Elements에서 Index 번째의 Element까지 스크롤
            Index : 기본값은 마지막 항목 (-1)
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TargetElement = self.ElementHandle

        self.WaitElement(TargetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                ElementHandle.location_once_scrolled_into_view
                self.log(f'Scrolle > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)
                time.sleep(self.__after__)
                return self
            except:
                self.log(f'Scrolle Error > {TargetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
                time.sleep(self.__after__)
        self.log(f'Error : Scrolle > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)

    def DragAndDrop(self, TargetElements, TargetIndex=None, retry_count:int=-1):
        """
            ElementHandle의 ElementIndex번째 Element를
            Target_Element의 Target_Index번째 Element로 드래그엔 드랍
            ElementHandle은 TargetElement로 갱신됨
            
            https://stackoverflow.com/questions/8833835/python-selenium-webdriver-drag-and-drop
            drag_and_drop > Mac에서는 동작하지 않음? > 다른 방법으로 대체 
        """
        SoureceElement = self.ElementHandle
        SoureceIndex = self.ElementIndex


        self.__ElementHandle__(TargetElements)
        TargetElement = self.ElementHandle

        self.ElementIndex = None
        self.__ElementIndex__(TargetElements,TargetIndex)
        TargetIndex = self.ElementIndex

        self.WaitElement(SoureceElement,Index=SoureceIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            Sourece_ElementCheck = self.ElementHandle[self.ElementIndex]
            self.WaitElement(TargetElement,Index=TargetIndex, retry_count=retry_count)
            if len(self.ElementHandle) > 0:
                Target_ElementCheck = self.ElementHandle[TargetIndex]
                try:
                    #ActionChains(self.driver).drag_and_drop(Sourece_ElementCheck[Sourece_IndexValue],Target_ElementCheck[Target_IndexValue]).perform()
                    Soureces = Sourece_ElementCheck
                    Target = Target_ElementCheck
                    Sourece_ElementCheck.location_once_scrolled_into_view
                    time.sleep(self.__after__)
                    ActionChains(self.driver).click_and_hold(Soureces).pause(self.__after__).perform()
                    time.sleep(self.__after__)
                    Target_ElementCheck.location_once_scrolled_into_view
                    time.sleep(self.__after__)
                    ActionChains(self.driver).move_to_element(Target).release(Target).perform()
                    self.log(f'DragAndDrop > {SoureceElement}[{SoureceIndex}] > {TargetElement}[{TargetIndex}]', write_log=self.__class_log__)
                    return self
                except:
                    self.log(f'DragAndDrop error > {SoureceElement}[{SoureceIndex}] > {TargetElement}[{TargetIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : DragAndDrop > {SoureceElement}[{SoureceIndex}] > {TargetElement}[{TargetIndex}]', write_log=self.__class_log__)

    def GetAttribute(self, Elements=None,
            attribute_list=['text','textContent','class','id','style','link','href','role'], retry_count:int=-1):
        """
        """
        self.__ElementHandle__(Elements)
        TargetElement = self.ElementHandle
        self.WaitElement(TargetElement,none_error=True, retry_count=retry_count)
        ElementAttribute = []
        ElementHandle = self.ElementHandle
        for Index in range(len(ElementHandle)):       
            get_attribute = {}
            for attribute in attribute_list:
                try:
                    get_value = ElementHandle[Index].get_attribute(attribute)
                    if attribute == 'text':
                        get_attribute[attribute] = ElementHandle[Index].text
                    else:
                        get_attribute[attribute] = get_value
                except:
                    self.log(f'GetAttribute Error > {TargetElement}[{Index}][{attribute}]\n{sys.exc_info()}', write_log=self.__class_log__)
            time.sleep(0.1)
            ElementAttribute.append(get_attribute)
    
        self.log(f'GetAttribute > {TargetElement} > {ElementAttribute}', write_log=self.__class_log__)
        self.ElementAttribute = ElementAttribute
        return self
    
    def screenshot(self, file_name=None, screenshot_path=None):

        if screenshot_path:
            __screenshot_path__ = screenshot_path
        else:
            __screenshot_path__ = self.__screenshot_path__

        if not(os.path.isdir(__screenshot_path__)):
            os.makedirs(os.path.join(__screenshot_path__))

        if file_name:
            file_path = f'{__screenshot_path__}/{self.now_time("file")}_{file_name}.png'
        else:
            file_path = f'{__screenshot_path__}/{self.now_time("file")}.png'

        self.driver.save_screenshot(file_path)

        return file_path


    def action(self):
        return  ActionChains(self.driver)