#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Project: ftn-system
File name: main
Short description: ftn system kernel
Description: Главный файл ядра системы


"""
__author__ = 'svelic'

import os
from os.path import join

from springpython.config import XMLConfig
from springpython.context import ApplicationContext


#TODO: Написать тесты
contextFile = u'context.xml'
currDir = os.getcwd()
contextFile = join(currDir, contextFile)
# print(contextFile)


class Kernel:
    """
    Main kernel class

    """
    #TODO: Написать тесты
    def __init__(self):
        """


        """
        pass

    def run(self):
        """


        """
        pass


def main():
    """
    Main function

    """
    #TODO: Написать тесты
    context = ApplicationContext(XMLConfig(contextFile))
    objKernel = context.get_object("Kernel")
    objKernel.run()


if __name__ == '__main__':
    main()
