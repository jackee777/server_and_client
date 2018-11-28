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
        while True:
            state_on = np.random.randint(100)

            try:
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

            time.sleep(wait_time)

    def repeat(self):
        # remedy to error
        while True:
            self.__init__(self.host, self.port)
            self.observe()

if __name__ == "__main__":
    client(host, port).repeat()
