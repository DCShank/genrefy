#!/usr/bin/env python3
from sys import argv
from nltk.tokenize import word_tokenize, sent_tokenize


def main(args):
    """ Parses a file to a format good for word embedding classification. """
    with open(args[1]) as inf, open(args[2], 'w') as outf:
        for line in inf:
            outstr = ''
            title, text, genres = line.split('\t')
            for sent in sent_tokenize(text):
                for word in (word_tokenize(sent)):
                    outstr += word + ' '
                outstr = outstr[:-2]
            outstr = outstr[:-1] + '\t' + genres
            outf.write(outstr)


if __name__ == '__main__':
    main(argv)
