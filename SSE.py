from cryptography.fernet import Fernet

from Crypto.Cipher import DES3, AES

import pyDes




class SSE:
    def __init__(self):
        self.key = self.generate_key_2()


    def generate_key_2(self):
        return Fernet(Fernet.generate_key())

    def encrypt_2(self, string):
        return self.key.encrypt(string.encode('utf-8'))

    def decrypt_2(self, encrypted_bytes):
        return self.key.decrypt(encrypted_bytes).decode()


def write_to_file(filepath, content):
    f = open(filepath, 'w')
    f.write(content)
    f.close()

def write_to_bin_file(filepath, content):
    f = open(filepath, 'wb')
    f.write(content)
    f.close()

def read_file(filepath):
    with open(filepath) as f:
        content = f.readlines()
        return content

def read_bin_file(filepath):
    with open(filepath, "rb") as f:
        Bytes = []
        byte = f.read(1)
        Bytes.append(byte)
        while byte != b"":
            byte = f.read(1)
            Bytes.append(byte)
        return b''.join(Bytes)


def ByteToHex(byteStr):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    a = ''.join(["%02X " % ord(x) for x in byteStr]).strip()
    print(a)

    return [chr(int(num, 16)) for num in a.split(' ') if (num is not '78' and num is not '5C')]


def pad(data):
    length = 16 - (len(data) % 16)
    data += bytes([length]) * length
    return data


def unpad(data):
    return data[:-data[-1]]



if __name__ == '__main__':
    print('AES CBC')

    obj = AES.new(b'This is a key123This is a key123', AES.MODE_CBC, b'This is an IV456')
    message = "Anja je lepa punca.".encode('utf-8')
    message = pad(message)
    ciphertext = obj.encrypt(message)
    print(ciphertext)

    obj_test = AES.new(b'This is a key123This is a key123', AES.MODE_CBC, b'This is an IV456')
    message = "Anja je ".encode('utf-8')
    message = pad(message)
    ciphertext = obj_test.encrypt(message)
    print(ciphertext)

    obj_test_3 = AES.new(b'This is a key123This is a key123', AES.MODE_CBC, b'This is an IV456')
    message = "lepa punca.".encode('utf-8')
    message = pad(message)
    ciphertext = obj_test_3.encrypt(message)
    print(ciphertext)

    obj2 = AES.new(b'This is a key123This is a key123', AES.MODE_CBC, b'This is an IV456')
    dec = obj2.decrypt(ciphertext)
    dec = unpad(dec)
    print(dec.decode())



    '''
    sse = SSE()
    print(sse.key, type(sse.key))

    # my_str = 'Danes je lep dan. Jutri bo še lepši, če bo sonce že posijalo 222.'
    my_str = "Hello world!"

    enc = sse.encrypt_2(my_str)
    print(enc, type(enc))

    dec = sse.decrypt_2(enc)
    print(dec, type(dec))

    print('---------------------------------------------------------')

    enc_2 = sse.encrypt_2(my_str)
    print(enc_2, type(enc_2), enc_2.decode())

    dec_2 = sse.decrypt_2(enc_2)
    print(dec_2, type(dec_2))

    # write_to_file('../Server/myfile', dec)

    print('---------------------------------------------------------')
    print('---------------------------------------------------------')
    print('---------------------------------------------------------')

    key = b'123456789012345678901234'

    des = DES3.new(key, DES3.MODE_ECB)
    print(des)

    text = '12345678901234  '.encode('utf-8')

    text_11 = '        '.encode('utf-8')

    cipher_text = des.encrypt(text)
    print(cipher_text)

    print(des.decrypt(cipher_text).decode())

    cipher_text_22222 = des.encrypt(text)
    print(cipher_text_22222)

    cipher_text_33333 = des.encrypt(text)
    print(cipher_text_33333)

    print('---------------------------------------------------------')
    print('---------------------------------------------------------')
    print('---------------------------------------------------------')
    '''



    '''
    print('---------------------------------------------------------')
    print('---------------------------------------------------------')
    print('---------------------------------------------------------')

    data = "Please encrypt my data now now now  io".encode('utf-8')

    data_22 = "Please encrypt encryptčšžđ".encode('utf-8')

    # key = b"123456789012345678901234"
    # write_to_bin_file('../key', key)

    key = read_file('../key')
    key = str(key[0]).encode('utf-8')
    print(str(key[0]).encode('utf-8'))

    k = pyDes.triple_des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
    print(k)

    # d = k.encrypt(data)
    # print(type(d))
    # print("Encrypted: %r" % d)
    # print("Decrypted: %r" % k.decrypt(d).decode())

    from binascii import unhexlify

    d_22 = k.encrypt(data_22)

    # a = bytes(bytearray.fromhex(d_22))
    # b = unhexlify(d_22)
    # c = ByteToHex(str(d_22))

    print("Encrypted 2: %r" % d_22)

    # write_to_bin_file('../encrypted', d_22)

    enc_file = read_bin_file('../encrypted')
    print(enc_file)

    print("Decrypted 2: %r" % k.decrypt(enc_file).decode())


    # print("Decrypted 2: %r" % k.decrypt(d_22).decode())
    '''
