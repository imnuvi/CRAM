import numpy as np
from scipy.sparse import random, csr_matrix, coo_matrix
print('starting')

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

# Example Usage
rows, cols = 5, 5        # Size of the matrix
density = 0.3            # 30% of the elements will be non-zero
format = 'csr'           # Choose the format: 'csr', 'coo', or 'csc'
random_state = 42        # Set a seed for reproducibility (optional)

# Generate a random sparse matrix
sparse_matrix = generate_random_sparse_matrix(rows, cols, density, format, random_state)

# Print the matrix
print(f"Sparse matrix ({format.upper()} format):\n{sparse_matrix}\n")
print(f"Array representation:\n{sparse_matrix.toarray()}")
