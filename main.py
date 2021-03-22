#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: main.py [-t path | -f file]")
    else:
        if sys.argv[1] == '-t':
            print("MODULO SALVATAGGIO\n\n")
            os.system('python authorship.py '+sys.argv[1]+' '+sys.argv[2])
            print("FINE SALVATAGGIO")
        if sys.argv[1] == '-f':
            print("MODULO SALVATAGGIO\n\n")
            os.system('python authorship.py '+sys.argv[1]+' '+sys.argv[2])
            print("FINE SALVATAGGIO")
            
            print(("MODULO ANALISI\n\n")
            unknown_file = sys.argv[2].split('.')[0]
            os.system('python analysis.py '+unknown_file)
            print("FINE ANALISI")
        else:
            print("Usage: main.py [-t path | -f file]")
