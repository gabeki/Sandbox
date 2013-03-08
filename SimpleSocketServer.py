#!/usr/local/bin/python

import os
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



class TreeWalkingRequestHandler:
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
            data = data.split('\r\n')[0]
            words = data.split()
            if len(words) == 3:
                command, path, version = words
            elif len(words) == 2:
                command, path = words
            else:
                self.handle_error_404()
                return;

            if command != 'GET':
                self.handle_error_501()
            else:
                self.do_get(path)

        self.client.close()

    def do_get(self, path):
        self.client.send("HTTP/1.1 200 OK\r\n");
        self.client.send("\r\n\r\n");

        base_path = "." + os.path.normpath(path)

        self.client.send("<html>");
        if path != "/":
            self.client.send("<a href=\"/" + base_path + "/..\">..</a><br/>");

        for file in os.listdir(base_path):
            current_file = os.path.join(base_path, file) 
            if os.path.isdir(current_file):
                self.client.send("<a href=\"/" + current_file + "\">" + file + "</a><br/>");
            else:
                self.client.send(file + "<br/>");

        self.client.send("</html>");

    def handle_error_404(self):
        self.client.send("HTTP/1.1 404 Bad Request\r\n");

    def handle_error_501(self):
        self.client.send("HTTP/1.1 501 Not Implemented\r\n");

    def finish(self):
        pass


if __name__ == '__main__':
    server_address = ('127.0.0.1', 8000)
    echo = SimpleSocketServer(server_address, TreeWalkingRequestHandler)
    sa = echo.socket.getsockname()
    print "Serving on", sa[0], "port", sa[1], "..."
    echo.serve_forever()
