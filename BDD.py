#Jacob Atwood
#11829191
#CPTS 350
from pyeda.inter import *

#Checks if all bits match returns true if yes
def equal_bits(a_bits, b_bits):
    assert len(a_bits) == len(b_bits)
    term = 1
    for a, b in zip(a_bits, b_bits):
        if isinstance(b, int):
            term &= a if b == 1 else ~a
        else:
            term &= ~(a^b)
    return term

#converts and integer to a list of bits with a given width returns a list of the bits
def int_to_bits(num, width=5):
    return [(num >> i) & 1 for i in reversed(range(width))]

#Builds the rr relation over x and y variables in a symbolic way
def make_R_expr(x,y):
    R_expr = 0
    for i in range(32):
        for j in [(i+3) % 32, (i + 8) % 32]:
            R_expr |= equal_bits(x, int_to_bits(i)) & equal_bits(y, int_to_bits(j))
    return R_expr

#creates a symbolic expressing that matches a integer on a given list of bit variables
def E_j(*bits, num):
    bitlist = int_to_bits(num, len(bits))
    term = 1
    for b, bit_var in zip(bitlist, bits):
        term &= bit_var if b == 1 else ~bit_var
    return term

#return a symbolic representation of all prime numbers within the domain
def build_prime(*x):
    primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    prime_exprs = 0
    for p in primes:
        prime_exprs |= E_j(*x, num=p)
    return prime_exprs

#returns a symbollic representation of all even numbers within the domain
def build_even(*y):
    even = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18 , 20, 22, 24, 26, 28, 30]
    even_exprs = 0
    for e in even:
        even_exprs |= E_j(*y, num=e)
    return even_exprs

#returns the transitve closure (fixed-point) of RR2 using BDD operations
def buildRR2star(RR2):
    RR2star = RR2
    prev = None
    while True:
        prev = RR2star
        RR2star = prev | RR2
        if RR2star.equivalent(prev):
            break
    return RR2star

# verifies that the statement for all u if u is PRIME then there exists a v such that v is EVEN and u can reach v via RR2STAR
def verify(RR2STAR, PRIME, EVEN):
    RR2_with_even = RR2STAR & EVEN
    
    exists_v = RR2_with_even.smoothing(y)

    verififcation = PRIME >> exists_v

    return verififcation.is_one()

#converst an integer to a dictionary mapping BDD varibales to 0/1 for test functions
def num_to_dict(num, var_list):
    bits = [(num >> i) & 1 for i in reversed(range(len(var_list)))]
    return {var_list[i]: bits[i] for i in range(len(var_list))}

# The following below functions are used to test all of the necessary BDD functions
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

def testRR2star(num1, num2):
    val1 = num_to_dict(num1, x)
    val2 = num_to_dict(num2, y)
    val1.update(val2)
    return bool(RR2STAR.restrict(val1))

#Prints out all of the tests
def testFunctions():
    print("Testing RR:\n")
    print(f"RR(27, 3); Epected: True; Actual: {testRR(27, 3)}\n")
    print(f"RR(16, 20); Epected: False; Actual: {testRR(16, 20)}\n")

    print("Testing EVEN:\n")
    print(f"EVEN(14); Epected: True; Actual: {testEVEN(14)}\n")
    print(f"EVEN(13); Epected: False; Actual: {testEVEN(13)}\n")

    print("Testing PRIME:\n")
    print(f"PRIME(7); Epected: True; Actual: {testPRIME(7)}\n")
    print(f"PRIME(2); Epected: False; Actual: {testPRIME(2)}\n")

    print("Testing RR2:\n")
    print(f"RR2(27, 6); Epected: True; Actual: {testRR2(27, 6)}\n")
    print(f"RR2(27, 9); Epected: False; Actual: {testRR2(27, 9)}\n")

    print("Testing RR2Star:\n")
    print(f"RR2STAR(27, 6); Epected: True; Actual: {testRR2star(27, 6)}\n")
    print(f"RR2STAR(16, 20); Epected: False; Actual: {testRR2star(16, 20)}\n")

#Main function
if __name__ == '__main__':
    #create bdd vars with 5 bits
    x = bddvars('x', 5) 
    y = bddvars('y', 5)
    z = bddvars('z', 5)

    #creates the BDDS RR PRIME and EVEN
    RR = expr2bdd(make_R_expr(x,y))
    PRIME = expr2bdd(build_prime(*x))
    EVEN = expr2bdd(build_even(*y))

    #using one line to generate RR2 using .compose() and .smoothing()
    RR2 = (RR.compose({y[i]: z[i] for i in range(5)}) & RR.compose({x[i]: z[i] for i in range(5)})).smoothing(z)

    #build the RR2star to compute the trasitive closure
    RR2STAR= buildRR2star(RR2)

    #execute test functions
    testFunctions()

    #test the verification of of the statement For all u if u is PRIME then there exists a v such that b is EVEN and u can reach v via RR2STAR 
    result = verify(RR2STAR, PRIME, EVEN)

    #prints the result of the verifacation
    print(f"The statement: For all u if u is PRIME then there exists a v such that b is EVEN and u can reach v via RR2STAR is {result}")

