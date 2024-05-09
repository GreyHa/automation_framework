# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#https://selenium-python.readthedocs.io/api.html#selenium.webdriver.common.touch_actions.TouchActions.scroll

import time, os, base64, sys
from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from appium.options.android import UiAutomator2Options
from .SupportModule import module

#appium --log error --port 4723 --allow-insecure=adb_shell

class AOS(module):
    def __init__(self, clientinfo):
        '''
            clientinfo = desired_capabilities
            {
                'device' : {
                    *'automationName': 'UiAutomator2'
                    *'platformName': 'Android'
                    *'udid': udid,
                    'newCommandTimeout' : timeout second
                    'platformVersion': 11.0,
                    'deviceName': 'Pixel_2_API_30'
                    'enableMultiWindows': bool
                }
                'ip': appium ip,
                'port' : appium port
                'retry' : if fail retry count,
                'after' : action delay second
                'screenshot_path' = save folder path,
                'log_file_path' = log file full path,
                'class_name' = class name > log > "{time} {class_name} {log_text}",
                'element_type' = id, xpath etc...
                'class_log' = True, class in func log write
            }
        '''
        self.__platform__ = 'AOS'
        self.__script_path__ = f'{os.path.dirname(os.path.abspath(__file__))}'
        self.__start_time__ = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))

        self.__client_info__:dict = clientinfo
        self.__device__:dict = self.__client_info__['device']

        self.__appium_ip__ = self.dict_value(self.__client_info__, key='ip', not_find_data='127.0.0.1')
        self.__appium_port__ = self.dict_value(self.__client_info__, key='port', not_find_data='4723')

        self.__screenshot_path__ = self.dict_value(self.__client_info__, key='screenshot_path', not_find_data=f'{self.__script_path__}/screenshot/{self.__start_time__}')
        self.__log_file_path__ = self.dict_value(self.__client_info__, key='log_file_path', not_find_data=f'{self.__script_path__}/log/{self.__start_time__}.txt')
        
        self.__class_name__ = self.dict_value(self.__client_info__, key='class_name', not_find_data=self.__platform__)
        self.__element_type__ = self.dict_value(self.__client_info__, key='element_type', not_find_data='id')
        self.__class_log__ = self.dict_value(self.__client_info__, key='class_log', not_find_data=True)
        self.__print_log__ = self.dict_value(self.__client_info__, key='print_log', not_find_data=True)        
        self.__log_collection__ = self.dict_value(self.__client_info__, key='log collection', not_find_data=True)

        self.__retry__ = self.dict_value(self.__client_info__, key='retry', not_find_data=5)
        self.__after__ = self.dict_value(self.__client_info__, key='after', not_find_data=1)

        RemotePath = self.dict_value(self.__client_info__, key='RemotePath', not_find_data='')
        self.__appium_host__ = f'http://{self.__appium_ip__}:{self.__appium_port__}{RemotePath}'

        self.__error__ = ''
        self.all_log_list = []   
        self.func_log_list = []
        capabilities_options = UiAutomator2Options().load_capabilities(self.__device__)
        self.driver = webdriver.Remote(command_executor=self.__appium_host__, options=capabilities_options)

        self.driver_location = self.driver.get_window_size()
        self.driver_capabilities = self.driver.capabilities
        self.device_maker = self.driver_capabilities['deviceManufacturer']
        self.device_model = self.driver_capabilities['deviceModel']
        self.android_version = self.driver_capabilities['platformVersion']

        self.ElementHandle = []
        self.ElementIndex = None
        self.ElementValue = None
        self.ElementValueType = None
        self.ElementValueList = []
        self.ElementAttribute = []

        self.path_create(os.path.dirname(self.__log_file_path__))
        self.path_create(os.path.dirname(self.__screenshot_path__))


    def __call__(self,Elements=None,Index=None,Value=None,ValueType=None):
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
                    self.ElementValueType = 'text'
        else:
            self.ElementValueType = ValueType


    def FindElements(self, Elements):
        """

            조건에 맞는 모든 Elements 핸들 집합 생성 후
            ElementHandle에 갱신
            
            Elements = {
                'Type' : 'id',
                'Target' : 'element'
            }

        """
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
                Result = self.driver.find_elements(ElementType, ElementTarget)
            except:
                self.log(f'Error : FindElements > Element Type : {ElementType} {TargetElement} [{str(type(TargetElement))}]\n{sys.exc_info()}', write_log=self.__class_log__)

            if len(Result) == 0:
                self.log(f'FindElements > Not Find >{TargetElement}', write_log=self.__class_log__)
                Result = []
            self.ElementHandle = Result
            return self
        else:
            self.log(f'Error : FindElements > Element Type : {TargetElement} [{str(type(TargetElement))}]', write_log=self.__class_log__)

    def FindValues(self, Elements=None, Value=None, ValueType=None, not_find_error=False, strip_value=False, retry_count:int=-1):
        """
            찾은 Element의 구성요소 값을 찾아서 ElementValueList에 갱신
            만약 ElementValueList에 Value값이 존재 한다면 ElementIndex에 갱신
            만약 ElementValue가 None 이라면 ElementValueList[0]을 ElementValue에 갱신
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
                get_value = ElementHandle[Index].get_attribute(ElementValueType)
                if get_value != None:
                    #GetValue = GetValue.decode('cp949')
                    if get_value == 'true':
                        GetValue = True
                    elif get_value == 'false':
                        GetValue = False
                    else:
                        GetValue = get_value
                    
                    if strip_value == True:
                        GetValue = GetValue.strip()

                else:
                    if ElementValueType == 'textContent' or ElementValueType == 'text':
                        GetValue = ElementHandle[Index].text

                ElementValueList.append(GetValue)

                self.log(f'FindValues > {TargetElement}[{Index}][{ElementValueType}] > "{GetValue}"', write_log=self.__class_log__)

                
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

    def WaitElement(self, Elements=None, Index=None, enabled=None, none_element:bool=False, none_error:bool=False, retry_count:int=-1):
        """
            Element가 나타날 때까지 대기 또는 사라질 때까지 대기
            다른 기본 함수에서 동작하기전 미리 선언하는 함수

            none_element : False > 나타날 때까지, True > 엘리먼트가 사라질 때까지
            none_error : False > 조건에 맞지 않으면 Error 발생, True > 조건에 맞지 않더라도 Error 발생시키지 않음
            retry_count : FindElements를 반복 하는 횟수
                if retry_count > 0:
                    retry = retry_count
                else:
                    retry = self.__retry__
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
                if enabled != None:
                    get_enabled = self.ElementHandle[ElementIndex].get_attribute('enabled')
                    if get_enabled == 'true':
                        check_enabled = True
                    else:
                        check_enabled = False

                    if check_enabled == enabled:
                        ElementHandle = [self.ElementHandle[ElementIndex]]
                    else:
                        ElementHandle = []
                else:
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

    def Click(self, Elements=None, Index=None, offset=(0,0), retry_count:int=-1):
        """
            찾은 Elements에서 Index 번째의 Element에 마우스 오버 및 클릭

            offset : 찾은 Element 중심에서 x y 만큼 이동해서 클릭

        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TargetElement = self.ElementHandle
        offset_x, offset_y = offset        
        
        self.WaitElement(TargetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                if offset_x != 0 or offset_y != 0:
                    bounds = ElementHandle.get_attribute('bounds')
                    bounds_split = bounds[:-1].replace('[','').split(']')
                    bounds_start = bounds_split[0].split(',')
                    bounds_end = bounds_split[1].split(',')

                    center_x = int((int(bounds_start[0]) + int(bounds_end[0]))/2)
                    center_y = int((int(bounds_start[1]) + int(bounds_end[1]))/2)

                    point_x = center_x + offset_x
                    point_y = center_y + offset_y

                    action = self.touchaction(self.driver)
                    action.press(x=point_x,y=point_y)
                    action.wait(1000)
                    action.release()
                    action.perform()
                else:
                    ElementHandle.click()
                self.log(f'Click > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)
                return self
            except:
                self.log(f'Click Error > {TargetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Click > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)

    def Send(self, Elements=None, Value=None, Index=None, clear:bool=True, enter:bool=False, hide_keyboard=True, retry_count:int=-1):
        """
            찾은 Elements의 Index 번째의 Element에 Value값을 입력
        
            clear : Value값 입력 전 전부 지우기 True
            enter : Value값 입력 후 enter 입력 False
            hide_keyboard : Value값 입력 후 키보드 숨기기  
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementValue__(Elements,Value)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        ElementValue = self.ElementValue
        TargetElement = self.ElementHandle

        self.WaitElement(TargetElement,Index=Index, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                if ElementValue != '':
                    if clear == True:
                        #자동으로 클리어 되는 경우가 있고 아닌 경우가 있어서 다시 추가
                        try:
                            ElementHandle.clear()
                        except:
                            pass
                        ElementHandle.send_keys(ElementValue)
                    else:
                        action = self.action()
                        action.send_keys(ElementValue).perform()

                    self.log(f'Send > {TargetElement}[{ElementIndex}] > "{ElementValue}"', write_log=self.__class_log__)

                if enter == True:
                    self.driver.press_keycode(66)
                
                if hide_keyboard == True:
                    time.sleep(self.__after__)
                    self.driver.hide_keyboard()
                return self
            except:
                self.log(f'Send Error > {TargetElement}[{ElementIndex}] > "{ElementValue}"\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Send > {TargetElement}[{ElementIndex}] > "{ElementValue}"', write_log=self.__class_log__)

    def GetAttribute(self, Elements=None, attribute_list=[
            'text','displayed','enabled','checked','selected','package',
            'class','resource-id','checkable','clickable','focusable','focused',
            'long-clickable','password','scrollable','bounds'], retry_count:int=-1):
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
                    if get_value != None:
                        if attribute == 'bounds':
                            #[0,262][1080,2501]
                            #0,262]1080,2501]
                            # 0 = [0, 262]
                            # 1 = [1080,2501]
                            bounds_split = get_value[:-1].replace('[','').split(']')
                            bounds0 = bounds_split[0].split(',')
                            bounds1 = bounds_split[1].split(',')
                            
                            get_attribute[attribute] = [[int(bounds0[0]),int(bounds0[1])],[int(bounds1[0]),int(bounds1[1])]]

                        elif attribute != 'textContent' or attribute != 'text':
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
                    self.log(f'GetAttribute Error > {TargetElement}[{Index}][{attribute}]\n{sys.exc_info()}', write_log=self.__class_log__)
            time.sleep(0.1)
            ElementAttribute.append(get_attribute)
    
        self.log(f'GetAttribute > {TargetElement} > {ElementAttribute}', write_log=self.__class_log__)
        self.ElementAttribute = ElementAttribute
        return self

    def Slide(self, TargetElements=None, TargetIndex=None, offset=(0,0), retry_count:int=-1):
        """
            ElementHandle의 ElementIndex번째 Element를
            TargetElements의 TargetIndex번째 위치로 슬라이드
            ElementHandle은 TargetElements로 갱신됨
            
            만약 TargetElements 값을 입력 하지 않으면 ElementHandle 위치 기점으로 offset 위치 까지 슬라이드
        """
        offset_x, offset_y = offset

        SoureceElement = self.ElementHandle
        if self.ElementIndex:
            Soureceindex = self.ElementIndex
        else:
            Soureceindex = 0

        if TargetElements:
            self.__ElementHandle__(TargetElements)
            TargetElement = self.ElementHandle
            self.ElementIndex = None
            self.__ElementIndex__(TargetElements,TargetIndex)
            Targetindex = self.ElementIndex
        else:
            TargetElement = SoureceElement
            Targetindex = Soureceindex

        self.WaitElement(SoureceElement,Index=Soureceindex, retry_count=retry_count)
        #self.screenshot(f'Scrolle')
        if len(self.ElementHandle) > 0:
            SoureceElementHandle = self.ElementHandle[Soureceindex]
            self.WaitElement(TargetElement,Index=Targetindex, retry_count=retry_count)
            if len(self.ElementHandle) > 0:
                TargetElementHandle = self.ElementHandle[Targetindex]
                try:

                    action = self.touchaction()
                    action.press(SoureceElementHandle)
                    action.wait(500)
                    action.move_to(TargetElementHandle,x=offset_x,y=offset_y)
                    action.release()
                    action.perform()
                    self.log(f'Slide > {TargetElement}[{Targetindex}] x:{offset_x},y:{offset_y}', write_log=self.__class_log__)
                    time.sleep(self.__after__)
                    #self.screenshot(f'Scrolle')
                    return self
                except:
                    self.log(f'Slide Error > {TargetElement}[{Targetindex}]\n{sys.exc_info()}', write_log=self.__class_log__)
                    time.sleep(self.__after__)
        #self.screenshot(f'Scrolle_Error')
        self.log(f'Error : Slide > {TargetElement}[{Targetindex}]', write_log=self.__class_log__)

    def LongPress(self, Elements=None, Index=None, offset=(0,0), duration=1, retry_count:int=-1):
        """
            찾은 Elements에서 Index 번째의 Element에 롱프레스
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TargetElement = self.ElementHandle
        offset_x, offset_y = offset
        
        self.WaitElement(TargetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            if offset_x != 0 or offset_y != 0:
                bounds = ElementHandle.get_attribute('bounds')
                bounds_split = bounds[:-1].replace('[','').split(']')
                bounds_start = bounds_split[0].split(',')
                bounds_end = bounds_split[1].split(',')

                center_x = int((int(bounds_start[0]) + int(bounds_end[0]))/2)
                center_y = int((int(bounds_start[1]) + int(bounds_end[1]))/2)

                if offset_x != None:
                    point_x = center_x + offset_x
                else:
                    point_x = center_x

                if offset_y != None:
                    point_y = center_y + offset_y
                else:
                    point_y = center_y

                action = self.touchaction()
                action.long_press(x=point_x, y=point_y, duration=duration*1000)
                action.release()
                action.perform()
            else:
                action = self.touchaction()
                action.long_press(el=ElementHandle, duration=duration*1000)
                action.release()
                action.perform()
            self.log(f'LongPress > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)
            return self
        self.log(f'Error : LongPress > {TargetElement}[{ElementIndex}]', write_log=self.__class_log__)

    def screenshot(self,file_name=None, screenshot_path=None):

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

    def element_screenshot(self, Elements, Index=0, file_name=None, screenshot_path=None):

        self.GetAttribute(Elements=Elements, attribute_list=['bounds'])

        bounds = self.ElementAttribute[Index]['bounds']

        if screenshot_path:
            __screenshot_path__ = screenshot_path
        else:
            __screenshot_path__ = self.__screenshot_path__

        if not(os.path.isdir(__screenshot_path__)):
            os.makedirs(os.path.join(__screenshot_path__))

        if file_name:
            origin_file_path = f'{__screenshot_path__}/{self.now_time("file")}_{file_name}_origin.png'
            file_path = f'{__screenshot_path__}/{self.now_time("file")}_{file_name}.png'
        else:
            origin_file_path = f'{__screenshot_path__}/{self.now_time("file")}_origin.png'
            file_path = f'{__screenshot_path__}/{self.now_time("file")}.png'

        self.driver.save_screenshot(origin_file_path)

        img = cv2.imread(origin_file_path)
        cv2.imwrite(file_path,img[bounds[0][1]:bounds[1][1],bounds[0][0]:bounds[1][0]])
        
        try:
            os.remove(origin_file_path)
        except:
            pass

        return file_path

    def recoding_start(self, timeLimit=1800):
        self.driver.start_recording_screen(timeLimit=timeLimit)

    def recoding_stop(self,file_name=None):
        if not(os.path.isdir(self.__screenshot_path__)):
            os.makedirs(os.path.join(self.__screenshot_path__))
        recode = self.driver.stop_recording_screen()
        with open(f'{self.__screenshot_path__}/{self.now_time("file")}_{file_name}.mp4', "wb") as recode_file:
            recode_file.write(base64.b64decode(recode))


    def touchaction(self):
        #https://github.com/appium/python-client/blob/7dbf4f2f7ce43f60eded19fa247bb2177b65bafd/README.md#multiactiontouchaction-to-w3c-actions
        action = self.action()
        action.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        return action.w3c_actions.pointer_action
    
    def action(self):
        return ActionChains(self.driver)

    def keycode(self, code):
        for _ in range(self.__retry__):
            try:
                self.driver.press_keycode(code)
                time.sleep(self.__after__)
                return self
            except:
                self.log(f'keycode Error > keycode > code {code}\n{sys.exc_info()}', write_log=self.__class_log__)
                time.sleep(self.__after__)
        self.log(f'Error : keycode > code {code}', write_log=self.__class_log__)

    def key_send(self, send_keys:list, wait=1):
        action = self.action()
        for send_key in send_keys:
            action_text = f' > "{send_key}"'
            action.send_keys(send_key).pause(seconds=wait)
        
        action.perform()
        self.log(f'key_send{action_text}')

    def key_home(self):
        #https://developer.android.com/reference/android/view/KeyEvent#KEYCODE_HOME
        self.keycode(3)
        
    def key_notification(self):
        self.keycode(83)

    def key_app_switch(self):
        self.keycode(187)

    def key_back(self):
        self.keycode(4)

    def touch_point(self, point=(0,0), wait=0):        
        action = self.touchaction()
        point_x, point_y = point
        self.func_log(f'{point}')
        action.pointer_down(x=point_x,y=point_y)
        action.pause(wait*1000)
        action.pointer_up(x=point_x,y=point_y)
        action.release()
        time.sleep(self.__after__)

    def slide_point(self, point=(0,0), point2=(0,0), wait=1):
        action = self.touchaction()
        point_x, point_y = point
        point2_x, point2_y = point2
        self.func_log(f'{point} > {point2}')
        action.pointer_down(x=point_x,y=point_y)
        action.pause(wait*1000)
        action.move_to(x=point2_x,y=point2_y)
        action.pointer_up(x=point_x,y=point_y)
        action.release()
        time.sleep(self.__after__)

    def slide_down(self,level=3, wait=1):
        point_x = int(self.driver_location['width']/2)
        point_y = int(self.driver_location['height']/2-self.driver_location['height']/8*level)
        move_y = int(self.driver_location['height']/2+self.driver_location['height']/8*level)
        
        point = (point_x, point_y)
        point2 = (point_x, move_y)

        self.slide_point(point=point, point2=point2, wait=wait)

    def slide_up(self,level=3,wait=1):
        point_x = int(self.driver_location['width']/2)

        point_y = int(self.driver_location['height']/2+self.driver_location['height']/8*level)
        move_y = int(self.driver_location['height']/2-self.driver_location['height']/8*level)

        point = (point_x, point_y)
        point2 = (point_x, move_y)

        self.slide_point(point=point, point2=point2, wait=wait)

    def slide_left(self,level=3, wait=1):
        point_x = int(self.driver_location['width']/2+self.driver_location['width']/8*level)
        move_x = int(self.driver_location['width']/2-self.driver_location['width']/8*level)
        point_y = int(self.driver_location['height']/2)
        point = (point_x, point_y)
        point2 = (move_x, point_y)

        self.slide_point(point=point, point2=point2, wait=wait)

    def slide_right(self,level=3,wait=1):
        point_x = int(self.driver_location['width']/2-self.driver_location['width']/8*level)
        move_x = int(self.driver_location['width']/2+self.driver_location['width']/8*level)
        point_y = int(self.driver_location['height']/2)

        point = (point_x, point_y)
        point2 = (move_x, point_y)
        self.slide_point(point=point, point2=point2, wait=wait)
    
    def slide_app_close(self, level=2):
        self.key_app_switch()
        self.slide_up(level=level)

    def app_start(self,app_id):
        self.driver.activate_app(app_id=app_id)

    def adb_shell(self, command, args):
        #args = {'command':'pm clear','args':'io.swit'}
        args = {'command':command,'args': args}
        self.driver.execute_script('mobile:shell',args)
        time.sleep(self.__after__)

    def adb_app_clear(self, app_id):
        self.adb_shell(command='pm clear',args=app_id)

    def adb_app_close(self, app_id):
        self.adb_shell(command='am force-stop',args=app_id)

    def adb_app_start(self, app_id):
        self.adb_shell(command='monkey',args=f'-p {app_id} -c android.intent.category.LAUNCHER 1')

    def hide_keyboard(self):
        self.driver.hide_keyboard()

    def check_element_img(self, Elements, template_img, Index=0, accuracy:int=0.8, debug=False):
        base_img = self.element_screenshot(Elements=Elements, Index=Index)
        result = self.check_img(template_img=template_img, base_img=base_img, base_crop=[], accuracy=accuracy, debug=debug)
        return result

    def touch_element_img(self, Elements, template_img, Index=0, accuracy=0.8, offset=(0,0), wait=0, find_index=0):
        '''
            전체 사이즈
            엘리먼트 좌표
                - 이미지 좌표
            
            터치 > 엘리먼트 좌표 + 이미지 좌표

        '''
        img_points = self.check_element_img(Elements=Elements, template_img=template_img, Index=Index, accuracy=accuracy)
        bounds = self.ElementAttribute[Index]['bounds']
        if img_points:
            offset_x, offset_y = offset
            center_x, center_y = img_points[find_index]
            point_x = center_x + offset_x + bounds[0][0]
            point_y = center_y + offset_y + bounds[0][1]

            self.touch_point((point_x,point_y), wait=wait)
        else:
            self.func_log(-1,f'not find img', write_log=self.__class_log__)

    def touch_img(self, template_img, base_img, base_crop=[], accuracy=0.8, offset=(0,0), wait=0, find_index=0):
        img_points = self.check_img(base_img=base_img, template_img=template_img, base_crop=base_crop, accuracy=accuracy)
        if img_points:
            offset_x, offset_y = offset
            center_x, center_y = img_points[find_index]
            point_x = center_x + offset_x
            point_y = center_y + offset_y

            self.touch_point((point_x,point_y), wait=wait)
        else:
            self.func_log(-1,f'not find img', write_log=self.__class_log__)
