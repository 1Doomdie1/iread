## Description

This script is designed to read data from physical or logical images of a disk. For now the script is built to read data from disks that are FAT 12, 16, 32.
The script will provide data regarding VBR and MBR.

MBR data:
Boot Flag, CHS Starting Address, Partition Type, CHS Ending Address, LBA Starting Address, Sector Count, Partition Size, Partition Size (GB)

VBR data:
BPS, Cluster Size, Reserve Size, Numbers of FATs, Root Max Entries, Root Size, FAT size, FAT1 address, FAT2 address, Root address

## Usage

- After cloning this you will need to install one more python package:

```bash
pip install prettytable
```

- Make sure you have a physical image or a logical image of a disk. You can obtain this by using FTKImager or any other Imaging forensics tool.
- If you have a physical image you can use this command to read the data from MBR:

```bash
py iread.py -m MBR -f file_name.001
```

- If you have a physical image you can use this command to read the data from MBR and VBR:

```bash
py iread.py -m BOTH -f file_name.001
```

- If you have a physical image and you want to read the VBR data ONLY, you will need to provide an offset. That offset will be provided by the LBA address. Convert that hex to decimal and pass it into this command:

```bash
py iread.py -m VBR -o 123456 -f file_name.001
```

- If you have a logical image you can use this command to read data from the VBR:

```bash
py iread.py -m VBR -f file_name.001
```

- You can read the entries from RD using this command:

```bash
py iread.py -e file_name.001
```

- You can see all the flags that you can pass by running:

```bash
py iread.py -h
```