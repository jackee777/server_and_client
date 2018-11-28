# -*- coding:utf-8 -*-
import copy
import datetime
import json
import socket
import sys
import threading
from multiprocessing import Value

host = "127.0.0.1"
port = 8000
BUFF = 1024
timeout_time = 100
write_time = 3
finish_time = 30 #* 60 #seconds
values = []
data_path = "original_data/"

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)


    def listen(self):
        while True:
            try:
                client, address = self.sock.accept()
                self.clients.append(client)
                #client.settimeout(timeout_time)
                threading.Thread(target = self.listenToClient,args = (client,address)).start()
            except:
                break

    def listenToClient(self, client, address):
        global values
        while True:
            try:
                data = client.recv(BUFF)
                if data:
                    now_time = datetime.datetime.now()
                    value = {
                            "time":str(now_time),
                            "ip":address[0],
                            "port":address[1],
                            "value":data.decode("utf-8")}
                    values.append(value)
                    client.send(str("server ok").encode("utf-8"))
                else:
                    print("raise error")
                    raise error('Client disconnected')

            except:
                print("close client")
                client.close()
                return False

    def finish(self):
        for client in self.clients:
            client.close()
        self.sock.close()


Server = ThreadedServer(host, port)

def timer():
    global values
    global Server
    now_time = datetime.datetime.now()
    prev_time = copy.copy(now_time)
    submit_time = copy.copy(now_time)
    values = []
    while True:
        now_time = datetime.datetime.now()
        td = now_time - prev_time
        submit_td = now_time - submit_time
        if td.seconds == write_time:
            if len(values) != 0:
                print(values)
                submit_time = copy.copy(now_time)
                with open(data_path+"data.txt", "a") as f:
                    for value in values:
                        json.dump(value, f, sort_keys=True)
                        f.write("\n")
            values = []
            prev_time = copy.copy(now_time)

        if submit_td.seconds > finish_time:
            print("finish data corecction")
            for thread in threading.enumerate():
                try:
                    thread.stop()
                except:
                    pass
            Server.finish()
            break

if __name__ == "__main__":
    threading.Thread(target = timer).start()
    Server.listen()
