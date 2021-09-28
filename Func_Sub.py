# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import hashlib
import pyautogui
import time, os
from cv2 import cv2
#import numpy as np
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
        raise Exception(f'func_type error')
        
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
    
def check_file_hash(check_hash, taget_path, hash_type='md5'):
    taget_hash = get_hash(file_path=taget_path, func_type=hash_type)
    if check_hash != taget_hash:
        raise Exception(f'check_hash: "{check_hash}" != taget_hash: "{taget_hash}"')

def check_img(img_path, img_path2, accuracy:int=0.3):
    img1 = cv2.imread(img_path,0)
    img2 = cv2.imread(img_path2,0)
    try:
        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1,None)
        kp2, des2 = sift.detectAndCompute(img2,None)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)
        good = []
        for m,n in matches:
            if m.distance < accuracy*n.distance:
                good.append([m])

        if kp1 == kp2:
            pass
            #img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
            #plt.imshow(img3),plt.show()
            #print(good)
            #print(len(good))
            #knn_image = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
            #plt.imshow(knn_image)
            #plt.show()
        print(f'check_img > result: {len(good)}')
        return len(good)
    except:
        return 0

def check_img_screen(driver, check_img_path, accuracy=0.3, pass_count=1):
    screenshot_path = driver.screenshot(file_name='check_img_screen')
    good_count = check_img(img_path=screenshot_path,img_path2=check_img_path, accuracy=accuracy)

    if pass_count > good_count:
        raise Exception(f'not find img : pass_count: {pass_count} > good_count: {good_count}')

    return screenshot_path