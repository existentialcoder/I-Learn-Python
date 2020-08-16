#!/usr/bin/env python3
def is_prime_number(num):
    i = 2
    isPrime = True
    while i <= (num // 2):
        if num % i == 0:
            isPrime = False
            break
        i += 1
    return isPrime

number = int(input('Enter number \n'))
isPrime = is_prime_number(number)

print('{} is {}'.format(number, 'prime' if isPrime else 'composite'))
