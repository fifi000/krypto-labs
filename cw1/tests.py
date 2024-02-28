from main import *


def test_ceaser_cipher_shift_3():
    text = "hello world"
    shift = 3
    encrypted = ceaser_cipher_encrypt(text, shift)
    assert encrypted == "khoor zruog"
    decrypted = ceaser_cipher_decrypt(encrypted, shift)
    assert decrypted == text
    universal_decrypted = ceaser_cipher_universal_decrypt(encrypted)
    assert universal_decrypted == text


def test_ceaser_cipher_shift_0():
    text = "hello world"
    shift = 0
    encrypted = ceaser_cipher_encrypt(text, shift)
    assert encrypted == "hello world"
    decrypted = ceaser_cipher_decrypt(encrypted, shift)
    assert decrypted == text
    universal_decrypted = ceaser_cipher_universal_decrypt(encrypted)
    assert universal_decrypted == text    

def test_ceaser_cipher_shift_26():
    text = "hello world"
    shift = 26
    encrypted = ceaser_cipher_encrypt(text, shift)
    assert encrypted == "hello world"
    decrypted = ceaser_cipher_decrypt(encrypted, shift)
    assert decrypted == text
    universal_decrypted = ceaser_cipher_universal_decrypt(encrypted)
    assert universal_decrypted == text


def test_vigener_cipher_key_aaa():
    text = "hello world"
    key = "aaa"
    encrypted = vigener_cipher_encrypt(text, key)
    assert encrypted == "hello world"
    decrypted = vigener_cipher_decrypt(encrypted, key)
    assert decrypted == text
    universal_decrypted = vigener_cipher_universal_decrypt(encrypted, len(key))
    assert universal_decrypted == text


def test_vigener_cipher_key_z():
    text = "hello world"
    key = "ddd"
    encrypted = vigener_cipher_encrypt(text, key)
    assert encrypted == "khoor zruog"
    decrypted = vigener_cipher_decrypt(encrypted, key)
    assert decrypted == text
    universal_decrypted = vigener_cipher_universal_decrypt(encrypted, len(key))
    assert universal_decrypted == text