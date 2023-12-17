import random
from utils import *
### HELPER FUNCTIONS ###

def generate_superincreasing_sequence(n):
    starter = random.randint(2, 10)
    current_total = starter
    seq = [starter]

    for _ in range(n-1):
        num = random.randint(current_total + 1, 2 * current_total)
        seq.append(num)
        current_total += num

    return seq


### ESSENTIAL FUNCTIONS ###

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)

    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """

    w = generate_superincreasing_sequence(n)
    total = sum(w)
    q = random.randint(total + 1, 2 * total)

    r = random.randint(2, q-1)

    while not coprime(q, r):
        r = random.randint(2, q-1)

    w = tuple(w)

    priv_key = tuple([w, q, r])

    return priv_key
    

def create_public_key(private_key):
    """Creates a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    w, q, r = private_key

    beta = [r * i % q for i in w]
    beta = tuple(beta)
    
    return beta

def encrypt_character(char, beta, n):
    alpha = byte_to_bits(char)
    alpha = tuple(alpha)

    sum = 0
    for i in range(n):
        sum += (alpha[i] * beta[i])

    return sum



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
    encrypted = []
    for char in message:
        encr_char = encrypt_character(ord(char), public_key, 8)
        encrypted.append(encr_char)

    return encrypted

def maxW_smaller_cp(w, cp, n):
    for i in range(n-1, -1, -1):
        if w[i] <= cp:
            return i+1

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

    w, q, r = private_key
    s = modinv(r, q)

    msg = ''

    for c in message:
        num = 0
        cp = c * s % q

        while cp > 0:
            print(f"w {w} cp {cp} maxw {maxW_smaller_cp(w, cp, 8)}")
            val = maxW_smaller_cp(w, cp, 8)
            num += 2 ** (8-val)

            cp = abs(cp - w[val-1])

        msg += chr(num)
        

    return msg

def generate_knapsack_key_pair():
    priv_key = generate_private_key()
    pub_key = create_public_key(priv_key)

    return priv_key, pub_key

priv_key, pub_key  = generate_knapsack_key_pair()


# uzi = '8001-G5ANz4jv1t'

# enc = encrypt_mh(uzi, pub_key)
# print(f'enc {enc}')

# dec = decrypt_mh(enc, priv_key)
# print(f'dec {dec}')