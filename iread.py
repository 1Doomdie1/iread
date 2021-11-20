from MBR import MBR_Reader
from VBR import VBR_Reader
from file_extract import file_ex
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', required=False, dest='mode',    type=str,            help='Depending on the file type you can have 3 modes. MBR ,VBR or BOTH.')
parser.add_argument('-f', required=False, dest='file',    type=str,            help='Name of the file.')
parser.add_argument('-e', required=False, dest='entries', type=str,            help='Lists the entries from RD.')
parser.add_argument('-o', required=False, dest='offset',  type=int, default=0, help='Set the offset to read the VBR data from a physical image file, mode VBR.')
args = parser.parse_args()

if args.mode == 'MBR':
    file_reader = MBR_Reader(args.file)
    print(file_reader.output())

elif args.mode == 'VBR':
    file_reader = VBR_Reader(args.file, args.offset)
    print(file_reader.output())

elif args.mode == 'BOTH':
    MBR = MBR_Reader(args.file)
    print(MBR.output())
    for LBA, TYPE in zip(MBR._lba_starting_addr(), MBR._p_type()):
        if TYPE != 'FAT 32' or TYPE != 'FAT 16':
            if LBA != '0x0':
                VBR = VBR_Reader(args.file, int(LBA, 16))
                print(VBR.output())
elif args.entries:
    MBR = MBR_Reader(args.entries)
    for VBR_offset in MBR._lba_starting_addr():
        if VBR_offset != '0x0':
            VBR = VBR_Reader(args.entries, int(VBR_offset, 16))
            file_ex(args.entries, int(VBR._root_addr(), 16), VBR._root_dr_sz()).output()
else:
    print(f'[-] Mode {args.mode} not defined. Use -h for more info.')
