from collections import Counter

frequency = Counter()
with open('encrypted', 'r') as f:
    data = f.read()
    for ch in data:
        frequency[ch] += 1

c = frequency.most_common(10)[0][0]
m = ' '
print (repr(c) + ' decrypts to ' + repr(m))

def xor(input_data, key):
    result = ""
    for ch in input_data:
        result += chr(ord(ch) ^ ord(key))
    return result

k = xor(c, m)

print (xor(data, k))
