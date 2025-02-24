import struct
import CRAM.core as core

class FileParser():
    def __init__(self, filepath):
        self.core = core.CRAMCore()
        self.filepath = filepath
    
    def parse_headers(self):
        '''
        Reads the header contents of the CRAM file

        input: none

        implementation: The seeker acts as a incremental pointer calculating where to seek and reads the data bytes based on CRAM.core

        output:
        :return: Header packet for the file
        :rtype: dict<str, str>
        '''
        seeker = 0
        with open(self.filepath, 'rb') as f:
            # magic number
            seeker += 4
            f.seek(seeker)

            # version
            version_size = struct.calcsize('=h')
            version, = struct.unpack('=h', f.read(version_size))
            seeker += version_size
            f.seek(seeker)

            rcnn_pattern = '=iiq'
            rcnn_size = struct.calcsize(rcnn_pattern)
            rows, cols, nnz = struct.unpack(rcnn_pattern, f.read(rcnn_size))
            seeker += rcnn_size
            f.seek(seeker)

            header_dict = {
                "version" : version,
                "rows" : rows,
                "columns" : cols,
                "non_zero_count" : nnz,
            }
            return header_dict

            # struct.unpack('=qq', self.core.header_size, data_offset))

    def parse(self, row_idx):
        '''
        Takes a row index and returns the data packets for those

        implementation: seek to the end of the header and read the row index list collecting the offsets for the row
        seek to the data block and read data packets based on rows and packet sizes

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

        implementation: seek to the end of the header and read the row index list collecting the offsets for each row
        seek to the data block and read data packets based on rows and packet sizes

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

    def parse_index_list(self, index_list, split_lists=False):
        '''
        Takes a list of row indices and returns the data packets for the specified rows

        implementation: seek to the end of the header and read the row index list collecting the offsets for each row
        seek to the data block and read data packets based on rows and packet sizes

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
            if split_lists:
                cols = []
                values = []
            else:
                rows = []
            for offset, nnz in offsets_list:
                f.seek(offset)
                row_data = [struct.unpack('=if', f.read(self.core.packet_size)) for _ in range(nnz)]
                if split_lists:
                    ncols, nvalues = zip(*row_data)
                    cols.append(ncols)
                    values.append(nvalues)
                else:
                    rows.append(row_data)

            if split_lists:
                return index_list, cols, values
            else:
                return rows