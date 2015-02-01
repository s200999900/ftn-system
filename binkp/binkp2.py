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

import configparser

from binkp import BinkpConnection, DEFAULT_BINKP_PORT, cmd_ids, cmd_names, ConnectionClosed


class BinkpSession(BinkpConnection):
    """
    Класс который обслуживает binkp сессию
    использует методы класса BinkpConnection
    """
    def __init__(self, addr=None, port=None, timeout=None, password=None):
        self.addr = addr
        self.port = port
        self.timeout = timeout
        self.session_password = password

        self.system_params = {}
        self.config_group_name = 'binkpgw'

        super().__init__(self.addr, self.port, self.timeout)

    def read_config(self):

        config_file = os.path.join(os.getcwd(), 'binkp', 'config.ini')
        print('Используем конфиг файл: {}'.format(config_file))

        # Если файла конфигурации нет, то создадим дефолтный
        if not os.path.isfile(config_file):
            config = configparser.ConfigParser()
            config[self.config_group_name] = { 'System Name' : 'Test FNT system',
                                              'SysOp Name' : 'Test Sysop',
                                              'Location' : 'City, Country',
                                              'Nodelist Flags' : '115200,TCP,BINKP',
                                              'FTN Address' : '2:464/900.777@fidonet'}
            with open(config_file, 'w') as c_file:
                config.write(c_file)
        elif os.access(config_file, os.R_OK):
            config = configparser.ConfigParser()
            config.read(config_file)

            if self.config_group_name in config:
                self.system_params['System_Name'] = config[self.config_group_name]['System Name']
                self.system_params['SysOp_Name'] = config[self.config_group_name]['SysOp Name']
                self.system_params['Location'] = config[self.config_group_name]['Location']
                self.system_params['Nodelist_Flags'] = config[self.config_group_name]['Nodelist Flags']
                self.system_params['FTN_Address'] = config[self.config_group_name]['FTN Address']
                print('Прочитали из конфигурации:')
                for x, v in self.system_params.items():
                    print('{} = {}'.format(x, v))

    def session_connect(self):
        """
        метод отвечает за подключение к удаленной ноде по протоколу binkp
        принимет параметры
        адресс, порт и пароль для сессии
        использует методы класса для обработки типов пакетов протокола
        ...
        """
        # читаем конфиг клиента
        self.read_config()
        self.connect()

        # Рукопожатие

        if self.codepage:
            self.send_cmd_frame('M_NUL', 'OPT {}'.format(self.codepage.upper()))

        self.send_cmd_frame('M_NUL', 'SYS {}'.format(self.system_params['System_Name']))
        self.send_cmd_frame('M_NUL', 'ZYZ {}'.format(self.system_params['SysOp_Name']))
        self.send_cmd_frame('M_NUL', 'LOC {}'.format(self.system_params['Location']))
        self.send_cmd_frame('M_NUL', 'NDL {}'.format(self.system_params['Nodelist_Flags']))
        self.send_cmd_frame('M_NUL', 'VER FNT binkgw/{} binkp/1.0'.format(__version__))

        self.send_cmd_frame('M_ADR', '{}'.format(self.system_params['FTN_Address']))

        frame = self.read_frame()
        print(frame)


    def session_disconnect(self):
        """
        Метод завершающий binkp сессию
        """
        self.disconnect()



def main( ):
    """
    Main entry point for the script
    """
    b = BinkpSession(addr='127.0.0.1', port='24554', password='1234567890')
    b.session_connect()


    # b.session_disconnect()

    return 0

if __name__ == "__main__":
    sys.exit(main())