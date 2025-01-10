
import struct
import CRAM.core as core

class FileWriter():
    '''
    File Writer class to write the sparse matrix into CRAM format
    input: scipy sparse matrix
    '''
    def __init__(self, filepath):
        self.filepath = filepath
        self.core = core.CRAMCore()

    def write(self, sparse_matrix):
        '''
        Reference for bytelength values : https://docs.python.org/3/library/struct.html#struct.pack
        '''

        # calculating data to be written
        from scipy.sparse import csr_matrix
        sparse_matrix = csr_matrix(sparse_matrix)
        rows, cols = sparse_matrix.shape
        nnz = sparse_matrix.nnz
        data_offset = self.core.header_size + ( rows * self.core.index_size ) 


        with open(self.filepath, 'wb') as f:
            # Headers
            f.write(b'CRAM')
            f.write(struct.pack('=h', self.core.version))
            f.write(struct.pack('=iiq', rows, cols, nnz))
            f.write(struct.pack('=qq', self.core.header_size, data_offset))

            # Index Section
            offset = data_offset
            for row_idx, start in enumerate(sparse_matrix.indptr[:-1]):
                end = sparse_matrix.indptr[row_idx + 1]
                nnz_in_row = end - start
                f.write(struct.pack('=iqi', row_idx, offset, nnz_in_row))
                offset += nnz_in_row * self.core.packet_size
            
            # Data Section
            for row_idx in range(rows):
                start = sparse_matrix.indptr[row_idx]
                end = sparse_matrix.indptr[row_idx + 1]
                for col, value in zip(sparse_matrix.indices[start:end], sparse_matrix.data[start:end]):
                    f.write(struct.pack('=if', col, value))
        return True