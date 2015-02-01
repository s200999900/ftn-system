#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'svelic'
__version__ = '0.0.0'

"""
file: binkp2
project: sclient_test
date: 1/14/15

Description:


"""

import sys
import os

from binkp import BinkpConnection, DEFAULT_BINKP_PORT, cmd_ids, cmd_names, ConnectionClosed


class BinkpSession():
    """

    """
    def __init__(self, addr='127.0.0.1', port='24554', timeout=None):

        self.binkpconn = BinkpConnection(list(addr, port), timeout)

    def connect(self):
        """

        """
        self.binkpconn.connect(self)

    def disconnect(self):
        """

        """
        self.binkpconn.disconnect(self)





def main( ):
    """
    Main entry point for the script
    """
    b = BinkpSession(addr='127.0.0.1', port='24554')
    b.connect()


if __name__ == "__main__":
    sys.exit( main() )