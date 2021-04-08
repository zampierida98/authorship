# -*- coding: utf-8 -*-

import os, sys
import getopt
import shutil

if __name__ == "__main__":
    
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "a:s:")
    
    except getopt.GetoptError:
        print('Uso: main.py -a <cartella_libri_da_analizzare> -s <cartella_libri_sconosciuti>')
        sys.exit(-1)
        
    if len(optlist) < 1:
        print('Uso: main.py -a <cartella_libri_da_analizzare> -s <cartella_libri_sconosciuti>')
        sys.exit(-1)

    for opt in optlist:
        if "-a" == opt[0]:
            print("Processo di creazione e salvataggio delle metriche di libri conosciuti")
            # print di separazione dei warning
            print("#" * shutil.get_terminal_size()[0] * 2)
            
            path_authorship = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'authorship.py') # path assoluto del file authorship.py
            argument = os.path.abspath(opt[1]) # path assoluto della directory passata come argomento
            os.system('spark-submit "' + path_authorship + '" -a "' + argument + '"')
            
            print("Fine processo di creazione e salvataggio delle metriche di libri conosciuti")
            
        if "-s" == opt[0]:
            dir_unknown_books = os.path.abspath(opt[1])
            
            print("Processo di generazione delle metriche di libri sconosciuti")
            # print di separazione dei warning
            print("#" * shutil.get_terminal_size()[0] * 2)
            
            path_authorship = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'authorship.py') # path assoluto del file authorship.py
            os.system('spark-submit "' + path_authorship + '" -s "' + dir_unknown_books +'"')
            
            print("Fine processo di generazione delle metriche di libri sconosciuti")                

            print("Processo di analisi dei testi sconosciuti")
            # print di separazione dei warning
            print("#" * shutil.get_terminal_size()[0] * 2)
            
            path_analysis = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'analysis.py') # path assoluto del file analysis.py
            os.system('spark-submit "' + path_analysis + '" "' + dir_unknown_books + '"')

            print("Fine processo di analisi dei testi sconosciuti")

            # rimozione dei file delle metriche
            for file in os.listdir(dir_unknown_books):
                if '.' in file:
                    continue
                
                os.remove(os.path.join(dir_unknown_books, file))
            