from Crypto.Util import number


def extended_euclidean_algorithm(a, b):
    if a < 0:
        print("A need to be non-negative")
        return -1
    if b < 0:
        print("B need to be non-negative")
        return -1

    if a < b:
        d, y, x = extended_euclidean_algorithm(b, a)
        return d, x, y

    if b == 0:
        d = a
        x = 1
        y = 0
        return d, x, y

    x2 = 1
    x1 = 0
    y2 = 0
    y1 = 1

    while b > 0:
        q = int(a / b)
        r = a - q * b
        x = x2 - q * x1
        y = y2 - q * y1

        a = b
        b = r
        x2 = x1
        x1 = x
        y2 = y1
        y1 = y
    d = a
    x = x2
    y = y2

    return d, x, y


def power_mod(base, exponent, modulo):
    if 0 > exponent:
        print("Exponent need to be non-negative.")
        # TODO Better error (the function can return -1)
        return -1
    if exponent >= modulo:
        print("The condition exponent < modulo is not fulfilled.")
        # TODO Better error (the function can return -1)
        return -1
    b = 1
    if exponent == 0:
        return b
    length = exponent.bit_length()
    a = base
    if exponent & 1 == 1:
        b = base
    exponent = exponent >> 1

    for x in range(1, length):  # length is exclusive

        a = a ** 2 % modulo
        if exponent & 1 == 1:
            b = a * b % modulo
        exponent = exponent >> 1
    return b


def generate_primes(key_size):
    assert key_size > 512, "key_size need to be greater than 512"
    assert key_size % 128 == 0, "key_size need to be a multiple of 128"

    p = number.getStrongPrime(key_size)

    while True:
        q = number.getStrongPrime(key_size)
        if p != q:
            return p, q
