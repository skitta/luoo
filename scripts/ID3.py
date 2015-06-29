class Decoder():

    def __init__(self, filename):
        self.fd = open(filename)

    def __del__(self):
        self.fd.close()

    def header(self):
        length = 3
        self.fd.seek(128)
        header = self.fd.read(length)
        return header
