import random


def prime_check(n, rounds=50):
    if n == 2:
        return True
    if not n & 1:
        return False

    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1:
            return True
        for i in range(s - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    s = 0
    d = n - 1

    while d % 2 == 0:
        d >>= 1
        s += 1

    for i in range(rounds):
        a = random.randrange(2, n - 1)
        if not check(a, s, d, n):
            return False
    return True


def generate_primes():
    p = []
    for i in range(0, 2):
        prime = random.randint(2 ** (256 - 1), 2 ** 256)

        while prime_check(prime) == False:
            prime = random.randint(2 ** (256 - 1), 2 ** 256)
        p.append(prime)

    return p


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def egcd(a, b):
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1

    while b > 0:
        r = a % b
        if r == 0:
            break
        q = a // b
        x = x0 - x1 * q
        y = y0 - y1 * q
        a = b
        b = r
        x0 = x1
        x1 = x
        y0 = y1
        y1 = y

    return x, y


def get_e(phi):
    e = random.randint(1, phi)

    while gcd(e, phi) != 1:
        e = random.randint(1, phi)

    return e


def get_d(e, phi):
    d = egcd(e, phi)[0]
    if d < 0:
        d += phi
    return d


def generate_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = get_e(phi)
    d = get_d(e, phi)
    return [[e, n], [d, n]]


def string_to_int(text):
    x = 0
    for i in text:
        x = 256 * x + ord(i)
    return x


def long_to_string(long):
    x = ""
    while long != 0:
        a = long % 256
        x = chr(a) + x
        long >>= 8
    return x


def encrypt_rsa(plain, public):
    ciphertext = pow(plain, public[0], public[1])
    return ciphertext


def decrypt_rsa(cipher, private):
    ciphertext = pow(cipher, private[0], private[1])
    return ciphertext