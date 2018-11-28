# -*- coding:utf-8 -*-
import ctypes
import errno
import keyboard
import numpy as np
import socket
import subprocess
import time

host = "127.0.0.1"
port = 8000
BUFF  = 1024
sleep_length = 0.5
timeout_time = 1

class client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.error = dict({ "ERROR_10053":"exc.errno == errno.WSAECONNABORTED",
                            "ERROR_10054":"exc.errno == errno.WSAECONNRESET",
                            "ERROR_10056":"exc.errno == errno.WSAEISCONN",
                            "ERROR_10057":"exc.errno == errno.WSAENOTCONN" })
        self.try_connection()

    def try_connection(self):
        while True:
            try:
                self.client.connect((self.host, self.port))
                #self.client.settimeout(timeout_time)
                break
            except socket.error as exc:
                print("Caught exception socket.error : %s" % exc)
                #for reconnection error not to continue connecting
                if self.error["ERROR_10056"] or self.error["ERROR_10057"]:
                    break
                continue

    def observe(self):
        state_on = None
        while True:
            state_on = np.random.randint(0, 100)
            try:
                self.client.send(str(state_on).encode("utf-8"))
                response = self.client.recv(BUFF)
                print(response)
            except socket.error as exc:
                print("Caught exception socket.error : %s" % exc)
                if self.error["ERROR_10053"]:
                    time.sleep(sleep_length)
                    try:
                        self.client.send(str(state_on).encode("utf-8"))
                        response = self.client.recv(BUFF)
                        print(response)
                    except socket.error:
                        break
                if self.error["ERROR_10054"]:
                    break
            time.sleep(sleep_length)

    def repeat(self):
        # remedy to error
        #本来はエラー対策だけでなく、サーバーが落ちた時の再アクセス用にループさせたかったのだが無理そう
        #(サーバーが落ちてもsocketが残るため、プログラムを落とさないと、通信しなおせない)
        #socketのclose, shutdown, timeoutなどは効果なしだった。
        #クライアントの再起動をせずに済む案あれば。。。
        while True:
            self.__init__(self.host, self.port)
            self.observe()

if __name__ == "__main__":
    client(host, port).repeat()
