# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import hashlib
import pyautogui
import time, os
from cv2 import cv2
from pathlib import Path
import numpy as np
#from matplotlib import pyplot as plt

def get_hash(file_path, func_type='md5'):
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
        
def find_img_position(file_path, region=(), confidence:int=0.75, grayscale:bool=True, retry:int=5, wait:int=1):
    '''
        https://pyautogui.readthedocs.io/en/latest/screenshot.html

    '''

    for _ in range(retry):
        result = pyautogui.locateOnScreen(file_path, confidence=confidence, region=region, grayscale=grayscale)
        if result != None:
            return result
        else:
            time.sleep(wait)
    
def check_file_hash(check_hash, target_path, hash_type='md5'):
    target_hash = get_hash(file_path=target_path, func_type=hash_type)
    if check_hash != target_hash:
        raise Exception(f'check_hash: "{check_hash}" != target_hash: "{target_hash}"')

def check_img(img_path, img_path2, accuracy:int=0.3):
    img_array1 = np.fromfile(Path(img_path), np.uint8)
    img_array2 = np.fromfile(Path(img_path2), np.uint8)

    img1 = cv2.imdecode(img_array1,0)
    img2 = cv2.imdecode(img_array2,0)

    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)
    good = []
    for m,n in matches:
        if m.distance < accuracy*n.distance:
            good.append(kp1[m.queryIdx].pt)

    print(f'check_img > result: [{len(good)}]{good}')
    return len(good)

def check_img_screen(driver, check_img_path, accuracy=0.3, pass_count=1):
    screenshot_path = driver.screenshot(file_name='check_img_screen')
    good_count = check_img(img_path=screenshot_path,img_path2=check_img_path, accuracy=accuracy)

    if pass_count > good_count:
        raise Exception(f'not find img : pass_count: {pass_count} > good_count: {good_count}')

    return screenshot_path