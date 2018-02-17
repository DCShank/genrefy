#!/usr/bin/env python3
from sys import argv


def main(args):
    with open(args[1]) as f, open(args[2]) as f2, open(args[3], 'w') as f3:
        labels_list = []
        i = 0
        for line in f2:
            title, text, genres = line.split('\t')
            labels_list.append(eval(genres))
        for line in f:
            outstr = ''
            labels = labels_list[i]
            outstr = line.strip()
            for label in labels:
                outstr += ' __label__'
                for word in label.split():
                    outstr += word + '_'
            outstr += '\n'
            f3.write(outstr)
            i += 1


if __name__ == '__main__':
    main(argv)
