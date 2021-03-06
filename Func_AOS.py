# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#https://selenium-python.readthedocs.io/api.html#selenium.webdriver.common.touch_actions.TouchActions.scroll

import time, os, base64, sys
from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.touch_action import TouchAction

#from Func_Common import NowTime
#from Func_Common import path_create

__platform__ = 'AOS'
__script_path__ = f'{os.path.dirname(os.path.abspath(__file__))}'
__time__ = time.strftime(f'%Y%m%d_%H%M%S',time.localtime(time.time()))

class AOS:
    def __init__(self, DeviceInfo, AppiumServerInfo={'ip':'127.0.0.1','port':'4723'}, Delay={'retry':5, 'after':1}, ClassOption={}):
        '''
            DeviceInfo = desired_capabilities
            {
                'uuid': uuid,
                'newCommandTimeout' : timeout second
                ...
            }

            AppiumServerInfo =
            {
                'ip': appium ip,
                'port' : appium port
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
                'class_name' = class name > log > "{time} {class_name} {log_text}",
                'element_type' = id, xpath etc...
                'class_log' = True, class in func log write
            }
        '''
        self.__device_info__ = DeviceInfo
        
        if 'ip' in AppiumServerInfo.keys():
            self.__appium_ip__ = AppiumServerInfo['ip']
        else:
            self.__appium_ip__ = '127.0.0.1'

        if 'port' in AppiumServerInfo.keys():
            self.__appium_port__ = AppiumServerInfo['port']
        else:
            self.__appium_port__ = '4723'

        self.__appium_host__ = f'http://{self.__appium_ip__}:{self.__appium_port__}/wd/hub'

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
            self.__element_type__ = 'id'

        if 'class_log' in ClassOption.keys():
            self.__class_log__ = ClassOption['class_log']
        else:
            self.__class_log__ = True

        if 'warning_collection' in ClassOption.keys():
            self.__warning_collection__ = ClassOption['warning_collection']
        else:
            self.__warning_collection__ = True

        if 'retry' in Delay:
            self.__retry__ = Delay['retry']
        else:
            self.__retry__ = 5

        if 'after' in Delay:
            self.__after__ = Delay['after']
        else:
            self.__after__ = 1

        self.__error__ = ''
        self.warning_list = []   
        self.class_data_01 = ''
        self.class_data_02 = ''
        self.class_data_03 = ''
        self.class_data_04 = ''

        self.driver = webdriver.Remote(command_executor=self.__appium_host__, desired_capabilities=self.__device_info__)

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
            Index : ?????? Elements??? ?????? ????????? ???????????? ?????? ?????? ????????? 0
            ???????????? : Index > ElementIndex > Elements > 0
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
            Value : ?????? Elements?????? ????????? ???
            type :  str
            ???????????? : Value > ElementValue > Elements > None
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
            ValueType : Value?????? ??????
            type :  str
            ???????????? : Value > ElementValueType > Elements > 'textContent'
        '''

        if ValueType == None:
            if self.ElementValueType == None:
                if 'dict' in str(type(Elements)) and 'ValueType' in Elements:
                    self.ElementValueType = Elements['ValueType']
                else:
                    self.ElementValueType = 'text'
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
        if self.__warning_collection__ == True:
            if str(log_text)[0:7].lower() == 'warning':
                self.warning_list.append(log_text)
        
        if str(log_text)[0:5].lower() == 'error':
            self.__error__ = f'[{self.__class_name__}]\t{str(log_text)}'
            log_write = f'{self.now_time()}\t[{self.__class_name__}]\t{str(log_text)}\n'
        else:
            log_write = f'{self.now_time()}\t[{self.__class_name__}]\t{str(log_text)}\n'
        
        if print_log == True:
            print(log_write, end='')

        if write_log == True:
            try:
                log_file = open(self.__log_file_path__, "a", encoding="utf-16")
                log_file.write(f'{log_write}')
                log_file.close()
            except:
                print(sys.exc_info())

        if str(log_text)[0:5].lower() == 'error':
            raise Exception(f'{self.__error__}')

    def FindElements(self, Elements):
        """

            ????????? ?????? ?????? Elements ?????? ?????? ?????? ???
            ElementHandle??? ??????
            
            Elements = {
                'Type' : 'id',
                'Taget' : 'element'
            }

        """
        self.__ElementHandle__(Elements)
        TagetElement = self.ElementHandle
            
        if 'list' in str(type(TagetElement)):
            #?????? ????????? WebElement ??????
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
                Result = self.driver.find_elements(ElementType, ElementTaget)
            except:
                self.log(f'Error : FindElements > Element Type : {ElementType} {TagetElement} [{str(type(TagetElement))}]\n{sys.exc_info()}', write_log=self.__class_log__)

            if len(Result) == 0:
                self.log(f'FindElements > Not Find >{TagetElement}', write_log=self.__class_log__)
                Result = []
            self.ElementHandle = Result
            return self
        else:
            self.log(f'Error : FindElements > Element Type : {TagetElement} [{str(type(TagetElement))}]', write_log=self.__class_log__)

    def FindValues(self, Elements=None, Value=None, ValueType=None, not_find_error=False, retry_count:int=-1):
        """
            ?????? Element??? ???????????? ?????? ????????? ElementValueList??? ??????
            ?????? ElementValueList??? Value?????? ?????? ????????? ElementIndex??? ??????
            ?????? ElementValue??? None ????????? ElementValueList[0]??? ElementValue??? ??????
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
                get_value = ElementHandle[Index].get_attribute(ElementValueType)
                #GetValue = GetValue.decode('cp949')
                if get_value == 'true':
                    GetValue = True
                elif get_value == 'false':
                    GetValue = False
                else:
                    GetValue = get_value
                self.log(f'FindValues > {TagetElement}[{Index}] > "{GetValue}"', write_log=self.__class_log__)
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
            Element??? ????????? ????????? ?????? ?????? ????????? ????????? ??????
            ?????? ?????? ???????????? ??????????????? ?????? ???????????? ??????

            none_element : False > ????????? ?????????, True > ??????????????? ????????? ?????????
            none_error : False > ????????? ?????? ????????? Error ??????, True > ????????? ?????? ???????????? Error ??????????????? ??????
            retry_count : FindElements??? ?????? ?????? ??????
                if retry_count > 0:
                    retry = retry_count
                else:
                    retry = self.__retry__
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
            self.log(f'Error : WaitElement [none_element:{none_element}] > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
        else:
            self.log(f'WaitElement [none_element:{none_element}] > {TagetElement}[{ElementIndex}] > Pass', write_log=self.__class_log__)
            return self

    def Click(self, Elements=None, Index=None, offset={'x':None,'y':None}, retry_count:int=-1):
        """
            ?????? Elements?????? Index ????????? Element??? ????????? ?????? ??? ??????

            offset : ?????? Element ???????????? x y ?????? ???????????? ??????

        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle
        if 'x' in offset.keys():
            offset_x = offset['x']
        else:
            offset_x = None

        if 'y' in offset.keys():
            offset_y = offset['y']
        else:
            offset_y = None
        

        self.WaitElement(TagetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                if offset_x != None or offset_y != None:
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

                    action = TouchAction(self.driver)
                    action.press(x=point_x,y=point_y)
                    action.wait(1000)
                    action.release()
                    action.perform()
                else:
                    ElementHandle.click()
                self.log(f'Click > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
                return self
            except:
                self.log(f'Click Error > {TagetElement}[{ElementIndex}]\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Click > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)

    def Send(self, Elements=None, Value=None, Index=None, clear:bool=True, enter:bool=False, hide_keyboard=True, retry_count:int=-1):
        """
            ?????? Elements??? Index ????????? Element??? Value?????? ??????
        
            clear : Value??? ?????? ??? ?????? ????????? True
            enter : Value??? ?????? ??? enter ?????? False
            hide_keyboard : Value??? ?????? ??? ????????? ?????????  
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementValue__(Elements,Value)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        ElementValue = self.ElementValue
        TagetElement = self.ElementHandle

        self.WaitElement(TagetElement,Index=Index, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            try:
                if ElementValue != '':
                    if clear == True:
                        #???????????? ????????? ?????? ????????? ?????? ?????? ????????? ????????? ?????? ??????
                        try:
                            ElementHandle.clear()
                        except:
                            pass
                        ElementHandle.send_keys(ElementValue)
                    else:
                        action = self.action()
                        action.send_keys(ElementValue).perform()

                    self.log(f'Send > {TagetElement}[{ElementIndex}] > "{ElementValue}"', write_log=self.__class_log__)

                if enter == True:
                    self.driver.press_keycode(66)
                
                if hide_keyboard == True:
                    time.sleep(self.__after__)
                    self.driver.hide_keyboard()
                return self
            except:
                self.log(f'Send Error > {TagetElement}[{ElementIndex}] > "{ElementValue}"\n{sys.exc_info()}', write_log=self.__class_log__)
        self.log(f'Error : Send > {TagetElement}[{ElementIndex}] > "{ElementValue}"', write_log=self.__class_log__)

    def GetAttribute(self, Elements=None, attribute_list=[
            'text','displayed','enabled','checked','selected','package',
            'class','resource-id','checkable','clickable','focusable','focused',
            'long-clickable','password','scrollable','bounds'], retry_count:int=-1):
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

    def Slide(self, TagetElements=None, TagetIndex=None, offset:dict={'x':0,'y':0}, retry_count:int=-1):
        """
            ElementHandle??? ElementIndex?????? Element???
            TagetElements??? TagetIndex?????? ????????? ????????????
            ElementHandle??? TagetElements??? ?????????
            
            ?????? TagetElements ?????? ?????? ?????? ????????? ElementHandle ?????? ???????????? offset ?????? ?????? ????????????
        """
        offset_x = offset['x']
        offset_y = offset['y']

        SoureceElement = self.ElementHandle
        if self.ElementIndex:
            Soureceindex = self.ElementIndex
        else:
            Soureceindex = 0

        if TagetElements:
            self.__ElementHandle__(TagetElements)
            TagetElement = self.ElementHandle
            self.ElementIndex = None
            self.__ElementIndex__(TagetElements,TagetIndex)
            Tagetindex = self.ElementIndex
        else:
            TagetElement = SoureceElement
            Tagetindex = Soureceindex

        self.WaitElement(SoureceElement,Index=Soureceindex, retry_count=retry_count)
        #self.screenshot(f'Scrolle')
        if len(self.ElementHandle) > 0:
            SoureceElementHandle = self.ElementHandle[Soureceindex]
            self.WaitElement(TagetElement,Index=Tagetindex, retry_count=retry_count)
            if len(self.ElementHandle) > 0:
                TagetElementHandle = self.ElementHandle[Tagetindex]
                try:

                    action = self.touchaction()
                    action.press(SoureceElementHandle)
                    action.wait(500)
                    action.move_to(TagetElementHandle,x=offset_x,y=offset_y)
                    action.release()
                    action.perform()
                    self.log(f'Slide > {TagetElement}[{Tagetindex}] x:{offset_x},y:{offset_y}', write_log=self.__class_log__)
                    time.sleep(self.__after__)
                    #self.screenshot(f'Scrolle')
                    return self
                except:
                    self.log(f'Slide Error > {TagetElement}[{Tagetindex}]\n{sys.exc_info()}', write_log=self.__class_log__)
                    time.sleep(self.__after__)
        #self.screenshot(f'Scrolle_Error')
        self.log(f'Error : Slide > {TagetElement}[{Tagetindex}]', write_log=self.__class_log__)

    def LongPress(self, Elements=None, Index=None, offset={'x':None,'y':None}, duration=1, retry_count:int=-1):
        """
            ?????? Elements?????? Index ????????? Element??? ????????????
        """
        self.__ElementIndex__(Elements,Index)
        self.__ElementHandle__(Elements)
        ElementIndex = self.ElementIndex
        TagetElement = self.ElementHandle
        if 'x' in offset.keys():
            offset_x = offset['x']
        else:
            offset_x = None

        if 'y' in offset.keys():
            offset_y = offset['y']
        else:
            offset_y = None
        
        self.WaitElement(TagetElement,Index=ElementIndex, retry_count=retry_count)
        if len(self.ElementHandle) > 0:
            ElementHandle = self.ElementHandle[ElementIndex]
            if offset_x != None or offset_y != None:
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
            self.log(f'LongPress > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)
            return self
        self.log(f'Error : LongPress > {TagetElement}[{ElementIndex}]', write_log=self.__class_log__)

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


    def recoding_start(self, timeLimit=1800):
        self.driver.start_recording_screen(timeLimit=timeLimit)

    def recoding_stop(self,file_name=None):
        if not(os.path.isdir(self.__screenshot_path__)):
            os.makedirs(os.path.join(self.__screenshot_path__))
        recode = self.driver.stop_recording_screen()
        with open(f'{self.__screenshot_path__}/{self.now_time("file")}_{file_name}.mp4', "wb") as recode_file:
            recode_file.write(base64.b64decode(recode))


    def touchaction(self):
        return TouchAction(self.driver)

    def action(self):
        return ActionChains(self.driver)

    def keycode(self,code):
        for _ in range(self.__retry__):
            try:
                self.driver.press_keycode(code)
                time.sleep(self.__after__)
                return self
            except:
                self.log(f'keycode Error > keycode > code {code}\n{sys.exc_info()}', write_log=self.__class_log__)
                time.sleep(self.__after__)
        self.log(f'Error : keycode > code {code}', write_log=self.__class_log__)

    def key_home(self):
        #https://developer.android.com/reference/android/view/KeyEvent#KEYCODE_HOME
        self.keycode(3)


    def key_app_switch(self):
        self.keycode(187)

    def key_back(self):
        self.keycode(4)

    def touch_point(self, point:dict={'x':0,'y':0}, wait=0):        
        action = self.touchaction()
        point_x = point['x']
        point_y = point['y']
        
        action.press(x=point_x,y=point_y)
        action.wait(wait*1000)
        action.release()
        action.perform()
        time.sleep(self.__after__)

    def slide_point(self, point:dict={'x':0,'y':0}, point2:dict={'x':0,'y':0}, wait=1):
        action = self.touchaction()
        point_x = point['x']
        point_y = point['y']
        point2_x = point2['x']
        point2_y = point2['y']

        action.press(x=point_x,y=point_y)
        action.wait(wait*1000)
        action.move_to(x=point2_x,y=point2_y)
        action.release()
        action.perform()
        time.sleep(self.__after__)

    def slide_down(self,level=3,wait=1):
        point_x = int(self.driver_location['width']/2)
        point_y = int(self.driver_location['height']/2-self.driver_location['height']/8*level)
        move_y = int(self.driver_location['height']/2+self.driver_location['height']/8*level)
        
        action = self.touchaction()
        action.press(x=point_x,y=point_y)
        action.wait(wait*1000)
        action.move_to(x=point_x,y=move_y)
        action.release()
        action.perform()
        time.sleep(self.__after__)

    def slide_up(self,level=3,wait=1):
        point_x = int(self.driver_location['width']/2)

        point_y = int(self.driver_location['height']/2+self.driver_location['height']/8*level)
        move_y = int(self.driver_location['height']/2-self.driver_location['height']/8*level)
        
        action = self.touchaction()
        action.press(x=point_x,y=point_y)
        action.wait(wait*1000)
        action.move_to(x=point_x,y=move_y)
        action.release()
        action.perform()
        time.sleep(self.__after__)

    def slide_left(self,level=3, wait=1):
        point_x = int(self.driver_location['width']/2+self.driver_location['width']/8*level)
        move_x = int(self.driver_location['width']/2-self.driver_location['width']/8*level)

        point_y = int(self.driver_location['height']/2)

        action = self.touchaction()
        action.press(x=point_x,y=point_y)
        action.wait(wait*1000)
        action.move_to(x=move_x,y=point_y)
        action.release()
        action.perform()
        time.sleep(self.__after__)

    def slide_right(self,level=3,wait=1):
        point_x = int(self.driver_location['width']/2-self.driver_location['width']/8*level)
        move_x = int(self.driver_location['width']/2+self.driver_location['width']/8*level)

        point_y = int(self.driver_location['height']/2)

        action = self.touchaction()
        action.press(x=point_x,y=point_y)
        action.wait(wait*1000)
        action.move_to(x=move_x,y=point_y)
        action.release()
        action.perform()
        time.sleep(self.__after__)
    
    def app_close(self):
        self.key_app_switch()
        self.slide_up(level=2)

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
        self.adb_shell(command='am start',args=app_id)