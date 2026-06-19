# In order to run this program, you need to install a Python package called egcd which is a basic, efficient, and pure-Python implementation of the extended Euclidean algorithm. Information can be found here: https://egcd.readthedocs.io/en/0.6.0/
# The command to install this package: pip install egcd

# pip install egcd

import sys
import math
from egcd import egcd

    
#=====================================================
# Please do NOT modify the following code, but you are more than welcome to understand the code in detail

class ExtendedAffineCipher:
    
    def __init__(self, alphabet_start, alphabet_end):
        self.alphabet_start = alphabet_start
        self.ord_start = ord(self.alphabet_start[0])
        self.alphabet_end = alphabet_end
        self.alphabet_size = ord(alphabet_end[0])-ord(alphabet_start[0])+1
    
    
    def get_alphabet_size(self):
        return self.alphabet_size
         
    
    def encrypt(self, plain_text, key_a, key_b):
        
        if None == plain_text:
            sys.exit('No plain text to encrypt!')
        
        # Check if the input is legitimate
        for i in plain_text:
            if self.alphabet_start > i and self.alphabet_end < i:
                sys.exit('Illegimate char in the plain text, check against the alphabet set!')
                
        # Check if key_a is a legitimate key
        if not self.is_coprime(key_a, self.alphabet_size):
            sys.exit('The parameter key_a is not set appropriately. Please select a value co-prime with the alphabet size!')
        else:
            key_a = key_a%self.alphabet_size
            key_b = key_b%self.alphabet_size
        
        cipher_text = ""
        for i in plain_text:
            cipher_text += chr((key_a*(ord(i)-self.ord_start)+key_b)%self.alphabet_size + self.ord_start)
        return cipher_text
    
    
    # We use the analytical way with the extended Euclidean Algorithm (note, an exhaustive way might be also possible)
    def decrypt(self, cipher_text, key_a, key_b):
        
        if None == cipher_text:
            sys.exit('No plain text to encrypt!')
        
        # Check if the input is legitimate
        for i in cipher_text:
            if self.alphabet_start > i and self.alphabet_end < i:
                sys.exit('Illegimate char in the plain text, check against the alphabet set!')
                        
        # Check if key_a is a legitimate key
        if not self.is_coprime(key_a, self.alphabet_size):
            sys.exit('The parameter key_a is not set appropriately. Please select a value co-prime with the alphabet size!')
        else:
            key_a = key_a%self.alphabet_size
            key_b = key_b%self.alphabet_size
        
        plain_text=""
        for i in cipher_text:
            plain_text += chr(self.multiplicative_inverse_with_egcd(key_a, key_b, (ord(i)-self.ord_start), self.alphabet_size) + self.ord_start)
        
        return plain_text

        
    # A function determines if two values are coprime
    def is_coprime(self, a, b):
        
        # Use the greatest common divisor (GCD) for the decision
        return 1 == math.gcd(a, b)
    
    
    # Solve equation: a * x + b = c (mod n)
    def multiplicative_inverse_with_egcd(self, a, b, c, n):
        
        # Solve a * y = 1 (mod n) using EGCD
        y = egcd(a, n)[1]
        
        # Now we have a * y * (c-b) = (c-b) (mod n)
        x = (y*((c-b+n)%n))%n
        
        return x

#=====================================================
# Examples of using the extended affine cipher
# Please do NOT alter this part. In Task A, we will use the same alphabet as in the follow example.

# Define an extended affine cipher where the alphabet set ranges from ' ' to '\x7f' (corresponding the printable characters). Please refer to https://www.ascii-code.com the more details about ASCII code table.
cipher = ExtendedAffineCipher(' ', '\x7f')
print("Alphabet size is: ", cipher.get_alphabet_size())

# Encrypt a plain text with the key pair (11, 10)
cipher_text = cipher.encrypt("Hello World, COMP2300/6300!", 11, 10)
print("The example cipher text is: ", cipher_text)

# Decrypt the cipher text generated above
plain_text = cipher.decrypt(cipher_text, 11, 10)
print("The example plain text is: ", plain_text)
print("")

#=====================================================
# Following area is for you to write or complete the code to achieve the answers to Task A

print("\n--- Subtask A.1 ---")

# Subtask A.1 (2 marks): Calculate the number of all the appropriate key pairs and choose a pair of appropriate keys (different from the one used in the example above) to encrypt the plain text "Hello World, COMP2300/6300!". 
# Report (1) the number of all propriate key pairs, (2) the chosen key pair, and the corresponding cipher text as the answers of Task A.1 in the assignment answer template.

plain_text_A_1 = "Hello everyone, welcome to COMP2300/6300!"

# TODO: Your code
def find_coprime_numbers(n):
    coprime_numbers = []
    for i in range(1, n):
        if math.gcd(i, n) == 1:
            coprime_numbers.append(i)
    return coprime_numbers

# Alphabet size
alphabet_size = cipher.get_alphabet_size()

# Find appropriate key_a values
valid_key_a_values = find_coprime_numbers(alphabet_size)
total_key_pairs = len(valid_key_a_values) * alphabet_size

print("Number of appropriate key pairs:", total_key_pairs)

# Choose key pair (different from example)
key_a_A_1 = valid_key_a_values[1]  
key_b_A_1 = 15  

# Encrypt message
cipher_text_A_1 = cipher.encrypt(plain_text_A_1, key_a_A_1, key_b_A_1)
print("Chosen key pair: (", key_a_A_1, ",", key_b_A_1, ")")
print("Cipher text for Task A.1:", cipher_text_A_1)


# Subtask A.2 (3 marks): Now, you are given a piece of cipher text "uA,)V,X)<.,%)Hk)n<w5p.V)W+G)H.)5A,).5<%,k5)(e)U9999999})pk%)5A,)V,X)<.,%)Hk)n<w5p.V)W+N)H.)Xr<')rJk).5<%,k5)(e+", but the key pair is missing.
# Your task is to figure out the key pair and decrypt the cipher text. The corresponding plain text is a meaningful piece of text which offers important information the Task B and Task C.
# To facilitate your cryptanalysis, we have the following plaintext-ciphertext pair: 
#    Plaintext:  Hellow World!
#    Ciphertext: !,]]rJ)*r']%0
# There are two options to achieve this subtask, BUT you just need to choose one to complete. 
# Option 1 is to use analytical analysis with solving a system of equations, which would be more advanced and efficient.
# Option 2 is to use the exhaustive method to try all the possible keys (simple but needs more computation), and check if the deciphered text is meaningful. If you follow this option, you are required to MINIMISE the number of possible keys to attempt. 
# Report (1) For Option 1: descibe the system of equations and how you build it,
#            For Option 2: the number of possible keys you have tried (with justification on if this is the minimal number of attempts),
# (2) the identified key pair, and (3) the corresponding plain text as the answers of Task A.2 in the assignment answer template.

cipher_text_A_2 = "uA,)V,X)<.,%)Hk)n<w5p.V)W+G)H.)5A,).5<%,k5)(e)U9999999})pk%)5A,)V,X)<.,%)Hk)n<w5p.V)W+N)H.)Xr<')rJk).5<%,k5)(e+"

# TODO: Your code to decrypt the cipher text
# Option 1: Analytical inference

# Subtask A.2 (3 marks) - Option 1: Analytical inference

print("\n--- Subtask A.2 ---")

# Known plaintext and ciphertext 
known_plaintext = "Hello World!"
known_ciphertext = "!,]]rJ)*r']%0"

# Extract corresponding plaintext and ciphertext characters
p1, p2 = known_plaintext[0], known_plaintext[1]
c1, c2 = known_ciphertext[0], known_ciphertext[1]

# Convert characters to their ordinal values 
p1_ord = ord(p1) - cipher.ord_start
p2_ord = ord(p2) - cipher.ord_start
c1_ord = ord(c1) - cipher.ord_start
c2_ord = ord(c2) - cipher.ord_start

# Calculate multiplicative inverse of (p2_ord - p1_ord) % alphabet_size
p_diff_inv = egcd(p2_ord - p1_ord, alphabet_size)[1]

# Calculate key_a
key_a = ((c2_ord - c1_ord) * p_diff_inv) % alphabet_size

# Substitute key_a into equation 1 to find key_b
key_b = (c1_ord - key_a * p1_ord) % alphabet_size

# Decryp ciphertext using found key pair
plain_text_A_2 = cipher.decrypt(cipher_text_A_2, key_a, key_b)

# Print results
print("System of equations:")
print("  Equation 1:", c1_ord, "=", "(key_a *", p1_ord, "+ key_b) %", alphabet_size)
print("  Equation 2:", c2_ord, "=", "(key_a *", p2_ord, "+ key_b) %", alphabet_size)
print("\nIdentified key pair: (key_a =", key_a, ", key_b =", key_b, ")")
print("Corresponding plain text:", plain_text_A_2)

