import sys
from prettytable import PrettyTable

class VBR_Reader():
    def __init__(self, file, start=0):
        try:
            with open(file, 'rb') as bin_file:
                bin_file.seek(start)
                self.data = bin_file.read(512)
        except FileNotFoundError:
            print(f'[-] "{file}" not found!')

    def _BPS(self):
        return int.from_bytes(self.data[11:13], 'little')

    def _cluster_size(self):
        return self.data[13]

    def _size_of_reserve(self):
        return int.from_bytes(self.data[14:16], 'little')

    def _fat_cnt(self):
        return self.data[16]

    def _max_entries(self):
        return int.from_bytes(self.data[17:19], 'little')

    def _root_dr_sz(self):
        return self._max_entries() * 32

    def _fat_sizes(self):
        return int.from_bytes(self.data[22:24], 'little')

    def _fat1_addr(self):
        return hex(self._size_of_reserve() * self._BPS())

    def _fat2_addr(self):
        return hex((self._size_of_reserve() + self._fat_sizes()) * self._BPS())

    def _root_addr(self):
        return hex(((self._size_of_reserve() + self._fat_sizes() * self._fat_cnt())*self._BPS()))

    def _cl_2_addr(self):
        return hex(self._size_of_reserve() + (self._fat_sizes() * self._fat_cnt()) + self._root_dr_sz() )

    def output(self):
        table = PrettyTable()
        table.field_names = ['BPS', 'Cluster Size', 'Reserve Size', 'Numbers of FATs', 'Root Max Entries', 'Root Size', 'FAT size', 'FAT1 address', 'FAT2 address', 'Root address', 'Cluster 2 addr']
        table.add_row([self._BPS(), self._cluster_size(), self._size_of_reserve(), self._fat_cnt(), self._max_entries(), self._root_dr_sz(), self._fat_sizes(), self._fat1_addr(), self._fat2_addr(), self._root_addr(), self._cl_2_addr()])
        return(table)
