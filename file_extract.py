import json


class file_ex():
    def __init__(self, file, offset=0, size=16384):
        self.size = size
        self.letters = [i for i in range(32, 127)]
        with open(file, 'rb') as bin_file:
            bin_file.seek(offset)
            self.data = bin_file.read(self.size)
        with open('assets/finger_prints/file_type.json') as file:
            self.file_type = json.load(file)
        with open('assets/finger_prints/file_attribute.json') as file:
            self.file_attr = json.load(file)

    def entries(self):
        return [self.data[i:i+32] for i in range(0, self.size, 32) if self.data[i:i+32][0] != 0]

    def label(self):
        return ''.join([chr(i) for i in self.entries()[0][:12] if i in self.letters])

    def folders(self, d):
        try:
            if self.file_type[hex(d[11])] == 'Directory':
                return True
        except KeyError:
            return False

    def files(self, d):
        try:
            if self.file_type[hex(d[11])] == 'File':
                return True
        except KeyError:
            return False

    def f_attr(self, d):
        try:
            return self.file_attr[hex(d[0])]
        except KeyError:
            return 'r'

    def edit(self, name):
        x = ''
        for i in name[:12]:
            if i in self.letters:
                x += chr(i)
        return x.replace(' ', '').replace('~', '-').replace('JPG', '.JPG').replace('TMP', '.TMP').replace('TXT', '.TXT').lower()

    def output(self):
        ent = self.entries()
        print(f'Volume Label: {self.label()}')
        for i in ent:
            if self.files(i):
                print(f'f/{self.f_attr(i)}: {self.edit(i)}')
            elif self.folders(i):
                print(f'd/{self.f_attr(i)}: {self.edit(i)}')
