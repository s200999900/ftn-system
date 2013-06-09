#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Project: ftn-system
File name: main_test
Short description:
Description:

'''
__author__ = 'svelic'

import unittest

class TestCase(unittest.TestCase):
    def test_starting_out(self):
        self.assertEqual(1, 1)

def main():
    unittest.main()

if __name__ == "__main__":
    main()