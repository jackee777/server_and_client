# -*- coding:utf-8 -*-
import ctypes
import datetime
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
finish_time = 10 #* 60 #seconds

class client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.submit_time = datetime.datetime.now()
        self.submit_td = datetime.datetime.now() - self.submit_time
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.error = dict({ "ERROR_10053":"exc.errno == errno.WSAECONNABORTED",
                            "ERROR_10054":"exc.errno == errno.WSAECONNRESET",
                            "ERROR_10056":"exc.errno == errno.WSAEISCONN",
                            "ERROR_10057":"exc.errno == errno.WSAENOTCONN" })
        self.try_connection()

    def try_connection(self):
        while self.submit_td.seconds <= finish_time:
            try:
                self.client.connect((self.host, self.port))
                #self.client.settimeout(timeout_time)
                self.submit_td = datetime.datetime.now() - self.submit_time
                break
            except socket.error as exc:
                print("Caught exception socket.error : %s" % exc)
                #for reconnection error not to continue connecting
                if self.error["ERROR_10056"] or self.error["ERROR_10057"]:
                    break
                continue


    def observe(self):
        state_on = None
        while self.submit_td.seconds <= finish_time:
            if keyboard.is_pressed("shift+w"):
                state_on = "good"
            elif keyboard.is_pressed("shift+s"):
                state_on = "bad"
            elif keyboard.is_pressed("shift+a"):
                state_on = "normal"
            elif keyboard.is_pressed("shift+d"):
                state_on = "normal"
            elif keyboard.is_pressed("shift+z"):
                state_on = "reject"
            #state_on = np.random.randint(0, 100)
            if state_on in ["good", "bad", "normal", "reject"]:
                self.submit_time = datetime.datetime.now()
                self.submit_td = datetime.datetime.now() - self.submit_time
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
                state_on = None
                time.sleep(sleep_length)
            self.submit_td = datetime.datetime.now() - self.submit_time

    def repeat(self):
        # remedy to error
        #本来はエラー対策だけでなく、サーバーが落ちた時の再アクセス用にループさせたかったのだが無理そう
        #(サーバーが落ちてもsocketが残るため、プログラムを落とさないと、通信しなおせない)
        #socketのclose, shutdown, timeoutなどは効果なしだった。
        #クライアントの再起動をせずに済む案あれば。。。
        while self.submit_td.seconds <= finish_time:
            self.__init__(self.host, self.port)
            self.observe()
        self.client.close()

if __name__ == "__main__":
    client(host, port).repeat()
