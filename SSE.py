from cryptography.fernet import Fernet


class SSE:
    def __init__(self):
        self.key = self.generate_key()


    def generate_key(self):
        return Fernet(Fernet.generate_key())

    def encrypt(self, string):
        return self.key.encrypt(string.encode('utf-8'))

    def decrypt(self, encrypted_bytes):
        return self.key.decrypt(encrypted_bytes).decode()


def write_to_file(filepath, content):
    f = open(filepath, 'w')
    f.write(content)
    f.close()




if __name__ == '__main__':
    sse = SSE()
    print(sse.key, type(sse.key))

    my_str = 'Danes je lep dan. Jutri bo še lepši, če bo sonce že posijalo 222.'

    enc = sse.encrypt(my_str)
    print(enc, type(enc))

    dec = sse.decrypt(enc)
    print(dec, type(dec))

    write_to_file('../Server/myfile', dec)
