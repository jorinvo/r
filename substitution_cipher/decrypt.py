'''
Break substitution ciphers

Is limited to text containing only characters from english alphabet
plus space and all words must exist in the supplied dictionary.

Requires a dictionary saved as words.txt.


Usage: python decrypt.py < encrypted.txt
'''
import fileinput
from itertools import permutations
from copy import copy
# Dictionary, has first 10k words sorted by frequency,
# followed by more than 200k alphabetically sorted words
# This is a combination of the Google 10000 words and the NLTK words corpus
english_dictionary = [line.rstrip('\n') for line in open('words.txt')]

frequencies = {
    ' ': 15,
    'e': 12.702,
    't': 9.056,
    'a': 8.167,
    'o': 7.507,
    'i': 6.966,
    'n': 6.749,
    's': 6.327,
    'h': 6.094,
    'r': 5.987,
    'd': 4.253,
    'l': 4.025,
    'c': 2.782,
    'u': 2.758,
    'm': 2.406,
    'w': 2.360,
    'f': 2.228,
    'g': 2.015,
    'y': 1.974,
    'p': 1.929,
    'b': 1.492,
    'v': 0.978,
    'k': 0.772,
    'j': 0.153,
    'x': 0.150,
    'q': 0.095,
    'z': 0.074,
}


def main():
    text, text_frequencies = text_with_frequencies(fileinput.input())
    text_key = [c for c, f in sort(text_frequencies)]
    english_key = [c for c, f in sort(frequencies)]
    variance = 2
    chars = 7
    possible_firsts = permutations(text_key[:chars+variance], chars)

    for i, firsts in enumerate(possible_firsts):
        if not i % 100:
            print('round', i)
        # Ignore permutations outside of variance
        if not all(in_variance(firsts, text_key, variance)):
            continue
        # First is space, try matching long words first
        # because they have less matches
        words = sorted(text.split(firsts[0]), key=len, reverse=True)
        # Recursively find substitutions that work for all words
        s = extend_subs(dict(zip(firsts, english_key)), words)
        if s:
            print('key:', s)
            print('text', ''.join(s[c] for c in text))
            return

    print('no key found. text might contain words that are not in dictionary.')
    print('also try higher variance value.')


def text_with_frequencies(lines):
    '''
    Takes a line generator and
    returns a tuple consiting of the whole text and its frequencies
    '''
    text = ''
    total = 0
    counts = dict.fromkeys(frequencies.keys(), 0)
    for line in fileinput.input():
        l = line.lower()
        text += l
        for c in l:
            if c != '\n':
                total += 1
                counts[c] += 1
    text_frequencies = {k: v / total * 100 for k, v in counts.items()}
    return text, text_frequencies


def extend_subs(subs, words):
    '''
    Recursive function to extend an existing dict of substitutions to
    the all substitutions to get valid english words for the given words
    '''
    word = words[0]
    pattern = [subs[c] if c in subs else None for c in word]
    # Find all words that match the patter
    matches = [e for e in english_dictionary if match_pattern(pattern, e)]
    # If matches are empty, the substitutions are wrong
    if not len(matches):
        return None
    # No more words left, the substitutions are correct
    left_words = words[1:]
    if not len(left_words):
        return subs
    # For debugging:
    print(word, pattern, len(matches), len(left_words))
    # Find matches of the left words for different possible substitutions
    for m in matches:
        new_subs = copy(subs)
        new_subs.update({c: m[i] for i, c in enumerate(word)})
        s = extend_subs(new_subs, left_words)
        if s:
            return s
    return None


def in_variance(a, b, variance):
    return (abs(b.index(c) - i) <= variance for i, c in enumerate(a))


def sort(x):
    return sorted(
        ((c, f) for c, f in x.items()),
        key=lambda x: x[1], reverse=True
    )


def match_pattern(pattern, word):
    if len(pattern) != len(word):
        return False
    for i, c in enumerate(pattern):
        if c and c != word[i]:
            return False
    return True


if __name__ == "__main__":
    main()