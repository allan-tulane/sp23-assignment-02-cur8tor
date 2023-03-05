"""
CMPS 2200  Assignment 2.
See assignment-02.pdf for details.
Tanner Martz v3.4.23-04
"""
import time

class BinaryNumber:
    """ done """
    def __init__(self, n):
        self.decimal_val = n               
        self.binary_vec = list('{0:b}'.format(n)) 
        
    def __repr__(self):
        return('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))
    

## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.
def binary2int(binary_vec): 
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))

def split_number(vec):
    return (binary2int(vec[:len(vec)//2]),
            binary2int(vec[len(vec)//2:]))

def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)
    
def pad(x,y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y)-len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x)-len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x,y

def subquadratic_multiply(x, y):
    ### TOD0:

    """
    Multiplies two BinaryNumber objects using a divide-and-conquer approach.
    Assumes x and y are binary vectors of equal length with an even number of bits.
    """
    # Get binary vectors of x and y
    x_vec = x.binary_vec
    y_vec = y.binary_vec
    
    # Base case: if x and y are single bits, return their product
    if x.decimal_val <= 1 and y.decimal_val <= 1:
        return BinaryNumber(x.decimal_val * y.decimal_val)
    
    # Pad x and y with leading zeros to ensure they have the same number of bits
    x_vec, y_vec = pad(x_vec, y_vec)
    
    # Get the length of the binary vectors
    length = len(x_vec)
    
    # Split x and y into left and right halves
    x_L, x_R = split_number(x_vec)
    y_L, y_R = split_number(y_vec)
    
    # Recursively compute the products of the left and right halves
    left = subquadratic_multiply(x_L, y_L)
    right = subquadratic_multiply(x_R, y_R)
    
    # Compute the sum of the left and right halves of x and y
    x_sum = BinaryNumber(x_L.decimal_val + x_R.decimal_val)
    y_sum = BinaryNumber(y_L.decimal_val + y_R.decimal_val)
    
    # Compute the product of the sums and subtract the products of the left and right halves
    mid_opp = subquadratic_multiply(x_sum, y_sum).decimal_val 
    mid = BinaryNumber(mid_opp - left.decimal_val - right.decimal_val)
    
    # Bit-shift the middle product to the right position
    mid = bit_shift(mid, length//2) 
    left = bit_shift(left, length)
    
    # Compute the final product as the sum of the three products
    return BinaryNumber(left.decimal_val + mid.decimal_val + right.decimal_val)
  

## Feel free to add your own tests here.
def test_multiply():
    assert subquadratic_multiply(BinaryNumber(2), BinaryNumber(2)).decimal_val == 2*2
    assert subquadratic_multiply(BinaryNumber(3), BinaryNumber(4)).decimal_val == 3*4
    assert subquadratic_multiply(BinaryNumber(5), BinaryNumber(6)).decimal_val == 5*6
    assert subquadratic_multiply(BinaryNumber(0), BinaryNumber(1)).decimal_val == 0*1

def time_multiply(x, y, f):
    start = time.time()
    # multiply two numbers x, y using function f
    f(BinaryNumber(x), BinaryNumber(y))
    return (time.time() - start)*1000

if __name__ == "__main__":
    print("start tests.")
    # Test subquadratic_multiply function
    print("test_multiply():")
    test_multiply()
    # Test the performance of subquadratic_multiply function on a range of inputs
    print("time_multiply():")
    test_range = list(map(lambda n: 2**n, range(0,1000,100)))
    for test in test_range:
        t = time_multiply(test, test, subquadratic_multiply)
        print("test {:.2e} * {:.2e} in {:.8f}ms".format(test, test, t))
    print("tests complete.")