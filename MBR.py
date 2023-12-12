import sys
import json
from prettytable import PrettyTable

class MBR_Reader():
    def __init__(self, file):
        # Try Load binary file
        self.file = file
        try:
            with open(self.file, 'rb') as p_data:
                data = p_data.read(512)[446:]
            self.partition = [data[i:i+16] for i in range(0, 64, 16)]
        except FileNotFoundError:
            sys.exit(1)
        # Try load finger print file
        try:
            with open('assets/finger_prints/disk_type_fp.json') as fp_file:
                self.fp = json.load(fp_file)
        except FileNotFoundError:
            print(f'[-] File "{fp_file}" not found')
            sys.exit(1)

    def _boot_flag(self):
        return [hex(i[0]) for i in self.partition]
    
    def _csh_starting_addr(self):
        return [hex(int.from_bytes(i[1:4], 'little')) for i in self.partition]

    def _p_type(self):
        return [self.fp[hex(i[4])] for i in self.partition]

    def _csh_ending_addr(self):
        return [hex(int.from_bytes(i[5:8], 'little')) for i in self.partition]

    def _lba_starting_addr(self):
        return [hex(int.from_bytes(i[8:12], 'little') * 512) for i in self.partition]

    def _sector_nr(self):
        return [int.from_bytes(i[12:16], 'little') for i in self.partition]

    def _p_size(self):
        return [i * 512 for i in self._sector_nr()]

    def _p_size_gb(self):
        return [round(i/1073741824, 2) for i in self._p_size()]

    def output(self):
        table = PrettyTable()
        table.field_names = ['Boot Flag', 'CHS Starting Address', 'Partition Type', 'CHS Ending Address', 'LBA Starting Address', 'Sector Count', 'Partition Size', 'Partition Size (GB)']
        for BF, CHSS, PT, CHSE, LBA, SC, PS, PS_GB in zip(self._boot_flag(), self._csh_starting_addr(), self._p_type(), self._csh_ending_addr(), self._lba_starting_addr(), self._sector_nr(), self._p_size(), self._p_size_gb()):
            table.add_row([BF, CHSS, PT, CHSE, LBA, SC, PS, PS_GB])
        return table
