#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import socket
import struct

DEFAULT_BINKP_PORT = 24554

cmd_names = {
    'M_NUL'   : 0,
    'M_ADR'   : 1,
    'M_PWD'   : 2,
    'M_OK'    : 4,
    'M_FILE'  : 3,
    'M_EOB'   : 5,
    'M_GOT'   : 6,
    'M_ERR'   : 7,
    'M_BSY'   : 8,
    'M_GET'   : 9,
    'M_SKIP'  : 10,
    }

cmd_ids = dict((v,k) for k,v in cmd_names.items())

class ConnectionClosed(Exception):
    pass

class BinkpConnection (object):

    def __init__ (self, addr, timeout=None):
        try:
            self.addr, self.port = addr
        except ValueError:
            (self.addr,) = addr
            self.port = DEFAULT_BINKP_PORT

        self.timeout = timeout

    def connect(self):
        self.ip = socket.gethostbyname(self.addr)
        s = socket.socket()
        self.sock = s

        if self.timeout:
            s.settimeout(float(self.timeout))

        s.connect((self.addr, int(self.port)))

    def __read_bytes(self, want):
        bytes = self.sock.recv(want)

        while len(bytes) < want:
            more = self.sock.recv(want - len(bytes))
            if not more:
                raise ConnectionClosed()
            bytes += more

        return bytes

    def read_frame (self):
        bytes = self.__read_bytes(2)
        frame_header = struct.unpack('>H', bytes)[0]
        cmd_frame = frame_header & 0x8000
        data_len = frame_header & ~0x8000

        if cmd_frame:
            cmd_id = struct.unpack('b', self.__read_bytes(1))[0]
            cmd_id = cmd_ids[cmd_id]
            data = self.__read_bytes(data_len - 1)
        else:
            cmd_id = None
            data = self.__read_bytes(data_len)

        return {'command': bool(cmd_frame),
                'cmd_id': cmd_id,
                'data': data}

    def send_cmd_frame(self, cmd_id, data=b''):
        cmd_id = cmd_names[cmd_id]
        data = struct.pack('b', cmd_id) + data
        data_len = len(data)
        frame_header = data_len | 0x8000
        self.sock.sendall(struct.pack('>H', frame_header))
        self.sock.sendall(data)

    def send_data_frame(self, data):
        data_len = len(data)
        self.sock.sendall(struct.pack('>H', data_len))
        self.sock.sendall(data)

    def disconnect(self):
        self.sock.close()

if __name__ == '__main__':

    # пример тестовой сессии с локальным binkd демоном
    # b = BinkpConnection(sys.argv[1].split(':'), timeout=10)
    user = "127.0.0.1"
    # user = "192.168.1.104"

    b = BinkpConnection(user.split(':'), timeout=10)

    b.connect()

    """
    Отправляем станционную информацию M_NULL 0 команды, предпочитаемый формат:
        Generally, mailer SHOULD use only characters from the ASCII range [32...126]
        in the symbol strings for command arguments. In case when there is a necessity
        to use non-ASCII characters, mailer SHOULD use the [UTF8] format of the multioctet
        Universal Character Set [ISO10646]. Mailer SHOULD use non-ASCII characters only
        if the other side have indicated it's support by transmitting M_NUL "OPT UTF8"
        frame during the session setup stage. Otherwise, mailer SHOULD assume that the
        remote does not support non-ASCII characters and SHOULD NOT use them in command
        arguments.

        M_NUL "SYS system_name"
        M_NUL "ZYZ sysop's_name"
        M_NUL "LOC system_location"
        M_NUL "NDL system_capabilities"
        M_NUL "TIME remote_date_time"
        remote_date_time format is described in [RFC822]. Example of valid remote_date_time is Sun, 06 Nov 1994 08:49:37 GMT
        M_NUL "VER mailer_version protocol_version"
        note: binkp/1.0 mailers should send "binkp/1.0" string for protocol_version.
        M_NUL "TRF netmail_bytes arcmail_bytes"
        traffic prognosis (in bytes) for the netmail (netmail_bytes) and arcmail and files (arcmail_bytes), both are decimal ASCII strings
        M_NUL "OPT protocol options"
        here protocol options is a space separated list of binkp options and extensions supported by the mailer.
        M_NUL "PHN string"
        phone number, ip address or other network layer addressing ID
        M_NUL "OPM string"
        string is a message for the system operator that may require manual attention
    """
    b.send_cmd_frame('M_NUL', b'OPT UTF-8')
    b.send_cmd_frame('M_NUL', b'SYS test FNT system')
    b.send_cmd_frame('M_NUL', b'ZYZ Test Sysop')
    b.send_cmd_frame('M_NUL', b'LOC City, Country')
    b.send_cmd_frame('M_NUL', b'NDL 115200,TCP,BINKP')
    b.send_cmd_frame('M_NUL', b'VER FNT binkgw/0.0.0 binkp/1.0')


    """
    отправляем список наших адрессов, M_ADR 1:
        List of 4D/5D addresses (space separated).

        e.g. "2:5047/13@fidonet 2:5047/0@fidonet"
    """
    b.send_cmd_frame('M_ADR', b'2:464/900.777@fidonet')

    """
    Отправляем пароль сессии M_PWD 2
        Session password, case sensitive. After successful password authentication of the remote, originating side proceeds to the file transfer stage. This command MUST never be sent by the Answering side.

        e.g. "pAsSwOrD"
    """
    b.send_cmd_frame('M_PWD', b'1234567890')


    while True:
        frame = b.read_frame()
        print(frame)
        if frame['cmd_id'] == 'M_OK':
            # break
            pass
        elif frame['cmd_id'] == 'M_ERR':
            print("Incorrect password!")
            b.disconnect()
        elif frame['cmd_id'] == 'M_FILE':
            fname_data = str(frame['data']).split()
            recv_fname = fname_data[0][2:]
            recv_fsize = int(fname_data[1])
            recv_futime = int(fname_data[2])
            recv_fpos = int(fname_data[3][:-1])
            print("Получаем файл: '{0}' размер {1} юникс время: {2} с позиции {3}".format(
                recv_fname, recv_fsize, recv_futime, recv_fpos)
            )

        elif not frame['cmd_id'] and frame['command'] is False:

            if not os.path.isfile(recv_fname):
                recv_fdescr = open(recv_fname, mode='wb')
                recv_fdescr.close()

            if os.path.getsize(recv_fname) > recv_fsize:
                print("Error: Размер файла за пределами EOF")
                b.send_cmd_frame('M_ERR', b'Error: file size beyond EOF')
            elif os.path.getsize(recv_fname) == recv_fsize:
                print("Файл: {0} получен".format(recv_fname))
                b.send_cmd_frame('M_GOT', str.encode('{0} {1} {2}'.format(recv_fname,
                                                                      recv_fsize,
                                                                      recv_futime
                                                                      )))
                recv_fdescr = open(recv_fname, mode='a+b')
                os.utime(recv_fname, recv_futime)
                recv_fdescr.close()
            else:
                recv_fdescr = open(recv_fname, mode='a+b')
                # s_buf = str(frame['data'])[2:-1]
                s = recv_fdescr.write(frame['data'])
                print("Записали в файл: {0} {1} байт".format(recv_fname, s))
                recv_fdescr.close()



    b.send_cmd_frame('M_EOB')
    # b.read_frame()
    b.disconnect()

    """
    Генерируем тестовый пакет:
    bash-3.2$ ./crashwrite FROMNAME "test" FROMADDR "2:464/900.1" TONAME "TEST" TOADDR "2:464/900.777" SUBJECT "test" PKTFROMADDR "2:464/900.1" PKTTOADDR "2:464/900.777" DIR "../out/01d00384.pnt/"
    Writing...
     From: test                                 (2:464/900.1)
       To: TEST                                 (2:464/900.777)
     Subj: test
     Date: 25 Dec 14  22:34:33
    """