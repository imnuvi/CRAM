import numpy as np
from scipy.sparse import random, csr_matrix, coo_matrix
import CRAM

def generate_random_sparse_matrix(rows, cols, density, format='csr', random_state=None):
    """
    Generate a random sparse matrix.

    Parameters:
        rows (int): Number of rows.
        cols (int): Number of columns.
        density (float): Fraction of non-zero elements (0 < density <= 1).
        format (str): The sparse format ('csr', 'coo', 'csc').
        random_state (int or None): Seed for reproducibility (optional).

    Returns:
        scipy.sparse.spmatrix: Sparse matrix in the specified format.
    """
    # Generate a random sparse matrix with specified density
    sparse_matrix = random(
        rows, cols, density=density, format=format, random_state=random_state,
        data_rvs=np.random.rand  # Random values for the non-zero elements
    )
    return sparse_matrix


def test_parse():
    testpath = '/tmp/'
    fullpath = testpath + 'test.cram'

    rows, cols = 8, 5        # Size of the matrix
    density = 0.3            # 30% of the elements will be non-zero
    format = 'coo'           # Choose the format: 'csr', 'coo', or 'csc'
    random_state = 42        # Set a seed for reproducibility (optional)

    sparse_matrix = generate_random_sparse_matrix(rows, cols, density, format, random_state)
    filewriter = CRAM.FileWriter(fullpath)
    print(filewriter.write(sparse_matrix))

    fileparser = CRAM.FileParser(fullpath)
    print(sparse_matrix)
    # test fileparser range fetch
    print("--------------------")
    print(fileparser.parse_headers())
    print("--------------------")
    # test fileparser row fetch
    for i in range(rows):
        print(fileparser.parse(i))
    print("--------------------")
    print(fileparser.parse_range(0, 5))
    print("--------------------")
    print(fileparser.parse_index_list([0,1,2,3,4]))
    print("--------------------")

test_parse()