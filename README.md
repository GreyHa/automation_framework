# automation_framework
# selenium, appium 기반으로 작성
pip install Appium-Python-Client

pip install selenium

# web 모듈은 현재 크롬을 고정으로 사용
https://chromedriver.chromium.org/downloads
https://pypi.org/project/chromedriver-autoinstaller/

pip install chromedriver-autoinstaller

import chromedriver_autoinstaller
chromedriver_path = chromedriver_autoinstaller.install()

# 사용중인 크롬을 디버그 하려면 아래 방법으로 실행해서 연결 필요
windows

chrome.exe --remote-debugging-port=9223 --user-data-dir=c:\test

mac

/Applications//Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9223 --user-data-dir="/Users/grey/Chrome-user01"

# AOS adb 기능을 사용하려면 옵션 켜야함
appium --allow-insecure=adb_shell


# Sub 이미지 인식 등 서브 모듈
pip install pyautogui
pip install opencv-python
pip install opencv-contrib
