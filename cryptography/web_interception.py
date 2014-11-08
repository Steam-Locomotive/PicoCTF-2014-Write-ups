from __future__ import print_function
import socket

alphabet = '''_abcdefghijklmnopqrstuvwxyz\n\rABCDEFGHIJKLMNOPQRSTUVWXYZ/.\t !"#$%&\'()*+,-0123456789:;<=>?@[\\]^`{|}~\x7f\x80\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'''

HOST = 'vuln2014.picoctf.com'
PORT = 65414

def send(string):
    assert len(string) < 4096 / 2
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.recv(4096)
    sock.sendall(string.encode('hex'))
    resp = sock.recv(4096).strip('\n').decode('hex')
    sock.close()
    return resp

target = ''
known = ''
#known = ' HTTP/1.1\r\nCookie: flag=congrats_on_your_first_ecb_decryption\r\n\x01'

print (known)
try:
    for i in range(len(known), 64): # 64 = length of secret
            # one iteration takes about 20 seconds
            if 0 <= i < 16:
                    target = send('A' * (11 + 15 - i))[16:32]
                    for test_char in alphabet:
                            resp = send('A' * (11 + 15 - i) + known + test_char)[16:32]
                            if resp == target:
                                    known += test_char
                                    print (known)
                                    break
                    else:
                        print ('no answer for', i)
            if 16 <= i < 32:
                    target = send('A' * (11 + 16 + 15 - i))[32:48]
                    for test_char in alphabet:
                            resp = send('A' * (11 + 16 + 15 - i) + known + test_char)[32:48]
                            if resp == target:
                                    known += test_char
                                    print (known)
                                    break
                    else:
                        print ('no answer for', i)
            if 32 <= i < 48:
                    target = send('A' * (11 + 16 + 16 + 15 - i))[48:64]
                    for test_char in alphabet:
                            resp = send('A' * (11 + 16 + 16 + 15 - i) + known + test_char)[48:64]
                            if resp == target:
                                    known += test_char
                                    print (known)
                                    break
                    else:
                        print ('no answer for', i)
            if 48 <= i < 64:
                    target = send('A' * (11 + 16 + 16 + 16 + 15 - i))[64:80]
                    for test_char in alphabet:
                            resp = send('A' * (11 + 16 + 16 + 16 + 15 - i) + known + test_char)[64:80]
                            if resp == target:
                                    known += test_char
                                    print (known)
                                    break
                    else:
                        print ('no answer for', i)
finally:
    print (repr(known))
