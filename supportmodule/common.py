# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import time, os, sys, hashlib, inspect, traceback, base64
from pathlib import Path

class module_class:
    def compare(self, target1, target2, compare_type='==', pass_type=0, fail_type=-1):
        compare_text = f'"{target1}" {compare_type} "{target2}"'
        
        compare_list = ['!=', '==', '>=', '<=', '>', '<', 'in', 'not in']
        if compare_type in compare_list:
            if compare_type == '!=' and target1 != target2:
                return pass_type, compare_text

            elif compare_type == '==' and target1 == target2:
                return pass_type, compare_text

            elif compare_type == '>=' and target1 >= target2:
                return pass_type, compare_text

            elif compare_type == '<=' and target1 <= target2:
                return pass_type, compare_text

            elif compare_type == '>' and target1 > target2:
                return pass_type, compare_text

            elif compare_type == '<' and target1 < target2:
                return pass_type, compare_text

            elif compare_type == 'in' and target1 in target2:
                return pass_type, compare_text

            elif compare_type == 'not in' and target1 not in target2:
                return pass_type, compare_text
            else:
                return fail_type, f'fail > ({compare_text})'
        else:
            raise Exception(f'compare_type: "{compare_type}" not in compare_list: {compare_list}')

    def func_log(self, log_text:str='', log_type:int=0):
        '''
            log_type : 0 > by pass
            log_tpye : 1 > start
            log_tpye : 2 > check
            log_tpye : 3 > end
            log_tpye : -2 > Warning
            log_tpye : -1 > Error
        '''
        func_name = inspect.stack()[1][3]

        if log_type == 1:
            text = f'[{func_name}][START]\n{log_text}'
            
        elif log_type == 2:
            text = f'[{func_name}][CHECK]\n{log_text}'

        elif log_type == 3:
            text = f'[{func_name}][END]\n{log_text}'

        else:
            text = f'[{func_name}]\n{log_text}'

        if self.__log_collection__ == True:
            self.func_log_list.append(text)
            if log_type == 3:
                self.func_log_list = []
        
        self.log(text, log_type=log_type, write_log=self.__class_log__)
        return log_type

    def compare_log(self, target1, target2, compare_type:str='==', pass_type=0, fail_type=-1, log_text:str=''):
        '''
            pass_type, fail_type
            log_type : 0 > by pass < pass_type
            log_tpye : 1 > start
            log_tpye : 2 > check
            log_tpye : 3 > end
            log_tpye : -2 > Warning
            log_tpye : -1 > Error < fail_type

            return log_type
        '''
        log_type, log_text2 = self.compare(target1,target2,compare_type=compare_type,pass_type=pass_type,fail_type=fail_type)
        
        if log_text:
            text = f'{log_text} : {log_text2}'
        else:
            text = log_text2

        self.func_log(log_text=text, log_type=log_type)

        return log_type

    def sleep(self, second=None):
        if second == None:
            time.sleep(self.__after__)
            self.log(f'sleep: {self.__after__}s')
        
        else:
            time.sleep(second)
            self.log(f'sleep: {second}s')

    def dict_value(self, target:dict, key:str, not_find_data=None, not_find_error=False):
        if key in target.keys():
            return target[key]
        else:
            if not_find_error == False:
                return not_find_data
            else:
                raise Exception(f'not find key\n target: {target}\nkey: "{key}"')

    def now_time(self, return_type='text'):
        if return_type.lower() == 'file':
            return time.strftime(f'%Y%m%d_%H%M%S',time.localtime(time.time()))
        elif return_type.lower() == 'text':
            return time.strftime(f'%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    def path_create(self, dir_path):
        if dir_path:
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(os.path.join(dir_path))
                except:
                    print(f'{traceback.format_exc()}\n"{dir_path}"')

    def log(self, log_text, log_type=0, write_log:bool=True):
        if self.__log_collection__ == True:
            self.all_log_list.append(log_text)
        
        if log_type == -1:
            self.__error__ = f'[{self.__class_name__}]\t{str(log_text)}'
            log_write = f'{self.now_time()}\t[{self.__class_name__}]\t{str(log_text)}\n'
        else:
            log_write = f'{self.now_time()}\t[{self.__class_name__}]\t{str(log_text)}\n'
        
        if self.__print_log__ == True:
            try:
                print(log_write, end='')
            except:
                print(traceback.format_exc())

        if write_log == True:
            try:
                log_file = open(self.__log_file_path__, "a", encoding="utf-8")
                log_file.write(f'{log_write}')
                log_file.close()
            except:
                print(sys.exc_info())

        if log_type == -1:
            raise Exception(f'{self.__error__}')

    def get_hash(self, file_path, func_type='md5'):
        '''
            func_type: 'md5', 'sha-1', 'sha-256'
        '''

        FileOpen = open(file_path, 'rb')
        FileData = FileOpen.read()
        FileOpen.close()

        if func_type.lower() == 'md5':
            return hashlib.md5(FileData).hexdigest()

        elif func_type.lower() == 'sha-1':
            return hashlib.sha1(FileData).hexdigest()

        elif func_type.lower() == 'sha-256':
            return hashlib.sha256(FileData).hexdigest()

        else:
            raise Exception('func_type error')
        
    def check_file_hash(self, check_hash, target_path, hash_type='md5'):
        target_hash = self.get_hash(file_path=target_path, func_type=hash_type)
        if check_hash != target_hash:
            self.log(f'Error\ncheck_hash: "{check_hash}"\ntarget_hash: "{target_hash}"', -1)