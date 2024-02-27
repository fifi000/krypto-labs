import string
import itertools
from tqdm import tqdm

from nltk.corpus import words


ALPHABET = list(string.ascii_letters)


def ceaser_cipher_encrypt(text: str, k: int) -> str:
    text = text.lower()    
    result = ''

    for char in text:
        if char in ALPHABET:
            result += ALPHABET[(ALPHABET.index(char) + k) % len(ALPHABET)]
        else:
            result += char

    return result


def ceaser_cipher_decrypt(text: str, k: int) -> str:
    return ceaser_cipher_encrypt(text, -k)


def ceaser_cipher_universal_decrypt(text: str) -> str:
    text = text.lower()

    candidates = [
        ceaser_cipher_decrypt(text, k) 
        for k in range(len(ALPHABET))
    ]

    return find_best_candidate(candidates)
        

def vigener_cipher_encrypt(text: str, key: str) -> str:
    text = text.lower()
    key = key.lower()

    result = ''
    key = key * (len(text) // len(key)) + key[:len(text) % len(key)]


    for i, char in enumerate(text):
        if char in ALPHABET:
            result += ALPHABET[(ALPHABET.index(char) + ALPHABET.index(key[i])) % len(ALPHABET)]
        else:
            result += char

    return result


def vigener_cipher_decrypt(text: str, key: str) -> str:
    key = key.lower()
    new_key = ''.join([ALPHABET[-ALPHABET.index(k)] for k in key])

    return vigener_cipher_encrypt(text, new_key)


def vigener_cipher_universal_decrypt(text: str, key_len) -> str:
    possible_keys = itertools.permutations(ALPHABET, key_len)

    candidates = [
        vigener_cipher_decrypt(text, ''.join(key)) 
        for key in possible_keys
    ]

    return find_best_candidate(candidates)


def __find_best_candidate(candidates: list[str], best_n = 1) -> list[dict]:
    from spacy_langdetect import LanguageDetector
    import spacy
    from spacy.language import Language

    # load spacy model for language detection
    nlp = spacy.load('en_core_web_sm')
    Language.factory(
        'language_detector', 
        func=lambda nlp, name: LanguageDetector()
    )
    nlp.add_pipe('language_detector', last=True)

    # filter out non-english texts
    # asign score to each candidate
    filtered = [
        {'score': lang['score'], 'text': c}
        for c in tqdm(candidates) 
        if (lang := nlp(c)._.language)['language'] == 'en'
    ]

    # return highest scored texts
    return sorted(filtered, key=lambda x: x['score'], reverse=True)[:best_n]


def find_best_candidate(candidates: list[str]) -> str:
    words_set = set(words.words())

    def score(text: str) -> int:
        return sum([word in words_set for word in text.split()])
    
    return max(candidates, key=score)


if __name__ == '__main__':    
    # ceaser cipher - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    text = '''
        This method is quite basic and might not work well for short or ambiguous texts.
        For more reliable language detection, especially for short texts or texts that 
        might be in any language, consider using a dedicated language detection library.
    '''
    encrypted_text = ceaser_cipher_encrypt(text, 3)
    print('ceaser encrypted: ', encrypted_text)

    decrypted_text = ceaser_cipher_universal_decrypt(encrypted_text)
    print('ceaser decrypted: ', decrypted_text)
    print()

    # vigenere cipher - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    text = '''
        This method is quite basic and might not work well for short or ambiguous texts.
        For more reliable language detection, especially for short texts or texts that 
        might be in any language, consider using a dedicated language detection library.
    '''
    key = 'abc'
    
    vigenere_encrypted = vigener_cipher_encrypt(text, key)
    print('vigenere encrypted: ', vigenere_encrypted)

    vigenere_decrypted = vigener_cipher_universal_decrypt(vigenere_encrypted, len(key))
    print('vigenere decrypted: ', vigenere_decrypted)






