# -*- coding: utf-8 -*-

import os, sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: main.py [-t path | -f file]")
    else:
        if sys.argv[1] == '-t':
            print("MODULO SALVATAGGIO\n\n")
            os.system('spark-submit authorship.py '+sys.argv[1]+' "'+sys.argv[2]+'"')
            print("FINE SALVATAGGIO")
        elif sys.argv[1] == '-f':
            print("MODULO SALVATAGGIO\n\n")
            os.system('spark-submit authorship.py '+sys.argv[1]+' "'+sys.argv[2]+'"')
            print("FINE SALVATAGGIO")
            
            print("MODULO ANALISI\n\n")
            unknown_file = sys.argv[2].split('.')[0]
            os.system('spark-submit analysis.py "'+unknown_file+'"')
            print("FINE ANALISI")
            
            os.remove(unknown_file)
        else:
            print("Usage: main.py [-t path | -f file]")
