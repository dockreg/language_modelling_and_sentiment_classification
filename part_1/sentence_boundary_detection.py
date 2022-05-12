#!/usr/bin/env python

import sys
import re

def main():
    with open('test.txt', 'r') as f:
        text = f.read()
        text = text.replace('\n', ' ')
        sentences = re.split(r"(?<!Miss\.|Prof\.|Cllr\.|Revd\.)(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z][a-z][a-z]\.)(?<=\.|\?|\!)\s", text)

    #write output to a file
    with open('output.txt', 'w') as g:
        for l in sentences:
            g.write(l.strip()+'\n')
    print('Test.txt has been processed and the sentences have been put line by line into output.txt')
        
if __name__ == '__main__':
    main()


