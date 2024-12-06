# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import time, os, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
import selenium.common.exceptions as selenium_exception
from ..supportmodule.common import module_class as common_module
from typing import Union
from selenium.webdriver.remote.webelement import WebElement

# chrome.exe --remote-debugging-port=9223 --user-data-dir=c:\test
# /Applications//Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9223 --user-data-dir="~/Chrome/Chrome-user01"

class module_class(common_module):
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

    def Connection(self, executable_path, debuggerAddress='', chrome_options:webdriver.ChromeOptions=None):
        if not chrome_options:
            chrome_options = webdriver.ChromeOptions()
            
        if debuggerAddress:
            chrome_options.add_experimental_option("debuggerAddress", debuggerAddress)
            #chrome_options.set_capability('loggingPrefs',{"browser": "ALL", 'performance': 'ALL'})
        
        service = Service(executable_path=executable_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)# service_args=["--verbose"] goog:loggingPrefs "--log-path=/qc1.txt"
        self.__debuggerAddress__ = self.driver.capabilities['goog:chromeOptions']['debuggerAddress'].split(':')
        self.__debugger_ip__ = self.__debuggerAddress__[0]
        self.__debugger_port__ = self.__debuggerAddress__[-1]

    def Change_url(self, url):
        self.driver.get(url)

    def Change_tab(self, handle_index=-1):
        self.driver.switch_to.window(self.driver.window_handles[handle_index])

    def Change_frame(self, frame_reference: Union[str, int, WebElement]):
        self.driver.switch_to.frame(frame_reference)

    def Execute_script(self, script, *args):
        self.driver.execute_script(script, *args)

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
                self.log(f'Error : FindElements > Element Target > {TargetElement}', log_type=-1,  write_log=self.__class_log__)

            try:
                FindResult = self.driver.find_elements(ElementType, ElementTarget)
            except:
                self.log(f'Error : FindElements > Element Type : {TargetElement} [{str(type(TargetElement))}]\n{sys.exc_info()}', log_type=-1,  write_log=self.__class_log__)
            
            if len(FindResult) == 0:
                self.log(f'FindElements > Not Find > {TargetElement}', write_log=self.__class_log__)
                FindResult = []

            self.ElementHandle = FindResult
            return self
        else:
            self.log(f'Error : FindElements > Element Type : {TargetElement} [{str(type(TargetElement))}]', log_type=-1,  write_log=self.__class_log__)

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
            self.log(f'Error : WaitElement [none_element:{none_element}] > {TargetElement}[{ElementIndex}]', log_type=-1, write_log=self.__class_log__)
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
                self.log(f'Error : FindValues > not find value', log_type=-1,  write_log=self.__class_log__)
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
        self.log(f'Error : DisplayElement > {TargetElement}[{ElementIndex}]', log_type=-1,  write_log=self.__class_log__)

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
                            self.log(f'Error > {sys.exc_info()}', log_type=-1,  write_log=self.__class_log__)

                    self.log(f'Click > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)
                else:
                    ActionChains(self.driver).move_to_element(ElementHandle).move_by_offset(offset_x, offset_y).click().perform()
                    self.log(f'Click[{offset_x},{offset_y}] > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)

                return self
            except:
                self.log(f'Click Error > {TargetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Click > {TargetElement}[{ElementIndex}]', log_type=-1,  write_log=self.__class_log__)

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
        self.log(f'Error : Select > {TargetElement}[{ElementIndex}]', log_type=-1,  write_log=self.__class_log__)

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
        self.log(f'Error : MouseOver > {TargetElement}[{ElementIndex}]', log_type=-1,  write_log=self.__class_log__)

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
        self.log(f'Error : Send > {TargetElement}[{ElementIndex}] > "{ElementValue}"', log_type=-1,  write_log=self.__class_log__)

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
        self.log(f'Error : Scrolle > {TargetElement}[{ElementIndex}]', log_type=-1,  write_log=self.__class_log__)

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
        self.log(f'Error : DragAndDrop > {SoureceElement}[{SoureceIndex}] > {TargetElement}[{TargetIndex}]', log_type=-1,  write_log=self.__class_log__)

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
    
    def alert(self):
        return Alert(self.driver)
    
    def alert_text(self):
        return self.alert().text
    
    def alert_accept(self):
        self.alert().accept()

    def alert_dismiss(self):
        self.alert().dismiss()
    