# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import time, os
from pathlib import Path
import pyautogui, numpy, cv2
from supportmodule.common import module_class as common_module

class module_class(common_module):
    def find_img_position(self, file_path, region=(), confidence:int=0.75, grayscale:bool=True, retry:int=5, wait:int=1):
        '''
            https://pyautogui.readthedocs.io/en/latest/screenshot.html

        '''

        for _ in range(retry):
            result = pyautogui.locateOnScreen(file_path, confidence=confidence, region=region, grayscale=grayscale)
            if result != None:
                return result
            else:
                time.sleep(wait)

    def check_img(self, img_path, img_path2, accuracy:int=0.3):
        img_array1 = numpy.fromfile(Path(img_path), numpy.uint8)
        img_array2 = numpy.fromfile(Path(img_path2), numpy.uint8)

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
        return good

    def check_img_screen(self, check_img_path, accuracy=0.3, pass_count=1):
        '''
            AOS
        '''
        screenshot_path = self.driver.screenshot(file_name='check_img_screen')
        good_count = self.check_img(img_path=screenshot_path,img_path2=check_img_path, accuracy=accuracy)

        if pass_count > good_count:
            raise Exception(f'not find img : pass_count: {pass_count} > good_count: {good_count}')

        return screenshot_path
    
    def check_img(self, template_img, base_img, base_crop=[], accuracy:int=0.8, debug=False):
        '''
            base_crop = [(start_y,end_y), (start_x,end_x)] or [bounds[0][1]:bounds[1][1],bounds[0][0]:bounds[1][0]]
        '''
        if base_img:
            img = cv2.imread(base_img)
        else:
            screenshot_path = self.screenshot(file_name='temp_screenshot',screenshot_path=self.__screenshot_path__)
            img = cv2.imread(screenshot_path)
            try:
                os.remove(screenshot_path)
            except:
                pass
        result = []

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if base_crop:
            imgGray[base_crop[0][0]:base_crop[0][1], base_crop[1][0]:base_crop[1][1]]

        target = cv2.imread(template_img, cv2.IMREAD_GRAYSCALE)
        w, h = target.shape[::-1]
        res = cv2.matchTemplate(imgGray, target, cv2.TM_CCOEFF_NORMED)

        accuracy = 0.8
        loc = numpy.where(res>=accuracy)
        for pt in zip(*loc[::-1]):
            result.append((int(pt[0]), int(pt[1])))
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2) # 결과값에 사각형을 그린다

        if debug == True:
            cv2.imshow("img", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        self.func_log(0,f'result: [{len(result)}]{result}')
        return result