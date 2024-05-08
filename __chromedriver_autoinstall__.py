
import requests, sys, os, subprocess
import chromedriver_autoinstaller, pyzipper
import shutil


#win64
#mac-arm64
#win32
#mac-x64
#linux64

def chrome_driver_install_path():
    run_os = sys.platform
    if run_os == 'darwin':
        platform = 'mac-x64'
    elif run_os == 'win32':
        platform = 'win64'
    else:
        platform = run_os
    try:
        file_list = os.listdir('./driver')
        file_list.sort()
        for item_index in range(len(file_list)-1):
            version_path = f'./driver/{file_list[item_index]}'
            #print(version_path)
            shutil.rmtree(version_path)
    except:
        pass

    def path_create(path):
        if not(os.path.isdir(path)):
            try:
                os.makedirs(os.path.join(path))
                return True
            except:
                print(sys.exc_info())
                return False

    def unzip(zip_path, unzip_path, password=''):
        if password != '':
            with pyzipper.AESZipFile(zip_path) as zf:
                zf.extractall(path=unzip_path, pwd=str.encode(password))
        else:
            with pyzipper.AESZipFile(zip_path) as zf:
                zf.extractall(path=unzip_path)

    def download(url:str, file_path:str='./'):

        url_split = url.split('/')
        file_name = url_split[-1]
        result = f'{file_path}/{file_name}'

        download_requests = requests.get(url)
        #if os.path.exists(result): 
        #    os.remove(result)

        open(result, 'wb').write(download_requests.content)

        return result

    def chk_ver_split(v1:str,v2:str,count=4):
        v1_split = v1.split('.')
        v2_split = v2.split('.')

        for num in range(count):
            if v1_split[num] != v2_split[num]:
                return False
            
        return True

    def download_url(driver_info):
        #win64
        #mac-arm64
        #win32
        #mac-x64
        #linux64
        #print(platform)
        result = ''
        for platform_info in  driver_info['downloads']['chromedriver']:
            if platform_info['platform'] == platform:
                result = platform_info['url']
        return result

    url = 'https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json'

    base_path = os.path.dirname(os.path.abspath(__file__))
    driver_folder = f'{base_path}/driver'
    path_create(driver_folder)

    chrome_ver = chromedriver_autoinstaller.get_chrome_version()
    driver_list = requests.get(url).json()['versions']

    count4 = []
    count3 = []
    for driver_info in driver_list:
        driver_ver = driver_info['version']
        if 'chromedriver' in driver_info['downloads'].keys():
            if chk_ver_split(v1=chrome_ver, v2=driver_ver, count=4) == True:
                    count4.append(driver_info)

            elif chk_ver_split(v1=chrome_ver, v2=driver_ver, count=3) == True:
                count3.append(driver_info)


    #print(count4)
    #print(count3)
    #print(chrome_ver)


    
    if count4:
        chrome_path = download_url(count4[0])
    else:
        if count3:
            chrome_path = download_url(count3[-1])
        else:
            return chromedriver_autoinstaller.install()

    #print(chrome_path)

    driver_folder_ver = f'{driver_folder}/{chrome_ver}'
    path_create(driver_folder_ver)


    if platform == 'win64':
        result = f'{driver_folder_ver}/chromedriver-win64/chromedriver.exe'
    elif platform == 'mac-x64':
        result = f'{driver_folder_ver}/chromedriver-mac-x64/chromedriver'
    else:
        result = '코드 확인 필요'

    if not os.path.exists(result):
        download_path = download(chrome_path,driver_folder_ver)
        unzip(zip_path=download_path, unzip_path=driver_folder_ver)
    #print(result)

    if platform == 'mac-x64':
        run_path = ['chmod',f'+x',f'{result}']
        subprocess.run(run_path)
    
    return result


#chrome_driver_install_path()
