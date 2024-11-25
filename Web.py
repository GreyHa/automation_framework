# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from supportmodule.Web import module_class as Web_module

class Web(Web_module):
    def __init__(self, clientinfo):
        self.clientinfo = clientinfo