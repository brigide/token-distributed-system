import argparse
from time import time
from random import randint
import socket

def test():
    quantity = 10000
    seconds = 5

    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--quantity', help='Quantity')
    parser.add_argument('-s', '--seconds', help='Seconds')

    args = parser.parse_args()

    if args.quantity != None:
        quantity = int(args.quantity)

    if args.seconds != None:
        seconds = int(args.seconds)


    print('preparing data...')
    messages = []
    for i in range(quantity):
        code = randint(10000000, 20000000)
        n = randint(5000, 15000)
        messages.append(str(code) + '&' + str(n))

    print('preparing socket...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 50002))
    print(s)

    print('starting...')
    endTime = time() + seconds
    count = 0.0
    i = 0
    while endTime > time():
        count = seconds - (endTime - time())
        print(f'{count:.2f}s') 
        s.sendall(bytes(str(messages[i]), encoding='utf-8'))
        print(f"{s.recv(1024).decode()}")
        i += 1
    
    print('token count: ' + str(i))
    print('average tokens per second: ' + str(i / seconds))

    s.sendall(bytes('/end', encoding='utf-8'))
    s.close()

test()