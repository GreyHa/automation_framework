# -*- coding: utf-8 -*-
#!/usr/bin/env python3
from __chromedriver_autoinstall__ import chrome_driver_install_path
from Web import Web
executable_path = chrome_driver_install_path()
div = Web(clientinfo={'executable_path':executable_path})
div.driver.get('https://google.com')
div.sleep(10)
div({'Target':'div'}).FindValues()