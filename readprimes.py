primes = {}
with open('primes.txt', 'r') as file:
    content = file.readlines()
    for i in range(len(content)):
        primes[int(content[i].strip('\n'))] = i

print('loaded')
print(4 in primes)
print(primes[44544371])
