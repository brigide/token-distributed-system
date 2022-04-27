import socket
import time
from src.helpers.helpers import Helpers, ServerHelper

class TokenGenerator:
    """
        Evaluation server class
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = ""
        self.primes = {}
        with open('primes.txt', 'r') as file:
            content = file.readlines()
            for i in range(len(content)):
                self.primes[int(content[i].strip('\n'))] = i


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
            while True:
                message = ServerHelper.waitMessage(conn) #recieves request from client
                if message == '/end':
                    break

                code, n = Helpers.splitRequest(message)

                ServerHelper.sendMessage(conn, str(Helpers.generateToken(code, n)))
                
            ServerHelper.closeConnection(conn, addr)

        except Exception as error:
            ServerHelper.closeConnection(conn, addr)

    def closeServer(self):
        #closes server's socket
        self.socket.close()