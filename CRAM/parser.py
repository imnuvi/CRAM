import struct
import CRAM.core as core

class FileParser():
    def __init__(self, filepath):
        self.core = core.CRAMCore()
        self.filepath = filepath

    def parse(self, row_idx):
        # TO-DO: make it run for row as well as columns
        with open(self.filepath, 'rb') as f:
            # Read indices: seek to the end of header and read the index packet of the row id
            f.seek(self.core.header_size + row_idx * self.core.index_size)
            _, offset, nnz = struct.unpack('=iqi', f.read(self.core.index_size))

            # Read data: seek to the actual data offset location and read the data packet
            f.seek(offset)
            row_data = [struct.unpack('=if', f.read(self.core.packet_size)) for _ in range(nnz)]
        return row_data
    
    def parse_range(self, start, end):
        with open(self.filepath, 'rb') as f:
            # Read indices: seek to the end of header and read the index packet of the row id
            offsets_list = []
            for row_idx in range(start, end):
                f.seek(self.core.header_size + row_idx * self.core.index_size)
                _, offset, nnz = struct.unpack('=iqi', f.read(self.core.index_size))
                offsets_list.append((offset, nnz))

            # Read data: seek to the actual data offset location and read the data packet
            initial_offset = offsets_list[0][0]
            rows = []
            for offset, nnz in offsets_list:
                f.seek(offset)
                row_data = [struct.unpack('=if', f.read(self.core.packet_size)) for _ in range(nnz)]
                rows.append(row_data)
        return rows