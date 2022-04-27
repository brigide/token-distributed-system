import socket
from sympy import prime, prevprime, nextprime, isprime

class Helpers:
    @staticmethod
    def evaluate(code, n):
        if code < 10000000:
            return False
        
        if n < 5000 or n > 15000:
            return False
        
        return True

    @staticmethod
    def generateToken(code, n, primes=None):

        if primes != None and code > 75000000:
            countBefore = 0
            countAfter = 0

            primeAfter = code
            primeBefore = code

            currentSum = code
            currentSub = code

            while countAfter < n:
                currentSum += 1

                while currentSum % 2 == 0 or currentSum % 10 == 5:
                    currentSum += 1

                if currentSum in primes:
                    countAfter += 1
                    if (countAfter == n):
                        primeAfter = currentSum
                else:
                    if isprime(currentSum):
                        countAfter += 1
                        if (countAfter == n):
                            primeAfter = currentSum

            while countBefore < n:
                currentSub -= 1
                while currentSub % 2 == 0 or currentSub % 10 == 5:
                    currentSub -= 1
                    
                if currentSub in primes:
                    countBefore += 1
                    if (countBefore == n):
                        primeBefore = currentSub
                else:
                    if isprime(currentSub):
                        countBefore += 1
                        if (countBefore == n):
                            primeBefore = currentSub

            return primeBefore * primeAfter


        elif primes != None and code <= 75000000:
            nextPrime = nextprime(code)
            nToNextPrime = primes[nextPrime]
            primeAfter = prime(nToNextPrime + n - 1)

            prevPrime = prevprime(code)
            nToPrevPrime = primes[prevPrime]
            primeBefore = prime(nToPrevPrime - n - 1)

            return primeBefore * primeAfter

        elif primes == None:
            print('none')
            countBefore = 0
            countAfter = 0

            primeAfter = code
            primeBefore = code

            currentSum = code
            currentSub = code

            while countAfter < n:
                currentSum += 1

                while currentSum % 2 == 0 or currentSum % 10 == 5:
                    currentSum += 1

                if isprime(currentSum):
                    countAfter += 1
                    if (countAfter == n):
                        primeAfter = currentSum

            while countBefore < n:
                currentSub -= 1
                while currentSub % 2 == 0 or currentSub % 10 == 5:
                    currentSub -= 1
                    
                if isprime(currentSub):
                    countBefore += 1
                    if (countBefore == n):
                        primeBefore = currentSub

            return primeBefore * primeAfter

        return 0
        


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
        try:
            if prefix != '':
                conn.sendall(prefix.encode())
            message = conn.recv(1024).decode()   
            return message
        except KeyboardInterrupt:
            return KeyboardInterrupt

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
        #conn.sendall('/end'.encode())
        conn.close()
        print('\n' + str(addr) + ' disconnected')

    @staticmethod
    def sendRequest(connection, message):
        """
            send a request for the other socket process
        """
        try:
            connection.sendall(bytes(message, encoding='utf-8'))
            response = connection.recv(1024)
            return response.decode()

        except Exception as error:
            print(error)