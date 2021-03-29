# -*- coding: utf-8 -*-

import os, sys, pyspark
import pickle
import statistics
import numpy as np

def verify_author(test_metrics, author_metrics_var):
    '''
    verify_author è la funzione che determina un punteggio, 
    a partire dalle metriche di un libro SCONOSCIUTO, calcolando la distanza
    dal valore medio di una data metrica (DI UNO SPECIFICO AUTORE) con il valore
    del libro SCONOSCIUTO.
    
    Parameters
    ----------
    metrics_dict : dict
        dizionario delle metriche del libro SCONOSCIUTO
    author_metrics_var : dict
        dizionario delle medie e dev standard per ogni attributo

    Returns
    -------
    TYPE
        float
    '''
    
    # inizializziamo score e total
    # score <= total (per ogni singolo momento)
    score = 0
    total = 0
    
    # calcoliamo la media e la deviazione standard delle metriche di ogni libro
    # di author_metrics_var 
    
    # per ogni singola metrica del libro SCONOSCIUTO
    for key in test_metrics:
        # se il tipo della metrica non è lista
        if type(test_metrics[key]) != list:
            # calcoliamo con gaussian un punteggio fra 0 e 1 da sommare a score
            score += gaussian(test_metrics[key], author_metrics_var[key][0], author_metrics_var[key][1])
            
            total += 1
        else:
            # abbiamo una lista di coppie tipo ("the", 100)
            for tup in test_metrics[key]:
                # res_search = None se non ci c'è il primo valore della metrica
                # res_search = (key,value) se key è presente dentro author_metrics_var[key]
                res_search = search_tuple(author_metrics_var[key], tup[0])
                
                # come sopra calcoliamo un punteggio che stabilisce la distanza
                # rispetto al valore medio
                if res_search != None:
                    score += gaussian(tup[1], res_search[1][0], res_search[1][1])
                    total += 1
                
                # se la key non è presente aumentiamo ugualmente total di 1
                # come penalità
                else:
                    total += 1
    
    return score/total * 100

def gaussian(x, mu, sigma):
    '''
    gaussian calcola la distanza di x
    rispetto al valore medio mu e a sigma

    Parameters
    ----------
    x : float
        valore su cui calolare la distanza
    mu : float
        valore medio della gaussiana
    sigma : float
        deviazione standard

    Returns
    -------
    float
        distanza dalla media

    '''
    # se la std non è 0 usiamo la formula standard
    if sigma != 0:
        return np.exp(-np.power((x - mu)/sigma, 2)/2)
    
    # se la std è 0 vuol dire che se x è uguale alla media allora è 0
    # perchè non ci sono altri valori amessi
    
    return 1 if x == mu else 0

def search_tuple(_list, value):
    '''
    search_tuple ricerca all'interno della lista di tuple _list se la chiave value
    è presente o meno.
    
    Parameters
    ----------
    _list : list
        lista di coppie (k,v)
    value : string
        chiave da ricercare
    Returns
    -------
    (k,v) se k == value
    None altrimenti
    '''    
    for tup in _list:
        if tup[0] == value:
            return tup
    return None

# Preparazione delle caratteristiche di stile complessive
def load_metrics(file_in):
    '''
    Carica i dizionari degli attributi presenti in un file.
    
    Parameters
    ----------
    file_in : str
        path del file da cui caricare

    Returns
    -------
    list
        lista di dizionari degli attributi
    '''

    res = []
    
    with open(file_in, "rb") as fin:
        while True:
            try:
                res.append(pickle.load(fin))
            except EOFError:
                break
                
    return res

def mean_std_couple(_list, tot_el):
    for i in range(0, tot_el - len(_list)):
        _list.append(0)

    return (statistics.mean(_list), statistics.stdev(_list))

def author_metrics(author_name):
    '''
    Calcola media e deviazione standard degli attributi (provenienti da vari testi) di un autore.
    
    Parameters
    ----------
    author_name : str
        nome del file contenente i dizionari degli attributi

    Returns
    -------
    dict
        dizionario con media e deviazione standard degli attributi
    '''
    
    diz_list = load_metrics(author_name)
    res = {}
    
    # recupero gli attributi dai dizionari e li metto sotto la stessa chiave
    for diz in diz_list:
        for key in diz:
            try:
                res[key] += [diz[key]]
            except:
                res[key] = [diz[key]]
    
    for key in res:
        if type(res[key][0]) != list:
            # se l'attributo NON è una lista, calcolo direttamente media e deviazione standard
            res[key] = (statistics.mean(res[key]), statistics.stdev(res[key]))
        else:
            # se l'attributo è una lista, calcolo direttamente media e deviazione standard
            tot_el = len(res[key])
            res[key] = (sc.parallelize(res[key])
                        .flatMap(lambda x: x)
                        .map(lambda x: (x[0], [x[1]]))
                        .reduceByKey(lambda a,b: a+b)
                        .map(lambda x: (x[0], mean_std_couple(x[1], tot_el)))
                        .collect()
                       )
    
    return res

# Main
if __name__ == "__main__":
    #os.environ['HADOOP_HOME'] = "C:\\winutils"
    sc = pyspark.SparkContext('local[*]')
    sc.setLogLevel("ERROR")
    
    # print di separazione del warning
    print("#" * os.get_terminal_size()[0] * 2)
    
    # authors è una lista di coppie della forma:
    # (nome_autore, dizionario_media_std_stilemi)
    dir_unknown_books = os.path.abspath(sys.argv[1])    
    author_metrics_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'author_metrics/')
    
    print("\nGenerazione per ogni autore delle medie e deviazioni standard...", end=" ")
    authors = []
    for author in os.listdir(author_metrics_dir):
        authors.append((author, author_metrics(author_metrics_dir + author)))
    
    print("completato")
    
    print("Caricamento dei libri nella struttura dati...",end=" ")
    # list_dict_unknown_books è una lista di coppie della forma:
    # (nome_libro, dizionario_stilemi_libro)
    
    list_dict_unknown_books =   (sc.parallelize(os.listdir(dir_unknown_books))
                                 .filter(lambda x: "." not in x)
                                 .map(lambda x: (x, dir_unknown_books + "/" + x))
                                 # genero le metriche del testo sconosciuto 
                                 # 1- file.split(".")[0] per recuperare le metriche
                                 # 2- Il secondo [0] perchè ritorna una lista con almeno un dizionario
                                 .map(lambda x: (x[0], load_metrics(x[1].split(".")[0])[0]))
                                 )
    print("completato")
    
    print("Inizio processo di classificazione dei libri...", end=" ")
    
    books_classification = (list_dict_unknown_books
         # eseguiamo il prodotto cartesiano con ogni autore su cui fare l'analisi
         # adesso abbiamo ((nome_libro, dizionario_stilemi_libro), autore)
         .cartesian(sc.parallelize(authors))
         
         # con questo map otteniamo una tupla di tre elementi:
         # (nome_libro, dizionario_stilemi_libro, nome_autore, dizionario_media_std_stilemi)
         .map(lambda x: (x[0][0], x[0][1], x[1][0], x[1][1]))
         
         # con questo map calcoliamo la probabiltà che il libro sia stato
         # prodotto da un determinato autore. Otteniamo la seguente tupla:
         # (nome_libro, autore, probabilità)
         .map(lambda x: (x[0], x[2], round(verify_author(x[1], x[3]), 3)))
         
         # creiamo adesso coppie per fare il group by key
         .map(lambda x: (x[0], x[1:]))
         .groupByKey()
         .mapValues(list)
         
         .collect()
         )
    
    print("completato")

    for book_class in books_classification:
        _max_response = 0
        _author_response = ""
        print("\nRisultati analisi del libro", book_class[0])
        
        for resp in book_class[1]:
            if _max_response < resp[1]:
                _max_response = resp[1]
                _author_response = resp[0]
            print("Autore:", resp[0], ",", "score:", resp[1], "%")
        
        # stampiamo a video l'informazione del possibile autore
        print("\nRisultato finale")
        print("Il libro", book_class[0], "riteniamo sia dell'autore", _author_response, "con", _max_response ,"%")
        
        print("\n" + "#" * os.get_terminal_size()[0])
    
    print("Fine processo di classificazione")
    
    '''
    for filename in os.listdir(dir_unknown_books):
        
        # saltiamo i file con le estensioni
        if "." in filename:
            continue
        
        # path completo dei libri
        file = dir_unknown_books + "/" + filename
        
        # genero le metriche del testo sconosciuto 
        # 1- file.split(".")[0] per recuperare le metriche
        # 2- Il secondo [0] perchè ritorna una lista con almeno un dizionario
        test_metrics = load_metrics(file.split(".")[0])[0]
    
        # per ogni autore calcolo lo score e mantengo l'informazione solo dello score migliore e del corrispondente autore
        _max_response = 0
        _author_response = ""
        
        print("\n\nInizio processo di classificazione del libro", filename)
        for author in authors:
            print("Sto calcolando rispetto all'autore:", author, "...", end=" ")
            percent_res = verify_author(test_metrics, author)
            
            # teniamo 3 cifre dopo la virgola
            percent_res = round(percent_res, 3)
            
            if _max_response < percent_res:
                _max_response = percent_res
                _author_response = author
            
            print("score:", percent_res, "%")

        # stampiamo a video l'informazione del possibile autore
        print("\nRisultato finale")
        print("Il libro", filename, "riteniamo sia dell'autore", _author_response, "con", _max_response ,"%")
        
        print("\n" + "#" * 150)
        
    print("Fine processo di classificazione")
    '''
    sc.stop()
