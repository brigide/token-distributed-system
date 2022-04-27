import sympy

primes = ''
for i in range(0, 25000000):
    percent = (i * 100) / 25000000
    print(f'{percent:.2f}%')
    if i % 2 == 0 or i % 10 == 5:
        continue
    else:
        if sympy.isprime(i):
            primes += str(i) + '\n'


with open('primes1.txt', 'w') as file:
    file.write(primes)
