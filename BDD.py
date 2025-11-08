from pyeda.inter import *



def make_R_expr(x,y):
    R_expr = []
    for i in range(32):
        for j in [(i+3) % 32, (i + 8) % 32]:
            R_expr.append(And(equal_bits(x, int_to_bits(i)), equal_bits(y, int_to_bits(j))))
    return Or(*R_expr)

def E_j(*bits, num):
    bitlist = int_to_bits(num, len(bits))
    terms = []
    for b, bt_var in zip(bitlis, bits):
        terms.append(bit_var if b == 1 else ~bit_var)
    return And(*terms)

def build_prime(*x):
    primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    prime_exprs = [E_j(*x, num=j) for j in primes]
    return Or(*prime_exprs)

def build_even(*y):
    even = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18 , 20, 22, 24, 26, 28, 30]
    even_exprs = [E_j(*y, num=j) for j in even]
    return Or(*even_exprs)

def num_to_dict(num, var):
    binary_format = "{:05b}".format(num)
    return {var[i]: int(bit) for i, bit in enumerate(binary_format)}

def testEVEN(num):
    val = num_to_dict(num, y)
    return bool(EVEN.restrict(val))


def testPRIME(num):
    val = num_to_dict(num, x)
    return bool(PRIME.restrict(val))

def testRR(num1, num2):
    val1 = num_to_dict(num1, x)
    val2 = num_to_dict(num2, y)
    val1.update(val2)
    return bool(RR.restrict(val1))

def testRR2(num1, num2):
    val1 = num_to_dict(num1, x)
    val2 = num_to_dict(num2, y)
    val1.update(val2)
    return bool(RR2.restrict(val1))

def testFunctions():
    print("Testing RR:\n")
    print(f"RR(27, 3); Epected: True; Actual: {testRR(27, 3)}\n")
    print(f"RR(16, 20); Epected: False; Actual: {testRR(16, 20)}\n")

    print("Testing EVEN:\n")
    print(f"EVEN(14); Epected: True; Actual: {testEVEN(14)}\n")
    print(f"EVEN(13); Epected: False; Actual: {testEVEN(14)}\n")

    print("Testing PRIME:\n")
    print(f"PRIME(7); Epected: True; Actual: {testPRIME(7)}\n")
    print(f"PRIME(2); Epected: False; Actual: {testPRIME(2)}\n")

    print("Testing RR2:\n")
    print(f"RR2(27, 6); Epected: True; Actual: {testRR2(27, 6)}\n")
    print(f"RR2(27, 9); Epected: False; Actual: {testRR(27, 9)}\n")


if __name__ == '__main__':
    x = exprvars('x', 5) 
    y = exprvars('y', 5)
    z = exprvars('z', 5)

    RR = expr2bdd(make_R_expr(x,y))
    PRIME = expr2bdd(build_prime(*x))
    EVEN = expr2bdd(build_even(*y))

    RR2 = (RR.compose({y[i]: z[i] for i in range(5)}) and RR.compose({x[i]: z[i] for i in range(5)})).smoothing(z)

    testFunctions()

