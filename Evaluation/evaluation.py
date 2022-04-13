import socket
import time
from Evaluation.helpers import Helpers

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
        try:
            request = self.waitMessage(conn, 'waiting for data...') #recieves request from client
            code, n = Helpers.splitRequest(request)

            isValid = Helpers.evaluate(code, n)

            if not isValid:
                self.sendMessage(conn, 'error: invalid parameter')
                self.closeConnection(conn, addr)
                return

            print('passei caralho')

        except Exception as error:
            print(error)


    def waitMessage(self, conn, prefix=''):
        """
            function to handle and wait message from the client
        """
        conn.sendall(prefix.encode())
        message = conn.recv(1024).decode()   
        return message

    def sendMessage(self, conn, message):
        """
            function to handle and send messages to the client
        """
        message += '\n'
        conn.sendall(message.encode())


    def closeConnection(self, conn, addr):
        """
            function to close client connection
        """
        conn.close()
        print('\n' + str(addr) + ' disconnected')

    def closeServer(self):
        #closes server's socket
        self.socket.close()