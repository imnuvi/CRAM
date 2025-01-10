
import CRAM

class CRAMCore():
    def __init__(self):
        self.version = 1

        self.magic_number_size = 4
        self.version_size = 2
        self.row_count_size = 4
        self.column_count_size = 4
        self.nnz_size_count = 8
        self.index_offset_size = 8
        self.data_offset_size = 8

        self.header_size = 38
        self.index_size = 16
        self.packet_size = 8