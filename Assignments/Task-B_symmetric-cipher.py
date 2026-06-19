#import cryptography
from cryptography.fernet import Fernet # for encryption and decryption
import base64
import sys
# if you get an error on the above line, you might need to run 
# pip install INSERT_LIBRARY_NAME or install the library another way.

#=====================================================
# Please do NOT modify the following code, but you are more than welcome to understand the code in detail

# This function generates a key from a given string representing a student's ID
# The base64 encoding changes 3 bytes into 4 bytes. Resultant alphabet contains letters, numbers, and three symbols +, /, and = (for padding)
def generate_key_from_string(key_string="please don't use the default"):
    if(len(key_string)<32):
       key_string = str(key_string + "abcdefghijklmnopqrstuvwxyz012345")
    key_string = key_string[0:32]
    key_string_bytes = str(key_string).encode("utf-8")
    key = base64.urlsafe_b64encode(key_string_bytes) 
    return key


# Examples
# Generate a key from a string
key = generate_key_from_string(key_string="12345678")
print("Example key is: ", key)
print("Length of the encoded key is: %d bytes" % len(key)) # The length should be a multiple of 4.
print("")

# Create a fernet with the key
fernet = Fernet(key)

# Plain text
plain_text = "Hellow World, COMP2300/6300!"

# Convert the string to binary string
plain_text_bytes = bytes(plain_text, "utf-8")
print("Example plain text byte string: ", plain_text_bytes)

# Encrypt the plain text and print the cipher text
cipher_text = fernet.encrypt(plain_text_bytes)
print("Example cipher text is: ", cipher_text)

# Binary string of the cipher text
cipher_text_binary_chars = []
for i in cipher_text:
    cipher_text_binary_chars.append(format(i, '08b'))
cipher_text_binary_string = ''.join(cipher_text_binary_chars)
print("Binary string for cipher text: ", cipher_text_binary_string)

# Decrypt the cipher text
decrypted_text_bytes = fernet.decrypt(cipher_text)

# Convert the bytes into string
decrypted_text = decrypted_text_bytes.decode("utf-8")
print("Example decrypted text is: ", decrypted_text)
print("")


#=====================================================
# Following area is for your to write or compelete the code to acheive the answers to Task B


# Subtask B.1 (3 marks): Write the corresponding code to answer the following questions.
# Please carefully go through the follwoing documentations to understand the fernet format and answer the questions correctly: https://cryptography.io/en/latest/fernet/, and https://github.com/fernet/spec/blob/master/Spec.md.
# Report the answers as the answers of Task B.1 in the assignment answer template  
# (1). In the example demonstrated above, whether the plain text and the cipher text have the same length as we expect as a pair of plain text and cipher text? Please explain the reason in detail.
# (2). Run the encryption function again to encrypt the same message, i.e., "Hellow World, COMP2300/6300!".
#      Whether the two resultant cipher texts for the same plain text are the same? Please explain the reason in detail.
# (3). Select a position in the plain text, replace the character with a different one of your choice. Now, the two plain texts have one character difference. 
#      You are requested to encrypt the modified plain text and compare the corresponding cipher text with that from the original plain text. 
#      Report the change you have made to the plain text, the corresponding cipher text, and what the percentage of positions having the same bit values in the two pieces of cipher text is.
#      Note that percetage should be calculated at the bit level.

# TODO: Your code to answer the questions above.

print("\n--- Subtask B.1 ---")
# (1) No, the plain text and cypher text are not the same length. The ciphertext is longer than the plaintext. This is because Fernet 
# utilises padding to ensure that the input data is a multiple of the block size used by the encryption method (AES in CBC mode). 
# It also includes a 16-byte initialisation vector (IV) at the start of the ciphertext and a 16-byte authentication tag (HMAC) at the 
# end of it. These modifications make the ciphertext larger than the original plaintext.

# (2)
cipher_text2 = fernet.encrypt(plain_text_bytes)
print("Second cipher text is: ", cipher_text2)

#No, the two resulting ciphertexts are not identical. This is because Fernet employs a random initialisation vector (IV) for each 
# encryption process. The IV is included in the ciphertext, ensuring that even if the same plaintext is encrypted numerous times with 
# the same key, the subsequent ciphertexts are distinct. This provides an additional degree of protection by making it more difficult 
# for an attacker to spot patterns in the encrypted data.

# (3)
# Modify plain text (replace first 'o' with 'e')
modified_plain_text = "Helle World, COMP2300/6300!"
modified_plain_text_bytes = bytes(modified_plain_text, "utf-8")

# Encrypt modified plain text
modified_cipher_text = fernet.encrypt(modified_plain_text_bytes)

# Convert cipher texts to binary strings for comparison
cipher_text_binary_string2 = ''.join(format(i, '08b') for i in modified_cipher_text)

# Compare two cipher texts at bit level
same_bits_count = 0
total_bits = len(cipher_text_binary_string)
for i in range(total_bits):
    if cipher_text_binary_string[i] == cipher_text_binary_string2[i]:
        same_bits_count += 1

percentage_same = (same_bits_count / total_bits) * 100

# Report results
print("\nModified plain text:", modified_plain_text)
print("Modified cipher text:", modified_cipher_text)
print("Percentage of same bits in the two cipher texts:", percentage_same)

# Subtask B.2 (1 mark): You are given a file containing a piece of cipher text. The key information is provided by the answer to Task A.2.
# Your task is to decrypt the cipher text (The decrypted text should be readable in English). 
# After decrypt the file successfully, report the line 6 of the text file as the answers of Task B.2 in the assignment answer template.

# Read the cipher text from the file as a string. 
# Note: if you use Windows, the file containing the cipher text should be "windows_data_encrypted.txt"

print("\n--- Subtask B.2 ---")

#File path 
file_path = r"C:\Users\abhay\Desktop\Uni\Year 2\semester 2\comp2300\Assignment 1\windows_data_encrypted.txt.txt"

# Generate key from the provided string (A.2 answer)
key = generate_key_from_string(key_string="40000000")
fernet = Fernet(key)

# Read cipher text from file 
with open(file_path, 'rb') as file:  
    cipher_text_B_2 = file.read()

# Decrypt cipher text 
plain_text_B_2 = fernet.decrypt(cipher_text_B_2).decode("utf-8")

# File path for decrypted plaintext output
output_plaintext_file = r"C:\Users\abhay\Desktop\Uni\Year 2\semester 2\comp2300\Assignment 1\47717653_Task-B-2_plain-text.txt"

# Write decrypted plaintext to file
with open(output_plaintext_file, 'w', encoding='utf-8') as file:
    file.write(plain_text_B_2)

print("Decrypted plaintext saved to:", output_plaintext_file)

# Split plaintext into lines and get line 6
lines = plain_text_B_2.splitlines()
line_6 = lines[5] 

# Print line 6
print("Line 6 of the decrypted text:", line_6)

# Subtask B.3 (1 mark): You are requested to encrypt the plain text from Subtask B.2 with a different key. The key information is also provided by the answer to Task A.2.
# The cipher text should be stored in a file which will be submitted for evaluation and marking (The markers will check if it is able to be decrypted with the given key).
# The cipher text file should be named with the format "<YourStudentID>_Task-B-2_cipher-text.txt", where <YourStudentID> should be replaced by your own student ID.

# TODO: Your code to achieve encryption

# Subtask B.3 (1 mark)

print("\n--- Subtask B.3 ---")

# Use key from A.2 answer
new_key_string = "47717653" 
new_key = generate_key_from_string(key_string=new_key_string)
new_fernet = Fernet(new_key)

# Encrypt plaintext from B.2
cipher_text_B_3 = new_fernet.encrypt(plain_text_B_2.encode("utf-8"))

output_filename = r"C:\Users\abhay\Desktop\Uni\Year 2\semester 2\comp2300\Assignment 1\47717653_Task-B-2_cipher-text.txt"

# Write cipher text to file ('wb' mode for binary data)
with open(output_filename, 'wb') as file:
    file.write(cipher_text_B_3)

print("Ciphertext saved to:", output_filename)

