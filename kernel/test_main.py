#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Project: ftn-system
File name: main_test
Short description:
Description:

'''
__author__ = 'svelic'

import os
from os.path import join

import unittest
from springpython.config import XMLConfig
from springpython.context import ApplicationContext

from main import Kernel

contextFile = u'context.xml'
currDir = os.getcwd()
contextFile = join(currDir, contextFile)

class TestCase(unittest.TestCase):
    def test_starting_out( self ):
        self.assertEqual(1, 1)

    # def setUp( self ):
    #     self.main = Kernel

    def test_main_has_Kernel_object( self ):
        context = ApplicationContext(XMLConfig(contextFile))
        self.assertTrue('Kernel' in context.objects)


def main( ):
    unittest.main()


if __name__ == "__main__":
    main()