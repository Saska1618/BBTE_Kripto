import random
import os

### CREATING STREAM CIPHER ###

class StreamCipher:
    def __init__(self, key=None):
        self.method = 'solitaire'
        self.generate_key = generate_keystream_solitaire
        self.key = key

    def encrypt(self, data, key=None):

        data = data.encode("utf-8")

        #print(f'Data to encrypt : {data}')


        encrypted_data = bytearray()
        key_length = len(data)

        if key is None:

            print("Something went wrong - no key")

        else:
            #print(f'The key is already generated: {key}')
            key = eval(key)

        #print(type(data), type(key))

        for i, byte in enumerate(data):
            key_byte = key[i % key_length]
            encrypted_data.append(byte ^ key_byte)

        return bytes(encrypted_data)

    def decrypt(self, data, key=None):
        # Decryption is the same as encryption in a stream cipher
        if key is None:
            print("Something went wrong - no key")

        

        return self.encrypt(data, key)


### SOLITAIRE ###

def shuffle_cards():
    cards = [i for i in range(54)]

    shuffled_cards = random.sample(cards, len(cards))
    return shuffled_cards

def adjust_jokers(cards):
    joker_A = cards.index(52)
    joker_B = cards.index(53)

    updated_A = (joker_A + 1) % 54
    updated_B = (joker_B + 2) % 54

    cards[joker_A], cards[updated_A] = cards[updated_A], cards[joker_A]
    cards[joker_B], cards[updated_B] = cards[updated_B], cards[joker_B]

    return cards

def triple_cut(cards):
    first_joker = cards.index(52)
    second_joker = cards.index(53)

    if first_joker > second_joker:
        first_joker, second_joker = second_joker, first_joker

    new_deck = []
    new_deck = cards[second_joker+1:] + cards[first_joker:second_joker+1] + cards[:first_joker]

    return new_deck

def count_cut(cards):
    bottom = cards[53]
    count = bottom

    if count == 52:
        count = 53

    new_deck = cards[count:53] + cards[:count] + [bottom]
    return new_deck

def generate_one_letter(cards):
    top = cards[0]

    return cards[top+1]


def generate_keystream_solitaire(key_len):
    cards = shuffle_cards()
    key = []

    for i in range(key_len):
        cards = adjust_jokers(cards)
        cards = triple_cut(cards)
        cards = count_cut(cards)
        key.append(generate_one_letter(cards)%26)

    return bytes(key)

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

def encrypt_solitaire(text, key):
    encrypted = ''
    abc = 'abcdefghijklmnopqrstuvwxyz'

    for i, val in enumerate(key):
        encrypted += rotate_word(text[i], val, abc)

    return encrypted

def decrypt_solitaire(text, key):
    decrypted = ''
    abc = 'abcdefghijklmnopqrstuvwxyz'

    print(text)

    for i, val in enumerate(key):
        decrypted += rotate_word(text[i], -val, abc)

    return decrypted
