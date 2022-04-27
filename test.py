import argparse
from time import time
from random import randint
import socket
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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

    if args.iteration != None:
        iteration = int(args.iteration)


    print('preparing data...')
    messages = []
    for i in range(quantity):
        code = randint(10000000, 15000000)
        n = randint(5000, 7500)
        messages.append(str(code) + '&' + str(n))

    print('preparing socket...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 50002))

    print('starting...')
    iterations = []
    timeAverage = []
    for i in range(iteration):
        print('iteration: ' + str(i + 1))
        
        endTime = time() + seconds
        count = 0.0
        tokenCount = 0
        tokens = []
        timePerToken = []
        while endTime > time():
            count = seconds - (endTime - time())
            print(f'time: {count:.2f}s') 

            s.sendall(bytes(str(messages[tokenCount]), encoding='utf-8'))
            
            token = s.recv(1024).decode()
            if (time() <= endTime):
                countAfter = seconds - (endTime - time())
                print(token)
                tokens.append(f"{token}")
                tokenCount += 1
                timePerToken.append(countAfter - count)

        
        iterations.append(tokens)
        timeAverage.append(timePerToken)


    s.sendall(bytes('/end', encoding='utf-8'))
    s.close()

    print('\n\nresults')
    iterationLabel = []
    tokenCountLabel = []
    tokensPerSecondLabel = []
    timePerTokenLabel = []
    maxTokens = 0
    maxTimeToGenerate = 0
    maxSeconds = 0
    for i in range(len(iterations)):
        timePerToken = 0
        for j in range(len(timeAverage[i])):
            timePerToken += timeAverage[i][j]
            if timeAverage[i][j] > maxTimeToGenerate:
                maxTimeToGenerate = timeAverage[i][j]
            timePerTokenLabel.append(timeAverage[i][j])

        print('iteration: ' + str(i + 1))

        print('token count: ' + str(len(iterations[i])))
        print('average tokens per second: ' + str(len(iterations[i]) / seconds))
        print(f'avarage time to generate: {timePerTokenLabel[i]:.2f}s\n')

        if len(iterations[i]) > maxTokens:
            maxTokens = len(iterations[i])

        if len(iterations[i]) / seconds > maxSeconds:
            maxSeconds = len(iterations[i]) / seconds

        iterationLabel.append(i + 1)
        tokenCountLabel.append(len(iterations[i]))
        #timePerTokenLabel.append(timePerToken / len(timeAverage[i]))

        tokensPerSecondLabel.append(len(iterations[i]) / seconds)

    soma = sum(tokenCountLabel)
    media = soma/len(tokenCountLabel)
    variancia = 0
    for i in range(len(tokenCountLabel)):
        distancia = (tokenCountLabel[i]-media)**2
        variancia += distancia
    desvioPadrao = variancia/len(tokenCountLabel)
    normal = stats.norm(media, desvioPadrao)

    print("mean: ", media)
    print("variance: ", variancia)
    print("standard deviation: ", desvioPadrao)

    print('\n\nplotting...')
    fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(15, 9))

    ax0.set_xlabel('iterations')
    ax0.set_ylabel('tokens')
    ax0.set_title('tokens per second')
    ax0.bar(iterationLabel, tokenCountLabel, width=0.5)
    ax0.set(xlim=(0, len(iterations) + 1), xticks=np.arange(0, len(iterations) + 1, 1),
        ylim=(0, maxTokens + 2))

    ax1.set_xlabel('iterations')
    ax1.set_ylabel('average seconds')
    ax1.set_title('aproximate tokens per second')
    ax1.plot(iterationLabel, tokensPerSecondLabel)
    ax1.set(xlim=(1, len(iterations)), xticks=np.arange(1, len(iterations) + 1, 1),
        ylim=(0, maxSeconds + 0.5))

    ax2.set_xlabel('iterations')
    ax2.set_ylabel('average seconds')
    ax2.set_title('time to generate per iteration')
    ax2.plot(np.linspace(0, len(iterationLabel), len(timePerTokenLabel)), timePerTokenLabel)
    ax2.set(xlim=(1, len(iterations)), xticks=np.arange(1, len(iterations) + 1, 1),
        ylim=(0, maxTimeToGenerate + 0.3))


    ax3.set_ylabel('standard deviation')
    ax3.set_xlabel('token variation in iterations')
    ax3.set_title('standard deviation')
    ax3.plot(tokenCountLabel, normal.pdf(tokenCountLabel))
    # ax3.set(xlim=(1, len(iterations)), xticks=np.arange(1, len(iterations) + 1),
    #     ylim=(0, seconds + 2), yticks=np.arange(0, seconds + 2))



    plt.show()

test()