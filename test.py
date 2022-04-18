import argparse
from time import time
from random import randint
import socket

def test():
    quantity = 100000
    seconds = 5
    iteration = 3

    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--quantity', help='Quantity')
    parser.add_argument('-s', '--seconds', help='Seconds')
    parser.add_argument('-i', '--iteration', help='Iteration')

    args = parser.parse_args()

    if args.quantity != None:
        quantity = int(args.quantity)

    if args.seconds != None:
        seconds = int(args.seconds)

    if args.seconds != None:
        iteration = int(args.iteration)


    print('preparing data...')
    messages = []
    for i in range(quantity):
        code = randint(10000000, 20000000)
        n = randint(5000, 15000)
        messages.append(str(code) + '&' + str(n))

    print('preparing socket...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 50002))

    print('starting...')
    iterations = []
    for i in range(iteration):
        print('iteration: ' + str(i + 1))
        
        endTime = time() + seconds
        count = 0.0
        tokenCount = 0
        tokens = []
        while endTime > time():
            count = seconds - (endTime - time())
            print(f'time: {count:.2f}s') 

            s.sendall(bytes(str(messages[tokenCount]), encoding='utf-8'))
            token = s.recv(1024).decode()

            print(token)
            tokens.append(f"{token}")
            tokenCount += 1
        
        iterations.append(tokens)

    for i in range(len(iterations)):
        print('iteration: ' + str(i + 1))

        print('token count: ' + str(len(iterations[i])))
        print('average tokens per second: ' + str(len(iterations[i]) / seconds) + '\n')


    s.sendall(bytes('/end', encoding='utf-8'))
    s.close()

test()