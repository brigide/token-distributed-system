import socket
import sympy

class Helpers:
    @staticmethod
    def evaluate(code, n):
        if code < 10000000:
            return False
        
        if n < 5000 or n > 15000:
            return False
        
        return True

    @staticmethod
    def generateToken(code, n):
        countBefore = 0
        countAfter = 0

        primeAfter = code
        primeBefore = code

        currentSum = code
        currentSub = code

        while (countAfter < n or countBefore < n):
            currentSum += 1
            currentSub -= 1
            if sympy.isprime(currentSum):
                countAfter += 1
                if (countAfter == n):
                    primeAfter = currentSum
            if sympy.isprime(currentSub):
                countBefore += 1
                if (countBefore == n):
                    primeBefore = currentSub
                    
        return primeBefore * primeAfter


    @staticmethod
    def splitRequest(request):
        code, n = request.split('&')
        return int(code), int(n)



class ServerHelper:
    @staticmethod
    def waitMessage(conn, prefix=''):
        """
            function to handle and wait message from the client
        """
        conn.sendall(prefix.encode())
        message = conn.recv(1024).decode()   
        return message

    @staticmethod
    def sendMessage(conn, message):
        """
            function to handle and send messages to the client
        """
        message += '\n'
        conn.sendall(message.encode())

    @staticmethod
    def closeConnection(conn, addr):
        """
            function to close client connection
        """
        conn.sendall('/end'.encode())
        conn.close()
        print('\n' + str(addr) + ' disconnected')

    @staticmethod
    def sendRequest(host, port, message):
        """
            send a request for the other socket process
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
                connection.connect((host, port))
                connection.sendall(bytes(message, encoding='utf-8'))
                response = connection.recv(1024)
                return response.decode()

        except Exception as error:
            print(error)