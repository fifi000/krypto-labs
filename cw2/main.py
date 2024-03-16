import time
import timeit
import hashlib

from tqdm import tqdm
from tabulate import tabulate
import plotly.graph_objs as go


def test_all_algorithms(text: str) -> None:
    """
    Test all available hash algorithms from `hashlib` on the given text.
    Prints results in a table format.

    Args:
        text (str): The input text to be hashed.
    """
    def time_hashing(algorithm: str, bytes_: bytes) -> tuple[float, str]:
        # time the hashing of the bytes
        start = time.time()
        hasher = hashlib.new(algorithm, bytes_)
        hashing_time = time.time() - start
        
        try:
            hasher = hasher.hexdigest()
        except TypeError:   # some hash functions require a length argument
            hasher = hasher.hexdigest(length=20)
        
        return hashing_time, hasher
    
    # encode input text into bytes
    bytes_ = text.encode()

    # iterate through all available hash functions and time the hashing of given text
    table = [
        [algorithm, *time_hashing(algorithm, bytes_)]
        for algorithm in hashlib.algorithms_available
    ]

    # print the results in a table format
    print(tabulate(        
        table, 
        headers=['Algorithm', 'Time (s)', 'Hash'], 
        tablefmt='fancy_grid'
    ))


def hash_file(file_path: str, algorithm: str = 'sha256') -> str:
    """
    Calculate the hash value of a file using the specified algorithm.

    Args:
        file_path (str): The path to the file.
        algorithm (str, optional): The hashing algorithm to use. Defaults to 'sha256'.

    Returns:
        str: The hash value of the file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    with open(file_path, 'rb') as file:
        bytes = file.read()
        return hashlib.new(algorithm, bytes).hexdigest()
    

def plot_hashing_time(
        algorithms: list[str] = ['md5', 'sha1', 'sha256', 'sha512'],
        message_sizes: list[int] = [2**i for i in range(10, 27)]
    ) -> None:
    """
    Plots the time taken to hash a message (using `plotly`) of given size for different hashing algorithms.

    This function measures the time taken to hash a message of different sizes using
    various hashing algorithms (md5, sha1, sha256, sha512). It then plots the results
    on a graph, with message size on the x-axis and time taken on the y-axis.
    
    Args:
        algorithms (list[str], optional): The hashing algorithms to test. Defaults to ['md5', 'sha1', 'sha256', 'sha512'].
        message_sizes (list[int], optional): The sizes of the messages to test. Defaults to [2**i for i in range(10, 27)].
    """
    # helper function to measure the time of hashing a message of given size
    def measure_hashing_time(algorithm: str ='sha256', number_of_runs: int = 100) -> list[float]:
        return [
            timeit.timeit(
                lambda: hashlib.new(algorithm, ('a' * size).encode()).hexdigest(), 
                number=number_of_runs
            )
            for size in message_sizes            
        ]

    # measure the time of hashing a message of given size for each algorithm
    data = [
        go.Scatter(
            x=message_sizes, 
            y=measure_hashing_time(algorithm), 
            mode='lines+markers', 
            name=algorithm
        )
        for algorithm in tqdm(algorithms)
    ]

    # plot the results
    layout = go.Layout(
        title='Time of hashing a message of given size for each algorithm',
        xaxis=dict(title='Message size (bytes)'),
        yaxis=dict(title='Time (s)'),
        legend=dict(orientation='h')
    )

    fig = go.Figure(data=data, layout=layout)
    fig.show()


if __name__ == "__main__":    
    # 1. test all available hash functions
    text = input('Enter the text to hash: ')
    test_all_algorithms(text)

    # 2|3. hash the file
    file_path = input('Enter the path to the file to hash: ')
    print(f'Hash of the file: {hash_file(file_path)}')

    # 4. plot the time of hashing a message of given size for each algorithm
    plot_hashing_time()
