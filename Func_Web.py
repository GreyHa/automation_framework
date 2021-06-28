# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#https://fenderist.tistory.com/168
#https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions

import time, os, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as selenium_exception

#from Func_Common import NowTime
#from Func_Common import find_list_in_dict_key
#from Func_Common import path_create

__platform__ = 'Web'
__script_path__ = f'{os.path.dirname(os.path.abspath(__file__))}'
__time__ = time.strftime(f'%Y%m%d_%H%M%S',time.localtime(time.time()))

#debug mode chrome
# windows
# chrome.exe --remote-debugging-port=9223 --user-data-dir=c:\test

# mac
# /Applications//Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9223 --user-data-dir="/Users/grey/Chrome-user01"

class Web:
    def __init__(self, DriverInfo, Delay={'retry':5, 'after':1}, ClassOption={}, WinDriver=None):
        '''
            DriverInfo =
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
                }
            }

            Delay =
            {
                'retry' : if fail retry count,
                'after' : action delay second
            }

            ClassOption =
            {
                'element_highlight' = bool,
                'screenshot_path' = save folder path,
                'log_file_path' = log file full path,
                'class_name' = class name > log > "{time} {class_name} {log_text}"
                'element_type' = css selector, xpath etc...
                'class_log' = True, class in func log write
            }

            WinDriver = None or Win modul class
        '''
        self.__driver_path__ = DriverInfo['executable_path']

        if 'ip' in DriverInfo.keys():
            self.__driver_ip__ = DriverInfo['ip']
        else:
            self.__driver_ip__ = None

        if 'port' in DriverInfo.keys():
            self.__driver_port__ = DriverInfo['port']
        else:
            self.__driver_port__ = None

        if 'location' in DriverInfo.keys():
            self.__driver_location__ = DriverInfo['location']
        else:
            self.__driver_location__ = None
        
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
            self.__element_type__ = 'css selector'

        if 'element_highlight' in ClassOption.keys():
            self.__element_highlight__ = ClassOption['element_highlight']
        else:
            self.__element_highlight__ = False

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

        self.__error__ = ''        
        self.class_data_01 = ''
        self.class_data_02 = ''
        self.class_data_03 = ''
        self.class_data_04 = ''
        
        self.path_create(os.path.dirname(self.__log_file_path__))
        self.path_create(os.path.dirname(self.__screenshot_path__))
        #os.system(f'start cmd /c python -m http.server --bind {Config.WebserverIP} {Config.WebserverPort} --directory {Config.BASE_DIR}')
        #https://chromedriver.chromium.org/capabilities
        ChromeOption = webdriver.ChromeOptions()
        if self.__driver_ip__ != None:
            ChromeOption.add_experimental_option("debuggerAddress", f"{self.__driver_ip__}:{self.__driver_port__}")
        else:
            ChromeOption.add_experimental_option('prefs',{"profile.default_content_setting_values.notifications" : 2})
        
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {"driver": "ALL", "browser": "ALL", 'performance': 'ALL'}# browser : 콘솔 로그 / performance : Network
        
        self.driver = webdriver.Chrome(executable_path=self.__driver_path__, chrome_options=ChromeOption, desired_capabilities=caps)# service_args=["--verbose"] goog:loggingPrefs "--log-path=/qc1.txt"
        
        self.capabilities = self.driver.capabilities
        debuggerAddress = self.capabilities['goog:chromeOptions']['debuggerAddress'].split(':')
        
        self.driver_port = int(debuggerAddress[-1])
        if WinDriver:
            origin_title = self.driver.title
            self.driver.execute_script("document.title = 'find handle driver'")
            windows_list = WinDriver.GetAttribute({'Type':'xpath','Taget':'/*/*'},attribute_list=['Name','NativeWindowHandle']).ElementAttribute
            self.windows_attribute = self.find_key_in_dict_list(dict_list=windows_list,key_name='Name',key_value='find handle driver - Chrome')
            if self.windows_attribute:
                self.WindowsHandle = hex(int(self.windows_attribute['NativeWindowHandle']))
            else:
                self.log('error : WindowsHandle > None', write_log=self.__class_log__)
            self.driver.execute_script(f"document.title = '{origin_title}'")
        else:
             self.WindowsHandle = None
        #if Config.RunOS == 'win.exe':
        #    self.process_info = find_process_info(key_name='local_port',key_value=self.driver_port)
        #else:
        #    process_info = None

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
        
        if write_log == True:
            print(log_write, end='')

        if write_log == True:
            log_file = open(self.__log_file_path__, "a", encoding="utf-16")
            log_file.write(f'{log_write}')
            log_file.close()

        if str(log_text)[0:5].lower() == 'error':
            raise Exception(f'{self.__error__}')
            
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
                self.log(f'Error : FindElements > Element Taget > {TagetElement}', write_log=self.__class_log__)

            try:
                FindResult = self.driver.find_elements(ElementType, ElementTaget)
            except:
                self.log(f'Error : FindElements > Element Type : {TagetElement} [{str(type(TagetElement))}]\n{sys.exc_info()}', write_log=self.__class_log__)
            if len(FindResult) == 0:
                self.log(f'FindElements > Not Find > {TagetElement}', write_log=self.__class_log__)
                FindResult = []
            else:
                if len(FindResult) >= 6:
                    for Index in range(0,6):
                        if self.__element_highlight__ == True:
                            self.highlight(FindResult[Index])
                else:
                    for Index in range(0,len(FindResult)):
                        if self.__element_highlight__ == True:
                            self.highlight(FindResult[Index])
            self.ElementHandle = FindResult
            return self
        else:
            self.log(f'Error : FindElements > Element Type : {TagetElement} [{str(type(TagetElement))}]', write_log=self.__class_log__)

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
            self.log(f'Error : WaitElement [none_element:{none_element}] > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
        else:
            self.log(f'WaitElement [none_element:{none_element}] > {TagetElement}[{ElementIndex}] > Pass', write_log=self.__class_log__)
            return self

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
                if ElementValueType != 'text':
                    GetValue = ElementHandle[Index].get_attribute(ElementValueType)
                else:
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

    def DisplayElement(self, Elements=None, Index=None, retry_count:int=-1):
        '''
            찾은 Element가 실제로 보이는지 확인 ElementDisplay에 갱신
        '''
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle

        self.WaitElement(TagetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                ElementDisplay = ElementHandle.is_displayed()
                self.log(f'DisplayElement > {TagetElement}[{ElementIndex}] > {ElementDisplay}', write_log=self.__class_log__)
                self.ElementDisplay = ElementDisplay
                return self
            except:
                self.ElementDisplay = False
                self.log(f'DisplayElement Error > {TagetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : DisplayElement > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)

    def Click(self, Elements=None, Index=None, auto_scroll:bool=True, retry_count:int=-1):
        """
            찾은 Elements에서 Index 번째의 Element에 마우스 오버 및 클릭
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle

        self.WaitElement(TagetElement,Index=ElementIndex, retry_count=retry_count)
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
                ActionChains(self.driver).move_to_element(ElementHandle).perform()
                try:
                    ElementHandle.click()
                except selenium_exception.ElementClickInterceptedException:
                        ElementHandle.send_keys(Keys.ENTER)
                except:
                        self.log(f'Error > {sys.exc_info()}', write_log=self.__class_log__)

                self.log(f'Click > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
                return self
            except:
                self.log(f'Click Error > {TagetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Click > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)

    def MouseOver(self, Elements=None, Index=None, auto_scroll:bool=True, retry_count:int=-1):
        """
            찾은 Elements에서 Index 번째의 Element에 마우스 오버 이벤트
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle

        self.WaitElement(TagetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            if auto_scroll == True:
                try:
                    ElementHandle.location_once_scrolled_into_view
                except:
                    pass
            try:
                ActionChains(self.driver).move_to_element(ElementHandle).perform()
                self.log(f'MouseOver > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
                return self
            except:
                self.log(f'MouseOver Error > {TagetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : MouseOver > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)

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

        if clear == True:
            self.WaitElement(TagetElement,Index=Index, retry_count=retry_count)
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
                    self.log(f'Send > clear > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
                except:
                    self.log(f'Send > clear Error > {TagetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
                time.sleep(self.__after__)

        self.WaitElement(TagetElement,Index=Index, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                if ElementValue != '':
                    ElementHandle.send_keys(ElementValue)
                    self.log(f'Send > {TagetElement}[{ElementIndex}] > "{ElementValue}"', write_log=self.__class_log__)
                if enter == True:
                    time.sleep(self.__after__)
                    ElementHandle.send_keys('\ue007')
                return self
            except:
                self.log(f'Send Error > {TagetElement}[{ElementIndex}] > "{ElementValue}"\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Send > {TagetElement}[{ElementIndex}] > "{ElementValue}"', write_log=self.__class_log__)

    def Scrolle(self, Elements=None, Index=-1, retry_count:int=-1):
        """
            찾은 Elements에서 Index 번째의 Element까지 스크롤
            Index : 기본값은 마지막 항목 (-1)
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle

        self.WaitElement(TagetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                ElementHandle.location_once_scrolled_into_view
                self.log(f'Scrolle > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
                time.sleep(self.__after__)
                return self
            except:
                self.log(f'Scrolle Error > {TagetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
                time.sleep(self.__after__)
        self.log(f'Error : Scrolle > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)

    def DragAndDrop(self, TagetElements, TagetIndex=None, retry_count:int=-1):
        """
            ElementHandle의 ElementIndex번째 Element를
            Taget_Element의 Taget_Index번째 Element로 드래그엔 드랍
            ElementHandle은 TagetElement로 갱신됨
            
            https://stackoverflow.com/questions/8833835/python-selenium-webdriver-drag-and-drop
            drag_and_drop > Mac에서는 동작하지 않음? > 다른 방법으로 대체 
        """
        SoureceElement = self.ElementHandle
        SoureceIndex = self.ElementIndex


        self.__ElementHandle__(TagetElements)
        TagetElement = self.ElementHandle

        self.ElementIndex = None
        self.__ElementIndex__(TagetElements,TagetIndex)
        TagetIndex = self.ElementIndex

        self.WaitElement(SoureceElement,Index=SoureceIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            Sourece_ElementCheck = self.ElementHandle[SoureceIndex]
            self.WaitElement(TagetElement,Index=TagetIndex, retry_count=retry_count)
            if len(self.ElementHandle) > 0:
                Taget_ElementCheck = self.ElementHandle[TagetIndex]
                try:
                    #ActionChains(self.driver).drag_and_drop(Sourece_ElementCheck[Sourece_IndexValue],Taget_ElementCheck[Taget_IndexValue]).perform()
                    Soureces = Sourece_ElementCheck
                    Taget = Taget_ElementCheck
                    Sourece_ElementCheck.location_once_scrolled_into_view
                    time.sleep(self.__after__)
                    ActionChains(self.driver).click_and_hold(Soureces).pause(self.__after__).perform()
                    time.sleep(self.__after__)
                    Taget_ElementCheck.location_once_scrolled_into_view
                    time.sleep(self.__after__)
                    ActionChains(self.driver).move_to_element(Taget).release(Taget).perform()
                    self.log(f'DragAndDrop > {SoureceElement}[{SoureceIndex}] > {TagetElement}[{TagetIndex}]', write_log=self.__class_log__)
                    return self
                except:
                    self.log(f'DragAndDrop error > {SoureceElement}[{SoureceIndex}] > {TagetElement}[{TagetIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : DragAndDrop > {SoureceElement}[{SoureceIndex}] > {TagetElement}[{TagetIndex}]', write_log=self.__class_log__)

    def GetAttribute(self, Elements=None,
            attribute_list=['text','textContent','class','id','style','link','href','role'], retry_count:int=-1):
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
                    if attribute == 'text':
                        get_attribute[attribute] = ElementHandle[Index].text
                    else:
                        get_attribute[attribute] = get_value
                except:
                    self.log(f'GetAttribute Error > {TagetElement}[{Index}][{attribute}]\n{sys.exc_info()}', write_log=self.__class_log__)
            time.sleep(0.1)
            ElementAttribute.append(get_attribute)
    
        self.log(f'GetAttribute > {TagetElement} > {ElementAttribute}', write_log=self.__class_log__)
        self.ElementAttribute = ElementAttribute
        return self

    def highlight(self, element):
        '''
            Highlights (blinks) a Selenium Webdriver element
        '''
        driver = element._parent
        def apply_style(s):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                element, s)
        try:
            original_style = element.get_attribute('style')
            apply_style("background: yellow; border: 2px solid red;")
            time.sleep(0.2)
            apply_style(original_style)
        except:
            self.log(f'Error : highlight\n{sys.exc_info()}', write_log=self.__class_log__)
    
    def screenshot(self,file_name):
        if not(os.path.isdir(self.__screenshot_path__)):
            os.makedirs(os.path.join(self.__screenshot_path__))
        self.driver.save_screenshot(f'{self.__screenshot_path__}/{self.now_time("file")}_{file_name}.png')


    def action(self):
        return  ActionChains(self.driver)