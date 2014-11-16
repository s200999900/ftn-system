#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Попытка реализовать binkp протокол на python

"""

__author__ = 'svelic'

import socket
import bitstring



def data_frame_size(LO, HI):
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
        пример: ['00000000', '00010100', 20, 20, 5120, 5120]
        в формате: ['LO', 'HI', uint, uintbe(Big-endian), uintle(Little-endian), uintne(Native-endian)]
    """
    if len(HI) != 8:
        HI = '0' + HI
    a = HI + LO
    b = '0b' + a
    c = bitstring.BitArray(b)
    d = [HI, LO, c.uint, c.uintbe, c.uintle, c.uintne]
    print("Размер данных пакета:", d)
    return d


def main():
    """

    """

    # server = "192.168.1.104"
    server = "127.0.0.1"
    port = 24554
    srv_port = (server,port)
    sock = socket.socket()
    sock.connect(srv_port)



    # Читаем из сокета
    data = sock.recv(3)
    # формируем битовый поток
    a = bitstring.BitStream(data)

    # формируем шаблон битового потока
    start_frame = ['bin:1','bin:7', 'bin:8', 'bin:8']
    # читаем из битового потока согласно шаблону
    data = a.readlist(start_frame)
    print("Прочитали следующий заголовок: ", data)

    # Вычисляем размер блока данных
    """
        >>> a = '00000000' + '00010001'
        >>> len(b)
        17
        >>> len(a)
        16
        >>> b = '0b' + a
        >>> b
        '0b0000000000010001'
        >>> len(b)
        18
        >>> c = bitstring.BitArray(b)
        >>> c
        BitArray('0x0011')
        >>> c.bin
        '0000000000010001'
        >>> c.hex
        '0011'
        >>> c.uint
        17
        >>> c.uintbe
        17
        >>> c.uintle
        4352
    """
    data_size = data_frame_size(HI=data[1], LO=data[2])[3] - 1

    # Читаем XXX байт из потока согласно вычисленному размеру блока данных
    # data_size = 17 - 1  # 1 - размер поля для команды (1-байт)
    data=sock.recv(data_size)
    print("Прочитали следующее из блока данных: ", data)


    # Читаем следующий блок
    # Читаем из сокета
    data = sock.recv(3)
    # формируем битовый поток
    a = bitstring.BitStream(data)

    # формируем шаблон битового потока
    start_frame = ['bin:1','bin:7', 'bin:8', 'bin:8']
    # читаем из битового потока согласно шаблону
    data = a.readlist(start_frame)
    print("Прочитали следующий заголовок: ", data)

    # Вычисляем размер блока данных
    """
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
    """
    data_size = data_frame_size(HI=data[1], LO=data[2])[3] - 1
    # Читаем XXX байт из потока согласно вычисленному размеру блока данных
    # data_size = 20 - 1  # 1 - размер поля для команды (1-байт)
    data=sock.recv(data_size)
    print("Прочитали следующее из блока данных: ", data)


    # Читаем следующий блок
    # Читаем из сокета
    data = sock.recv(3)
    # формируем битовый поток
    a = bitstring.BitStream(data)

    # формируем шаблон битового потока
    start_frame = ['bin:1','bin:7', 'bin:8', 'bin:8']
    # читаем из битового потока согласно шаблону
    data = a.readlist(start_frame)
    print("Прочитали следующий заголовок: ", data)

    # Вычисляем размер блока данных
    """
        >>> a = '00000000' + '00010010'
        >>> len(a)
        16
        >>> b = '0b' + a
        >>> len(b)
        18
        >>> c = bitstring.BitArray(b)
        >>> c.uint
        18
        >>> c.uintbe
        18
    """
    data_size = data_frame_size(HI=data[1], LO=data[2])[3] - 1
    # Читаем XXX байт из потока согласно вычисленному размеру блока данных
    # data_size = 18 - 1  # 1 - размер поля для команды (1-байт)
    data=sock.recv(data_size)
    print("Прочитали следующее из блока данных: ", data)


    # Читаем следующий блок
    # Читаем из сокета
    data = sock.recv(3)
    # формируем битовый поток
    a = bitstring.BitStream(data)

    # формируем шаблон битового потока
    start_frame = ['bin:1','bin:7', 'bin:8', 'bin:8']
    # читаем из битового потока согласно шаблону
    data = a.readlist(start_frame)
    print("Прочитали следующий заголовок: ", data)

    # Вычисляем размер блока данных
    """
        >>> a = '00000000' + '00010101'
        >>> len(a)
        16
        >>> b = '0b' + a
        >>> c = bitstring.BitArray(b)
        >>> c.uint
        21
        >>> c.uintbe
        21
    """

    data_size = data_frame_size(HI=data[1], LO=data[2])[3] - 1
    # Читаем XXX байт из потока согласно вычисленному размеру блока данных
    # data_size = 21 - 1  # 1 - размер поля для команды (1-байт)
    data=sock.recv(data_size)
    print("Прочитали следующее из блока данных: ", data)

    # Читаем следующий блок
    # Читаем из сокета
    data = sock.recv(3)
    # формируем битовый поток
    a = bitstring.BitStream(data)

    # формируем шаблон битового потока
    start_frame = ['bin:1','bin:7', 'bin:8', 'bin:8']
    # читаем из битового потока согласно шаблону
    data = a.readlist(start_frame)
    print("Прочитали следующий заголовок: ", data)

    # Вычисляем размер блока данных
    """
        >>> a = '00000000' + '00100101'
        >>> len(a)
        16
        >>> b = '0b' + a
        >>> len(b)
        18
        >>> c = bitstring.BitArray(b)
        >>> c.uint
        37
        >>> c.uintbe
        37
    """
    data_size = data_frame_size(HI=data[1], LO=data[2])[3] - 1

    # Читаем XXX байт из потока согласно вычисленному размеру блока данных
    # data_size = 37 - 1  # 1 - размер поля для команды (1-байт)
    data=sock.recv(data_size)
    print("Прочитали следующее из блока данных: ", data)

    # Читаем следующий блок
    # Читаем из сокета
    data = sock.recv(3)
    # формируем битовый поток
    a = bitstring.BitStream(data)

    # формируем шаблон битового потока
    start_frame = ['bin:1','bin:7', 'bin:8', 'bin:8']
    # читаем из битового потока согласно шаблону
    data = a.readlist(start_frame)
    print("Прочитали следующий заголовок: ", data)

    # Вычисляем размер блока данных
    """
        >>> a = '00000000' + '00100001'
        >>> len(a)
        16
        >>> b = '0b' + a
        >>> len(b)
        18
        >>> c = bitstring.BitArray(b)
        >>> c.uint
        33
        >>> c.uintbe
        33
    """
    data_size = data_frame_size(HI=data[1], LO=data[2])[3] - 1
    # Читаем XXX байт из потока согласно вычисленному размеру блока данных
    # data_size = 33 - 1  # 1 - размер поля для команды (1-байт)
    data=sock.recv(data_size)
    print("Прочитали следующее из блока данных: ", data)

    # Читаем следующий блок
    # Читаем из сокета
    data = sock.recv(3)
    # формируем битовый поток
    a = bitstring.BitStream(data)

    # формируем шаблон битового потока
    start_frame = ['bin:1','bin:7', 'bin:8', 'bin:8']
    # читаем из битового потока согласно шаблону
    data = a.readlist(start_frame)
    print("Прочитали следующий заголовок: ", data)

    # Вычисляем размер блока данных
    """
        >>> a = '00000000' + '00010101'
        >>> len(a)
        16
        >>> b = '0b' + a
        >>> len(b)
        18
        >>> c = bitstring.BitArray(b)
        >>> c.uint
        21
        >>> c.uintbe
        21
    """
    data_size = data_frame_size(HI=data[1], LO=data[2])[3] - 1
    # Читаем XXX байт из потока согласно вычисленному размеру блока данных
    # data_size = 33 - 1  # 1 - размер поля для команды (1-байт)
    data=sock.recv(data_size)
    print("Прочитали следующее из блока данных: ", data)


    sock.close()



if __name__ == "__main__":
    main()