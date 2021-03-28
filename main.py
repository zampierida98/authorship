# -*- coding: utf-8 -*-

import os, sys
import getopt

if __name__ == "__main__":
    
    try:
        optlist, args = optlist, args = getopt.getopt(sys.argv[1:], "a:s:")
    
    except getopt.GetoptError:
        print('Uso: main.py -a <cartella_libri_da_analizzare> -s <cartella_libri_sconosciuti>')
        sys.exit(-1)

    for opt in optlist:
        if "-a" == opt[0]:
            print("Processo di creazione e salvataggio delle metriche di libri conosciuti")
            # print di separazione del warning
            print("#"*50, "Warning SPARK", end=" ")
            print("#"*350)
            
            path_authorship = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'authorship.py') # path assoluto del file authorship.py
            argument = os.path.abspath(opt[1]) # path assoluto della directory passata come argomento
            os.system('spark-submit "' + path_authorship + '" ' + "-a"  + ' "' + argument + '"')
            
            print("Fine processo di creazione e salvataggio delle metriche di libri conosciuti")
            
        if "-s" == opt[0]:
            '''
            print("Processo di generazione delle metriche di libri sconosciuti")
            # print di separazione del warning
            print("#"*50, "Warning SPARK", end=" ")
            print("#"*350)
            
            path_authorship = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'authorship.py') # path assoluto del file authorship.py
            dir_unknown_books = os.path.abspath(opt[1])
            
            for file in os.listdir(dir_unknown_books):
                file = dir_unknown_books + "/" + file
                os.system('spark-submit "' + path_authorship + '" ' + "-f" + ' "' + file +'"')
                
            print("Fine processo di generazione delle metriche di libri sconosciuti")
            '''
            
            dir_unknown_books = os.path.abspath(opt[1])
            
            print("Processo di analisi dei testi sconosciuti")
            # print di separazione del warning
            print("#"*50, "Warning SPARK", end=" ")
            print("#"*350)
            
            path_analysis = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'analysis.py') # path assoluto del file analysis.py
            os.system('spark-submit "' + path_analysis + '" "' + dir_unknown_books + '"')

            print("Fine processo di analisi dei testi sconosciuti")

            # rimozione delle metriche
            #for file in os.listdir(dir_unknown_books):
            #    os.remove((dir_unknown_books + "/" + file).split('.')[0])
'''
    
    if len(sys.argv) != 3:
        print("Usage: main.py [-t path | -f file]")
    else:
        if sys.argv[1] == '-t':
            print("MODULO SALVATAGGIO")
            # print di separazione del warning
            print("#"*50, "Warning SPARK", end=" ")
            print("#"*350)
            
            path_authorship = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'authorship.py') # path assoluto del file authorship.py
            argument = os.path.abspath(sys.argv[2]) # path assoluto della directory passata come argomento
            os.system('spark-submit "'+path_authorship+'" '+sys.argv[1]+' "'+argument+'"')
            print("FINE SALVATAGGIO")
        elif sys.argv[1] == '-f':
            print("MODULO SALVATAGGIO")
            # print di separazione del warning
            print("#"*50, "Warning SPARK", end=" ")
            print("#"*350)
            
            path_authorship = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'authorship.py') # path assoluto del file authorship.py
            argument = os.path.abspath(sys.argv[2]) # path assoluto del file passato come argomento
            os.system('spark-submit "'+path_authorship+'" '+sys.argv[1]+' "'+argument+'"')
            print("FINE SALVATAGGIO")
            
            print("MODULO ANALISI")
            # print di separazione del warning
            print("#"*50, "Warning SPARK", end=" ")
            print("#"*350)
            
            path_analysis = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'analysis.py') # path assoluto del file analysis.py
            unknown_file = os.path.abspath(sys.argv[2].split('.')[0]) # path assoluto del file salvato
            os.system('spark-submit "'+path_analysis+'" "'+unknown_file+'"')
            print("FINE ANALISI")
            
            os.remove(unknown_file)
        else:
            print("Usage: main.py [-t path | -f file]")

'''
