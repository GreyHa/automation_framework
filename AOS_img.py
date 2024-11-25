# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from supportmodule.AOS import module_class as AOS_module
from supportmodule.img import module_class as img_module

class AOS(AOS_module, img_module):
    def __init__(self, clientinfo):
        self.clientinfo = clientinfo