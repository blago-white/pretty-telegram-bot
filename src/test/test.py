import random

num = random.randint(10000, 99999)
print('Случайное число: {}'.format(num))
print('Cумма цифр: {}'.format(
    (num // 10000) + ((num%10000) // 1000) + ((num%1000) // 100) + ((num // 10) % 10) + (num % 10)))
