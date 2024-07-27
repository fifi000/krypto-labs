import math
import timeit
from typing import Callable, Iterable, Literal
from logging import getLogger
from string import ascii_lowercase, ascii_uppercase, whitespace


logger = getLogger(__name__)


def logger_wrapper(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start = timeit.default_timer()
        logger.debug(f'Starting {func.__name__}')
        result = func(*args, **kwargs)
        logger.debug(f'Finished {func.__name__} in: {timeit.default_timer() - start:.4f}s')
        return result
    return wrapper
    

def encrypt(text: str) -> str:
    # Step 0
    # prepare text
    text = __prepare_text(text)
    length = len(text)
    
    # Step 1
    # Create a square
    matrix = __create_matrix(text)
    assert all(len(row) == len(matrix) for row in matrix)
    
    # Step 2
    # Castle columns
    matrix = __castle_columns(matrix, 'short')
    assert all(len(row) == len(matrix) for row in matrix)
    
    # Step 3
    # Castle rows
    matrix = __castle_rows(matrix)
    assert all(len(row) == len(matrix) for row in matrix)
    
    # Step 4
    # encript each line with the Ceaser cipher
    lines = (''.join(row) for row in matrix)
    lines = __encrypt_lines(lines)
    
    assert all(len(line) == len(matrix) for line in lines)
    
    return '\n'.join(lines)
    

@logger_wrapper
def __prepare_text(text: str) -> str:
    new_text = []
    
    # set all characters to lowercase
    # all whitespaces are replaced with a space
    for char in text:
        if char in ascii_lowercase:
            new_text.append(char)
        elif char in whitespace:
            new_text.append(' ')
        elif char in ascii_uppercase:
            new_text.append(char.lower())
            
    return ''.join(new_text)
    
    
@logger_wrapper    
def __create_matrix(text: str) -> list[list[str]]:
    # create a square matrix
    side_len = math.ceil(len(text) ** 0.5)
    matrix = [
        [' ' for _ in range(side_len)] 
        for _ in range(side_len)
    ] 
    
    # fill the matrix
    for i, char in enumerate(text):
        matrix[i // side_len][i % side_len] = char
            
    return matrix

    
@logger_wrapper
def __castle_columns(matrix: list[list[str]], castling: Literal['short', 'long']) -> list[list[str]]:
    row = matrix[0]    
    n = 8  # chess board size 
    
    def castle(row: list[int]) -> list[int]:
        assert len(row) == n
        
        if castling == 'short':
            row[4], row[6] = row[6], row[4]  # swap king and knight        
            row[5], row[7] = row[7], row[5]  # swap rook and bishop
        elif castling == 'long':
            row[2], row[4] = row[4], row[2]  # swap king and bishop
            row[0], row[3] = row[3], row[0]  # swap rook and queen
        else:
            raise ValueError('Invalid castling')
        
        return row            
    
    if len(row) < n:
        return matrix
    
    # how many times we can castle
    castle_Count = (len(row) - n) + 1
    
    # hash table to store the column indecies
    col_indices = list(range(len(row)))
    for i in range(castle_Count):
        slice_ = slice(i, i + n)
        col_indices[slice_] = castle(col_indices[slice_])
        
    # swap the columns
    new_matrix = [
        [r[i] for i in col_indices]
        for r in matrix
    ]    
    
    return new_matrix
    
    
@logger_wrapper   
def __castle_rows(matrix: list[list[str]]) -> list[list[str]]:
    transposed = list(zip(*matrix))
    new_matrix = __castle_columns(transposed, 'long')
    
    return list(zip(*new_matrix))

    
@logger_wrapper
def __encrypt_lines(lines: Iterable[str]) -> list[str]:
    alphabet = list(ascii_lowercase + ' ')
    lines = [
        __ceaser_cipher_encrypt(line, 21115395998448816, alphabet)
        for line in lines
    ]
    return lines


def __ceaser_cipher_encrypt(text: str, k: int, alphabet: list[str]) -> str:
    alphabet_dict = {char: i for i, char in enumerate(alphabet)}

    # helper function to encrypt a single character
    def encrypt_char(char: str) -> str:
        if char in alphabet_dict:
            return alphabet[(alphabet_dict[char] + k) % len(alphabet)]
        return char

    return ''.join( 
        encrypt_char(char)
        for char in text
    )
    