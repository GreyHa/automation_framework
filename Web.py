# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os, time
from .supportmodule.Web import module_class as Web_module

class Web(Web_module):
    def __init__(self, clientinfo={}):
        '''
            clientinfo =
            {
                'retry' : if fail retry count,
                'after' : action delay second,
                'screenshot_path' = save folder path,
                'log_file_path' = log file full path,
                'class_name' = class name > log > "{time} {class_name} {log_text}"
                'element_type' = css selector, xpath etc...
                'class_log' = True, class in func log write
            }
        '''
        self.__client_info__:dict = clientinfo
        
        self.__platform__ = 'Web'
        self.__script_path__ = f'{os.path.dirname(os.path.abspath(__file__))}'
        self.__start_time__ = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))
        
        self.__screenshot_path__ = self.dict_value(self.__client_info__, key='screenshot_path', not_find_data=f'{self.__script_path__}/screenshot/{self.__start_time__}')
        self.__log_file_path__ = self.dict_value(self.__client_info__, key='log_file_path', not_find_data=f'{self.__script_path__}/log/{self.__start_time__}.txt')

        self.__class_name__ = self.dict_value(self.__client_info__, key='class_name', not_find_data=self.__platform__)
        self.__element_type__ = self.dict_value(self.__client_info__, key='element_type', not_find_data='css selector')
        self.__class_log__ = self.dict_value(self.__client_info__, key='class_log', not_find_data=True)
        self.__print_log__ = self.dict_value(self.__client_info__, key='print_log', not_find_data=True)        
        self.__log_collection__ = self.dict_value(self.__client_info__, key='log_collection', not_find_data=False)

        self.__retry__ = self.dict_value(self.__client_info__, key='retry', not_find_data=5)
        self.__after__ = self.dict_value(self.__client_info__, key='after', not_find_data=1)

        self.__debuggerAddress__ = ''
        self.__debugger_ip__ = ''
        self.__debugger_port__ = ''
        self.__error__ = ''
        self.all_log_list = []
        self.func_log_list = []

        self.path_create(os.path.dirname(self.__log_file_path__))
        self.path_create(self.__screenshot_path__)
               
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