import string
import itertools

from nltk.corpus import words


ALPHABET = list(string.ascii_lowercase)
ALPHABET_DICT = {char: i for i, char in enumerate(ALPHABET)}


def ceaser_cipher_encrypt(text: str, k: int) -> str:
    """
    Encrypts the given text using the Caesar cipher algorithm.

    Args:
        text (str): The text to be encrypted.
        k (int): The number of positions to shift each character.

    Returns:
        str: The encrypted text.
    """
    text = text.lower()

    # helper function to encrypt a single character
    def encrypt_char(char: str) -> str:
        if char in ALPHABET_DICT:
            return ALPHABET[(ALPHABET_DICT[char] + k) % len(ALPHABET)]
        return char

    return ''.join( 
        encrypt_char(char)
        for char in text
    )


def ceaser_cipher_decrypt(text: str, k: int) -> str:
    """
    Decrypts the given text using the Caesar cipher algorithm using negative shift.

    Args:
        text (str): The text to be encrypted.
        k (int): The number of positions original text was shifted.

    Returns:
        str: The decrypted text.
    """
    return ceaser_cipher_encrypt(text, -k)


def ceaser_cipher_universal_decrypt(text: str) -> str:
    """
    Decrypts a Caesar cipher encrypted text using a brute force approach.
    Finds the best match by counting English words among the decrypted texts.

    Args:
        text (str): The text to be decrypted.

    Returns:
        str: The decrypted text.
    """
    text = text.lower()

    # remove punctuation
    for p in string.punctuation:
        text = text.replace(p, '')

    candidates = [
        ceaser_cipher_decrypt(text, k) 
        for k in range(len(ALPHABET))
    ]

    return find_best_candidate(candidates)
        

def vigener_cipher_encrypt(text: str, key: str) -> str:
    """
    Encrypts the given text using the Vigenere cipher with the provided key.

    Args:
        text (str): The text to be encrypted.
        key (str): The key used for encryption.

    Returns:
        str: The encrypted text.
    """
    text = text.lower()
    key = key.lower()
    key = itertools.cycle(key)

    def encrypt_char(char: str) -> str:
        if char in ALPHABET_DICT:
            return ceaser_cipher_encrypt(char, ALPHABET_DICT[next(key)])
        return char
    
    return ''.join(
        encrypt_char(char)
        for char in text
    )


def vigener_cipher_decrypt(text: str, key: str) -> str:
    """
    Decrypts the given text using the Vigenere cipher algorithm with the original key.

    Args:
        text (str): The text to be decrypted.
        key (str): The key originally used for encryption.

    Returns:
        str: The decrypted text.
    """
    key = key.lower()    
    new_key = ''.join([
        ALPHABET[-ALPHABET_DICT[k]] 
        for k in key
    ])

    return vigener_cipher_encrypt(text, new_key)


def vigener_cipher_universal_decrypt(text: str, key_len: int) -> str:
    """
    Decrypts a Vigener cipher encrypted text using a brute force approach.
    Finds the best match by counting English words among the decrypted texts.

    Args:
        text (str): The text to be decrypted.
        key_len (int): The length of the key used for encryption.
    Returns:
        str: The decrypted text.
    """
    possible_keys = itertools.product(ALPHABET, repeat=key_len)

    candidates = [
        vigener_cipher_decrypt(text, ''.join(key)) 
        for key in possible_keys
    ]

    return find_best_candidate(candidates)


def find_best_candidate(candidates: list[str]) -> str:
    """
    Finds the best candidate from a list of candidates based on the score.
    The score is calculated by counting the number of English words in the text.

    Args:
        candidates (list[str]): The list of candidates to choose from.

    Returns:
        str: The best candidate.

    """
    words_set = set(words.words())

    def score(text: str) -> int:
        return sum(word in words_set for word in text.split())
    
    return max(candidates, key=score)


if __name__ == '__main__':    
    # ceaser cipher - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    text = '''
        This method is quite basic and might not work well for short or ambiguous texts.
        For more reliable language detection, especially for short texts or texts that 
        might be in any language, consider using a dedicated language detection library.
    '''

    shift = 0

    print('original:', text)

    encrypted_text = ceaser_cipher_encrypt(text, shift)
    print('ceaser encrypted:', encrypted_text)

    decrypted_text = ceaser_cipher_decrypt(encrypted_text, shift)
    print('ceaser decrypted:', decrypted_text)

    decrypted_text = ceaser_cipher_universal_decrypt(encrypted_text)
    print('ceaser universal decrypted:', decrypted_text)
    print()

    # vigenere cipher - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    text = '''
        This method is quite basic and might not work well for short or ambiguous texts.
        For more reliable language detection, especially for short texts or texts that 
        might be in any language, consider using a dedicated language detection library.
    '''
    key = 'aa'
    
    print('original:', text)

    vigenere_encrypted = vigener_cipher_encrypt(text, key)
    print('vigenere encrypted: ', vigenere_encrypted)

    vigenere_decrypted = vigener_cipher_decrypt(vigenere_encrypted, key)
    print('vigenere decrypted: ', vigenere_decrypted)

    vigenere_decrypted = vigener_cipher_universal_decrypt(vigenere_encrypted, len(key))
    print('vigenere universal decrypted: ', vigenere_decrypted)

