#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: Magyari-Saska Attila
SUNet: maim2158

Replace this with a description of the program.
"""
#import utils
#import math

# Caesar Cipher

def rotate_word(word, count, abc):
    '''
        Rotates a 'word' by 'count' characters. Only rotates the characters that are in 'abc'
    '''
    new_word = ''
    for char in word:
        if char not in abc:
            new_word += char
        else:
            index = abc.index(char)
            index += count

            if index < 0:
                index = len(abc) + index
            elif index >= len(abc):
                index = index - len(abc)

            new_word += abc[index]

    return new_word

def encrypt_caesar(plaintext):
    """Encrypt plaintext using a Caesar cipher.

    Add more implementation details here.
    """

    abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    count = 3
    return rotate_word(plaintext, count, abc)


def decrypt_caesar(ciphertext):
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """
    abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    count = -3
    return rotate_word(ciphertext, count, abc)


# Vigenere Cipher

def make_keyword_long_enough(keyword, length):
    '''
        Makes the 'keyword' repeate until its length reaches 'length'
    '''
    final_key = keyword
    orig_key_len = len(keyword)

    for i in range(orig_key_len, length):
        final_key += keyword[i % orig_key_len]
    return final_key

def keyword_to_shifts(keyword, abc):
    '''
        Determines how many shifts does each character mean in the 'keyword'
        returns a list with this integer values
    '''
    shifts = []

    for char in keyword:
        shifts.append(abc.index(char))

    return shifts

def encrypt_vigenere(plaintext, keyword):
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """

    abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    new_word = ''
    final_key = keyword_to_shifts(make_keyword_long_enough(keyword, len(plaintext)), abc)

    for i, char in enumerate(plaintext):
        new_word += rotate_word(char, final_key[i], abc)

    return new_word

    # raise NotImplementedError  # Your implementation here


def decrypt_vigenere(ciphertext, keyword):
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """

    abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    new_word = ''
    final_key = keyword_to_shifts(make_keyword_long_enough(keyword, len(ciphertext)), abc)

    for i, char in enumerate(ciphertext):
        new_word += rotate_word(char, -1 * final_key[i], abc)

    return new_word

    # raise NotImplementedError  # Your implementation here


# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! 
    Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    raise NotImplementedError  # Your implementation here

def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    raise NotImplementedError  # Your implementation here


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    raise NotImplementedError  # Your implementation here

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    raise NotImplementedError  # Your implementation here


def encrypt_scytale(plaintext, circumference):
    '''
        Encrypts scytale
    '''
    new_word = ''

    for i in range(0, circumference):
        for j in range(i, len(plaintext), circumference):
            new_word += plaintext[j]

    return new_word


def decrypt_scytale(ciphertext, circumference):
    '''
        Decrypts scytale
    '''
    # return encrypt_scytale(ciphertext, math.ceil(len(ciphertext) / circumference))
    new_word = ''
    steps = [int(len(ciphertext) / circumference)] * circumference
    for i in range(0, (len(ciphertext) % circumference)):
        steps[i] += 1


    for i in range(0, circumference):
        k = i
        count = 0
        while k < len(ciphertext)and len(new_word) < len(ciphertext):
            new_word += ciphertext[k]
            k += steps[count]
            count += 1

    return new_word

def get_steps_for_railfence(num_rails):
    '''
        Determines how many characters have to be jumped over for each rail - used when encoding
    '''
    steps = []

    for i in range(int((num_rails+1)/2)):
        steps.append((num_rails-i-1)*2)

    # k = steps[int(len(steps)/2)]
    rev_steps = steps[::-1]
    if num_rails % 2 == 1:
        rev_steps = rev_steps[1:]

    help_step = []

    for i, step in enumerate(rev_steps):
        help_step.append(steps[0] - step)

    help_step[len(help_step)-1] = steps[0]

    steps = steps + help_step
    print(steps)
    return steps

def encrypt_railfence(plaintext, num_rails):
    '''
        Encrypts railfence
    '''
    steps = get_steps_for_railfence(num_rails)
    new_word = ''

    for i in range(0, len(plaintext), steps[0]):
        new_word += plaintext[i]

    for i in range(1, num_rails-1):
        k = i
        count = 1
        while k < len(plaintext):
            new_word += plaintext[k]
            
            if count == 1:
                k += steps[i]
                count = 2
            else:
                k += steps[0] - steps[i]
                count = 1

    for i in range(num_rails-1, len(plaintext), steps[0]):
        new_word += plaintext[i]

    return new_word

def get_permutation(plainlist, num_rails):
    '''
        Determines how a word with len(plainlist) characters would be transformed
        when encoded in railfence. Returns a list representing the permutation
    '''
    steps = get_steps_for_railfence(num_rails)
    new_word = []

    for i in range(0, len(plainlist), steps[0]):
        new_word.append(plainlist[i])

    for i in range(1, num_rails-1):
        k = i
        count = 1
        while k < len(plainlist):
            new_word.append(plainlist[k])
            
            if count == 1:
                k += steps[i]
                count = 2
            else:
                k += steps[0] - steps[i]
                count = 1

    for i in range(num_rails-1, len(plainlist), steps[0]):
        new_word.append(plainlist[i])

    return new_word


def decrypt_railfence(ciphertext, num_rails):

    '''
        Decrypts railfence
    '''
    original_order = []
    for i in range(len(ciphertext)):
        original_order.append(i)

    print(original_order)

    order = get_permutation(original_order, num_rails)
    print(order)

    new_word = ''

    for i in range(len(ciphertext)):
        index = order.index(i)
        new_word += ciphertext[index]
    return new_word
