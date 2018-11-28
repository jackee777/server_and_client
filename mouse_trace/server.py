import socket
import threading

host = "127.0.0.1"
port = 8000
BUFF = 1024

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

    def listen(self):
        while True:
            client, address = self.sock.accept()
            #client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        while True:
            try:
                data = client.recv(BUFF)
                if data:
                    # Set the response to echo back the recieved data
                    response = data
                    print(address)
                    print(data)
                    client.send(str("server ok").encode("utf-8"))
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False



if __name__ == "__main__":
    ThreadedServer(host, port).listen()
