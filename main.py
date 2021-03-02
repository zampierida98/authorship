import math
import pickle
import statistics
import numpy as np

# importiamo il modulo authoriship.py
import authorship

def create_metrics_file(dir_generate_metrics):
    '''
    create_metrics_file è la funzione che data la directory genera le metriche
    per ogni libro all'interno della dir. Aggiunge poi tali valori nel file 
    dell'autore a cui appartiene il libro
    
    Parameters
    ----------
    dir_generate_metrics : string
        dir che contiene i file di autori noti

    Returns
    -------
    None.

    '''
    
    # dalla directory recuperiamo la lista di file
    path = os.path.abspath(os.path.join(dir_generate_metrics))
    filelist = os.listdir(path)

    # per ogni file recuperiamo gli autori che sono la sottostringa
    authors = []
    for file in filelist:
        author = file.split('___')[0]
        if author not in authors:
            authors.append(author)

    # per ogni autore poi prendiamo i suoi libri e li inseriamo nel file
    # che contiene tutti i valori dei suoi libri
    for author in authors:
        for file in filelist:
            if author in file:
                authorship.save_metrics(path + '/' + file, "./author_metrics/" + author)
    return None


def verify_author(metrics_dict, author_name):
    '''
    verify_author è la funzione che determina un punteggio, 
    a partire dalle metriche di un libro SCONOSCIUTO, calcolando la distanza
    dal valore medio di una data metrica (DI UNO SPECIFICO AUTORE) con il valore
    del libro SCONOSCIUTO.
    
    

    Parameters
    ----------
    metrics_dict : dict
        dizionario delle metriche del libro SCONOSCIUTO
    author_name : string
        nome dell'autore

    Returns
    -------
    TYPE
        float 

    '''
    
    
def verify_author(test_metrics, author_name):
    
    # inizializziamo score e total
    # score <= total (per ogni singolo momento)
    score = 0
    total = 0
    
    # calcoliamo la media e la deviazione standard delle metriche di ogni libro
    # di author_name
    author_metrics_var = authorship.author_metrics("./author_metrics/" + author_name)
    
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

if __name__ == "__main__":
    import os
    import sys
    import getopt

    # inizializziamo:
    # - la directory dei libri SCONOSCIUTI: dir_analize_files
    # - la directory dei libri con autore:  dir_generate_metrics
    
    dir_analize_files = './analize_files/'
    dir_generate_metrics = './test/'
    
    # try catch per gestire il getops
    try:
        # stabilisco i parametri in input richiesti eventualmente
        optlist, args = optlist, args = getopt.getopt(sys.argv[1:], 'g:f:')    
    
    # in caso in cui ci siano dei parametri DIVERSI da quelli opzionali
    # da errore
    except getopt.GetoptError:
        print('Uso\nmain.py -g <dir_for_generating_metrics> -d <dir_unknown_authors>')
        sys.exit(-1)
    
    # per ogni parametro riconosciuto richiamiamo le funzioni applicate alla
    # directory passata come parametro
    for opt in optlist:
        # qui andiamo a creare il file di metriche
        if "-g" == opt[0]:
            create_metrics_file(opt[1])
        # specifichiamo una dictory diversa da quella standard su cui analizzare
        # i file
        if "-d" == opt[0]:
            dir_analize_files = opt[1]
                
    
    # aggiungiamo gli autori che noi conosciamo
    authors = []
    for author in os.listdir('./author_metrics'):
        authors.append(author)
    
    # per ogni file da analizzare
    for file in os.listdir(dir_analize_files):        
        # genero le metriche del file sconosciuto
        test_metrics = authorship.generate_metrics(dir_analize_files + file)
        
        
        _max_response = 0
        _author_response = ""
        
        # per ogni autore calcolo lo score e mantengo informazione
        # solo dello score migliore e del corrispondente autore
        
        print("\n\nInizio processo di classificazione del libro", file)
        for author in authors:
            print("Sto calcolando rispetto all'auture:", author, "...", end=" ")
            percent_res = verify_author(test_metrics, author)
            
            # teniamo 3 cifre dopo la virgola
            percent_res = round(percent_res, 3)
            
            if _max_response < percent_res:
                _max_response = percent_res
                _author_response = author
            
            print("score:", percent_res, "%")
            
        print("Fine processo di classificazione")
        print("\nRisultato finale")
        # stampiamo a video l'informazione del possibile autore
        print("Il libro", file, "riteniamo sia dell'autore", _author_response, "con", _max_response ,"%")
        
        print("\n" + "#" * 75)
    
    authorship.sc.stop()