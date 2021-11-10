from MBR import MBR_Reader
from VBR import VBR_Reader
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', required=True,  dest='mode',   type=str,            help='Depending on the file type you can have 3 modes. MBR ,VBR or BOTH')
parser.add_argument('-f', required=True,  dest='file',   type=str,            help='Name of the file')
parser.add_argument('-o', required=False, dest='offset', type=int, default=0, help='Set the offset to read the VBR data from a physical image file, mode VBR.')
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
else:
    print(f'[-] Mode {args.mode} not defined. Use -h for more info.')
