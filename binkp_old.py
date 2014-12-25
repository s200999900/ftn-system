#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'svelic'

import sys

import bitstring
import socket

class Binkp_client(object):
    def __init__(self, sock):
        self.sock = sock
        self.frame_header_type = None # {'0': 'DATA', '1': 'CMD'}
        self.frame_commands = {
                                '0': 'M_NUL',
                                '1': 'M_ADR'
                            }
        self.frame_command = None
        self.frame_header_sizes = None
        self.socket_header_bufer = None
        self.socket_command_buffer = None
        self.socket_frame_data_buffer = None
        self.header_buffer = None
        self.frame_data_size = None

    def recv_header(self):
        """
        Читаем из сокета заголовок пакета
        :param sock: подключенный сокет
        :return: вернуть кортеж с полученным заголовком
            в формате: (block_type, HI, LO)
        """

        header_size = 2
        # формируем шаблон битового потока
        header_frame_template = ['bin:1', 'bin:7', 'bin:8']

        # Читаем из сокета заголовок
        self.socket_header_bufer = self.sock.recv(header_size)
        # print("Прочитали из сокета: ", len(self.socket_header_bufer), "байт")
        if self.socket_header_bufer:
            # формируем битовый поток
            bit_stream = bitstring.BitStream(self.socket_header_bufer)
            # читаем из битового потока согласно шаблону
            self.header_buffer = tuple(bit_stream.readlist(header_frame_template))
            print("Прочитали заголовок блока: ", self.header_buffer)
            return self.header_buffer
        else:
            return None

    def f_data_size(self):
        """
        Считаем размер блока данных
        Пример:
            >>> a = '00000000' + '00010100'
            >>> len(a)
            16
            >>> b = '0b' + a
            >>> len(b)
            18
            >>> c = bitstring.BitArray(b)
            >>> c.uint
            20
            >>> c.uintbe
            20
            :param LO: значение байта LO из заголовка для командных фреймов(8бит)
            :param HI: значение байта HI из заголовка для командных фреймов(7бит) - дополняем в начале 0 ! до длины в 8 бит !
            :return:
                возвращаем кортеж
                пример: (20, 20, )
                в формате: (uint, uintbe(Big-endian), )
        """

        HI = self.header_buffer[1]
        LO = self.header_buffer[2]
        if len(HI) != 8:
            HI = '0' + HI
        frame_data_size = HI + LO
        bit_array = bitstring.BitArray(bin=frame_data_size)
        self.frame_data_size = bit_array.uintbe
        if not self.frame_data_size:
            return None

        if self.frame_header_type == 1:
            self.frame_data_size -= 1
            print("Размер данных пакета с командой:", self.frame_data_size, "bytes")
            return self.frame_data_size
        else:
            print("Размер данных пакета:", self.frame_data_size, "bytes")
            return self.frame_data_size


    def f_type(self):
        """
        функция которая определяет тип блока: блок данных или блок комманд
        и вызывает соответсвующие фукнции обработки блоков
        """

        block_type = self.header_buffer[0]
        if block_type == '0':
            # Обрабатываем пакет как блок данных
            print("Получили блок данных")
            self.frame_header_type = 0
            return self.frame_header_type
        elif block_type == '1':
            # Обрабатываем пакет как блок комманд
            print("Получили блок с командой")
            self.frame_header_type = 1
            return self.frame_header_type
        else:
            # Получили неизвестный или поврежденный блок
            print("Получили неизвестный или поврежденный блок")
            return None

    def recv_frame_cmd(self):
        """
        Читаем из сокета команду командного фрейма и возвращаем ее
        Если команда неизвестна возвращаем None
        """
        # формируем шаблон битового потока
        header_frame_template = ['bin:8']

        # Читаем из сокета заголовок
        self.socket_command_buffer = self.sock.recv(1)
        # print("Прочитали из сокета: ", len(self.socket_command_buffer), "байт")
        if self.socket_command_buffer:
            self.frame_command = str(bitstring.BitArray(self.socket_command_buffer).uintbe)
            # print("Команда до разбора: ", self.frame_command)
        else:
            print("Команда пустая!")
            return None

        if self.frame_command in self.frame_commands.keys():
            print("Прочитали команду:", self.frame_commands[self.frame_command], self.frame_command)
            return (self.frame_commands[self.frame_command], self.frame_command)
        else:
            print("Получили неизвестную команду!")
            return None


    def recv_frame_data(self):
        """
        Читаем данные фрейма. Используем размер данных и сокета
        :param sock: сокет
        :param data_size: размер блока данных
        :return: блок данных
        """
        self.socket_frame_data_buffer = self.sock.recv(self.frame_data_size)
        print("Прочитано из сокета:", len(self.socket_frame_data_buffer), "байт")

        if self.socket_frame_data_buffer:
            print("Прочитали блока данных: ", self.socket_frame_data_buffer)
            return self.socket_frame_data_buffer
        else:
            print("Нет данных в блоке данных")
            return None




def main():
    """
    Run binkd server: sbin/binkd -s -v -m -r etc/binkd.config
    :return 0 в случае успеха
    :return >0 в случае  проблем
    """

    # server = "192.168.1.104"
    server = "127.0.0.1"
    port = 24554
    srv_port = (server, port)
    sock = socket.socket()
    sock.connect(srv_port)

    client = Binkp_client(sock=sock)

    data = client.recv_header()
    print(data)
    frame_size = client.f_data_size()
    print(frame_size)
    frame_type = client.f_type()
    print(frame_type)
    if frame_type == 0:
        pass
    else:
        frame_cmd = client.recv_frame_cmd()
        print(frame_cmd)
    frame_data = client.recv_frame_data()
    if frame_data:
        print(data)
    else:
        print("No data in frame!")


    sock.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())