# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:45:00 2020

Modulo per calcolare le varie metriche/attributi necessari
per stabilire se un testo è stato scritto da un autore

@author: michele
"""
import os, pyspark
os.environ['HADOOP_HOME'] = "C:\\winutils"
sc = pyspark.SparkContext('local[*]')

def word_counter(RDD):
    '''
    funzione che dato un RDD conta il numero di volte che compare una parola.
    Inoltre per risparmiare operazioni ritorna anche l'ATTRIBUTO VOCABULARY_SIZE
    
    Parameters
    ----------
    row : RDD
        RDD del file in input

    Returns
    -------
    res : (RDD, int)
        RDD del word_counter e la grandezza del vocabolario del testo (quante parole diverse)
    '''
    
    word_counter = (RDD.flatMap(lambda x: x)
                .map(lambda x: (x,1))
                .reduceByKey(lambda a,b: a+b)
                .sortBy(lambda x: -x[1])
               )
    return word_counter, len(word_counter.collect())

	
	
def text_length_in_words(RDD_word_counter):
    '''
    text_length_in_words:   calcola il numero di parole del testo usando word_counter
    '''
    
    # word_counter: [("word1", 100), ...]
    
    return (RDD_word_counter.map(lambda x: x[1])
                            .reduce(lambda a,b: a+b)
           )
		   
def remove_number_some_punctuation_marks(row):
    '''
    Rimuove i caratteri numerici e il carattere '"' e "--"
    dalla stringa e la trasforma in lower-case

    Parameters
    ----------
    row : string
        linea del file in input

    Returns
    -------
    res : string
        linea senza --, ", e i numeri

    '''
    lowercase = row.lower()
    lowercase = lowercase.replace("--", " ")
    
    res = ""
    
    for char in lowercase:
        if not ('0' <= char <= '9' or char == '"'):
            res += char

    return res

def remove_number_punctuation_marks(row):
    '''
    Rimuove i caratteri numerici dalla stringa e i segni di punteggiatura 
    e la trasforma in lower-case

    Parameters
    ----------
    row : string
        linea del file in input

    Returns
    -------
    res : string
        linea senza numeri e segni di punteggiatura

    '''
    
    lowercase = row.lower()
    lowercase = lowercase.replace("--", " ")
    
    res = ""
    
    for char in lowercase:
        if 'a' <= char <= 'z' or char == ' ' or char == '-' or char == "'":
            res += char

    return res

def load_file_without_punctuations_marks(filepath):
    '''
    Carichiamo il contenuto di un file in un RDD.
    La collezione ritornata sarà una lista di stringhe senza numeri e segni
    di punteggiatura.
    
    Parameters
    ----------
    filepath : string
        percorso del file da caricare

    Returns 
    -------
    RDD
        la collezione manipolabile

    '''
    # caricamento del dataset
    raw_text = sc.textFile(filepath)

    # rimuoviamo i numeri e i segni di punteggiatura
    
    return (raw_text.filter(bool)                    # rimuoviamo le stringhe vuote
        .map(remove_number_punctuation_marks)
        .map(lambda x : ' '.join(x.split()))        # rimuoviamo diversi spazi bianchi con uno
        .map(lambda row : row.split(" "))
       )

def load_file_without_number(filepath):
    '''
    Carichiamo il contenuto di un file in un RDD.
    La collezione ritornata sarà una lista di stringhe senza numeri
    e senza i caratteri " e --
    
    Parameters
    ----------
    filepath : string
        percorso del file da caricare

    Returns 
    -------
    RDD
        la collezione manipolabile

    '''
    # caricamento del dataset
    raw_text = sc.textFile(filepath)

    # rimuoviamo i numeri e i segni di punteggiatura
    
    return (raw_text.filter(bool)                    # rimuoviamo le stringhe vuote
        .map(remove_number_some_punctuation_marks)
        .map(lambda x : ' '.join(x.split()))        # rimuoviamo diversi spazi bianchi con uno
        .map(lambda row : row.split(" "))
       )

if __name__ == "__main__":
    print("Caricamento del file ... ", end=" ")
        
    data = load_file_without_punctuations_marks("datasets/Anthony Trollope___The O'Conors of Castle Conor from Tales from all Countries.txt")
    
    print("caricamento completato")
    print("data.take(5)", data.take(5))
        
    # POSIAMO I DATI NELLA CACHE
    data.persist()
    
    '''
    wc, l = word_counter(data)
    print(l, wc.take(5))
    tl = text_length_in_words(wc)
    print(tl)
    '''
    
    sc.stop()
    