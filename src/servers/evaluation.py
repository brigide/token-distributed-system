import socket
import time
from src.helpers.helpers import Helpers, ServerHelper

class Evaluation:
    """
        Evaluation server class
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = ""


    def createSocket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except OSError as message:
            print('socket creation error: ' + str(message))

    def bindSocket(self):
        """
            binding our created socket to the ip and port 
        """
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(100)

            print('server listening on port: ' + str(self.port))

        #auto reconnection every 3 seconds in case of errors
        except OSError as message:
            print('socket binding error: ' + str(message))
            print('retrying in 3 seconds...\n')
            time.sleep(3)
            self.bindSocket()


    def acceptConnection(self):
        """
            now it accepts connections 
        """
        conn, addr = self.socket.accept()
        print('\n' + str(addr) + ' connected')
        return conn, addr

    def run(self, conn, addr):
        """
            this function handles every client from any thread
            and return it's response
        """
        host = 'localhost'
        port = 50003
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        try:
            while True:
                request = ServerHelper.waitMessage(conn) #recieves request from client
                if request == '/end':
                    ServerHelper.sendRequest(s, request)
                    break

                code, n = Helpers.splitRequest(request)

                isValid = Helpers.evaluate(code, n)

                if not isValid:
                    ServerHelper.sendMessage(conn, 'error: invalid parameter')
                    ServerHelper.closeConnection(conn, addr)
                    break

                response = ServerHelper.sendRequest(s, request)

                ServerHelper.sendMessage(conn, 'token: ' + response)

            ServerHelper.closeConnection(conn, addr)


        except Exception as error:
            ServerHelper.closeConnection(conn, addr)

    def closeServer(self):
        #closes server's socket
        self.socket.close()