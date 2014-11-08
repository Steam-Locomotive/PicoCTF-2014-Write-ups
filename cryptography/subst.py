import re
from collections import Counter
import itertools
import enchant
from data import ctext, words

#code = {'c':'T', 'h':'E', 'r':'A', 'i':'R'}
#code = {'r': 'T', 'i':'H', 'h':'E'}
#code = {'r': 'T', 'i':'H', 'h':'E', 's':'H', 'w':'R'}
#code = {'r': 'T', 'i':'H', 'h':'E', 's':'H', 'w':'R', 'e':'A', 'q':'I'}
#code = {'r': 'T', 'i':'H', 'h':'E', 's':'H', 'w':'R', 'e':'A', 'q':'I', 'b': 'W'
#, 'c':'O', 'a': 'N'}
code = {'h':'E', 'r':'T', 'i': 'H', 'b':'W', 'e':'A', 'q':'I', 'k':'N', 'c':'O',
        'd':'K', 's':'V', 'w':'R', 'j':'U', 'x':'Z', 'z':'G', 'v':'B', 'a':'S',
        'f':'C', 'u':'L', 'l':'P', 't':'D', 'o':'F', 'g':'Y', 'n':'M', 'm':'J'}

def decode(word):
    decoded = ''
    for letter in word:
        try:
            decoded += code[letter]
        except KeyError:
            decoded += letter
    return decoded

ctext_words = filter(bool, re.split('\s', ctext))

max_gram = 15 # up to pentagram
n_grams = []
n_words = []
for i in range(1, max_gram + 1):
    # for i = 2, do bigrams (an, un, he, it)
    # for i = 3, do trigrams (the, her, its)
    a = Counter()
    for j in range(len(ctext) - i):
        gram = ctext[j:j + i]
        if ' ' in gram or '\n' in gram:
            continue # skip grams seperated by space
        a[gram] += 1
    n_grams.append(a)

    b = Counter()
    for word in ctext_words:
        if len(word) != i:
            continue
        b[word] += 1
    n_words.append(b)

starting_letters = Counter()
ending_letters = Counter()
for word in ctext_words:
    starting_letters[word[0]] += 1
    ending_letters[word[-1]] += 1

def table(counter, n=10):
    total = sum(counter.values())
    for word, freq in counter.most_common(n):
        print '{0: <10.1f}{1}'.format(float(freq) / total * 100, decode(word))

# for n_gram in n_grams:
#     for word, freq in n_gram.most_common(15):
#         print decode(word), freq

# sorted_words = []
# for i in range(max_gram):
#     sorted_words.append([])
# for word in words.split('\n'):
#     if "'" in word:
#         continue
#     try:
#         sorted_words[len(word) - 1].append(word)
#     except IndexError:
#         pass

# target = n_grams[-1].most_common(1)[0][0]
# for big_gram in sorted_words[max_gram - 1]:
#     code = dict(zip(target, big_gram))
#     print big_gram
#     #''.join(code[letter] for letter in target)
#     print code, len(code)
