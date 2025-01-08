
import CRAM

class CRAMCore():
    def __init__(self):
        self.version = 1
        self.header_size = 38
        self.index_size = 16
        self.packet_size = 8