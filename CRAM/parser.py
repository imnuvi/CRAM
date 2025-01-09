import struct
import CRAM.core as core

class FileParser():
    def __init__(self, filepath):
        self.core = core.CRAMCore()
        self.filepath = filepath

    def parse(self, row_idx):
        '''
        Takes a row index and returns the data packets for those

        input:
        :param row_idx: row index
        :type row_idx: int

        output:
        :return: list of data packets for the specified rows
        :rtype: list<tuple<int, float>>
        '''
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
        '''
        Takes a range of rows and returns the data packets for those

        input:
        :param start: start of range
        :type start: int
        :param end: start of range
        :type end: int

        output:
        :return: list of data packets for the specified rows
        :rtype: list<list<tuple<int, float>>>
        '''
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

    def parse_index_list(self, index_list):
        '''
        Takes a list of row indices and returns the data packets for the specified rows

        input:
        :param index_list: list of row indices
        :type index_list: list<int>

        output:
        :return: list of data packets for the specified rows
        :rtype: list<list<tuple<int, float>>>
        '''
        with open(self.filepath, 'rb') as f:
            offsets_list = []
            for row_idx in index_list:
                f.seek(self.core.header_size + row_idx * self.core.index_size)
                _, offset, nnz = struct.unpack('=iqi', f.read(self.core.index_size))
                offsets_list.append((offset, nnz))

            # Read data: seek to the actual data offset location and read the data packet
            rows = []
            for offset, nnz in offsets_list:
                f.seek(offset)
                row_data = [struct.unpack('=if', f.read(self.core.packet_size)) for _ in range(nnz)]
                rows.append(row_data)
            return rows