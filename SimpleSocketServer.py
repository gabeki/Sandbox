#!/usr/local/bin/python

import socket

class SimpleSocketServer:

    def __init__(self, server_address, RequestHandlerClass):
        self.server_address = server_address
        self.RequestHandlerClass = RequestHandlerClass

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

        self.server_activate()

    def server_activate(self):
        """ Listen to only 1 clients """
        self.socket.listen(1)

    def serve_forever(self):
        while True:
            client, address = self.socket.accept()
            self.handle_request(client, address)

    def handle_request(self, client, client_address):
        self.RequestHandlerClass(client, client_address)



class EchoRequestHandler:
    def __init__(self, client, client_address):
        self.client = client
        self.client_address = client_address
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        pass

    def handle(self):
        data = self.client.recv(1024)
        if data: 
            self.client.send(data) 
            print self.client_address, " >>> ", data
        self.client.close()

    def finish(self):
        pass


if __name__ == '__main__':
    server_address = ('127.0.0.1', 8000)
    echo = SimpleSocketServer(server_address, EchoRequestHandler)
    sa = echo.socket.getsockname()
    print "Serving on", sa[0], "port", sa[1], "..."
    echo.serve_forever()
