import ctypes
import errno
import numpy as np
import socket
import subprocess
import time

host = "127.0.0.1"
port = 8000
BUFF  = 1024
wait_time = 5

# define pointer class
class _pointer(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_long),
        ('y', ctypes.c_long),
    ]

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
                break
            except socket.error as exc:
                print("Caught exception socket.error : %s" % exc)
                #for reconnection error not to continue connecting
                if self.error["ERROR_10056"] or self.error["ERROR_10057"]:
                    break
                continue

    def observe(self):
        # initialize pointer
        before_point = _pointer()
        after_point = _pointer()

        weight = -1
        state_on = 0
        time_weight = [1, 1, 1, 1, 1]#待ち時間

        while True:
            before_point.x = after_point.x
            before_point.y = after_point.y
            ctypes.windll.user32.GetCursorPos(ctypes.byref(after_point))
            print(weight)

            if before_point.x == after_point.x and before_point.y == after_point.y:
                weight = weight - 1 if weight >= 0 and state_on else 0
            elif weight != 3:
                weight += 1
                if weight == 1 and state_on != 1:
                    state_on = 1
                    try:
                        print("turn on")
                        self.client.send(str(state_on).encode("utf-8"))
                        response = self.client.recv(BUFF)
                        print(response)
                    except socket.error as exc:
                        print("Caught exception socket.error : %s" % exc)
                        if self.error["ERROR_10053"]:
                            time.sleep(wait_time)
                            try:
                                self.client.send(str(state_on).encode("utf-8"))
                                response = self.client.recv(BUFF)
                                print(response)
                            except socket.error:
                                break
                        if self.error["ERROR_10054"]:
                            break

            if weight == -1:
                state_on = 0
                try:
                    print("turn off")
                    self.client.send(str(state_on).encode("utf-8"))
                    response = self.client.recv(BUFF)
                    print(response)
                except socket.error as exc:
                    print("Caught exception socket.error : %s" % exc)
                    if self.error["ERROR_10053"]:
                        time.sleep(wait_time)
                        try:
                            self.client.send(str(state_on).encode("utf-8"))
                            response = self.client.recv(BUFF)
                            print(response)
                        except socket.error:
                            break
                    if self.error["ERROR_10054"]:
                        break

            time.sleep(time_weight[weight + 1])

    def repeat(self):
        # remedy to error
        while True:
            self.__init__(self.host, self.port)
            self.observe()

if __name__ == "__main__":
    client(host, port).repeat()
