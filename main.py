# -*- coding: utf-8 -*-

import os, sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: main.py [-t path | -f file]")
    else:
        if sys.argv[1] == '-t':
            print("MODULO SALVATAGGIO\n\n")
            path_authorship = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'authorship.py') # path assoluto del file authorship.py
            argument = os.path.abspath(sys.argv[2]) # path assoluto della directory passata come argomento
            os.system('spark-submit "'+path_authorship+'" '+sys.argv[1]+' "'+argument+'"')
            print("FINE SALVATAGGIO")
        elif sys.argv[1] == '-f':
            print("MODULO SALVATAGGIO\n\n")
            path_authorship = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'authorship.py') # path assoluto del file authorship.py
            argument = os.path.abspath(sys.argv[2]) # path assoluto del file passato come argomento
            os.system('spark-submit "'+path_authorship+'" '+sys.argv[1]+' "'+argument+'"')
            print("FINE SALVATAGGIO")
            
            print("MODULO ANALISI\n\n")
            path_analysis = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'analysis.py') # path assoluto del file analysis.py
            unknown_file = os.path.abspath(sys.argv[2].split('.')[0]) # path assoluto del file salvato
            os.system('spark-submit "'+path_analysis+'" "'+unknown_file+'"')
            print("FINE ANALISI")
            
            os.remove(unknown_file)
        else:
            print("Usage: main.py [-t path | -f file]")
