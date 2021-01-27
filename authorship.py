import os, pyspark
os.environ['HADOOP_HOME'] = "C:\\winutils"
sc = pyspark.SparkContext('local[*]')

import math
import pickle
import statistics
from timeit import default_timer as timer

# %% Attributi sull'intero testo
def word_counter(RDD):
    '''
    Data una RDD, conta quante volte compare ogni parola ritornando anche la dimensione del vocabolario.
    
    Parameters
    ----------
    RDD : RDD
        RDD del file in input

    Returns
    -------
    (RDD, int)
        RDD dell'output del word count e dimensione del vocabolario
    '''
    
    word_counter = (RDD.flatMap(lambda x: x)
                    .map(lambda x: (x,1))
                    .reduceByKey(lambda a,b: a+b)
                    .sortBy(lambda x: -x[1])
                   )
    
    return word_counter, word_counter.count()

def text_length_in_words(RDD_word_counter):
    '''
    Calcola la lunghezza del testo in termini di numero di parole.
    
    Parameters
    ----------
    RDD_word_counter : RDD
        RDD dell'output del word count

    Returns
    -------
    int
        numero di parole totali presenti nel testo
    '''

    return (RDD_word_counter.map(lambda x: x[1])
            .reduce(lambda a,b: a+b)
           )

def entropy(RDD_word_counter, text_len):
    '''
    Calcola l'entropia (numero medio di bit richiesti per rappresentare tutte le parole del testo).
    
    Parameters
    ----------
    RDD_word_counter : RDD
        RDD dell'output del word count
    text_len : int
        numero di parole totali presenti nel testo

    Returns
    -------
    float
        valore dell'entropia
    '''
    
    return -(RDD_word_counter.map(lambda x: (x[1]/text_len) * math.log2(x[1]/text_len))
             .reduce(lambda a,b: a+b)
            ) # l'entropia ha segno negativo

# %% Attributi sulle frasi
def sentence_lengths(RDD):
    '''
    Calcola le lunghezze (in termini di numero di parole) di tutte le frasi di un testo.
    
    Parameters
    ----------
    RDD : RDD
        RDD del file in input

    Returns
    -------
    RDD
        RDD che contiene le lunghezze delle frasi
    '''
    
    # operazioni preliminari sul testo
    text = RDD.flatMap(lambda x: x).reduce(lambda a,b: a + ' ' + b) # metto tutto il testo in una stringa unica
    text = text.replace("?", ".") # ? termina una frase
    text = text.replace("!", ".") # ! termina una frase
    text = text.split('. ') # splitto quando trovo un carattere che termina una frase (. seguito da uno spazio)
    
    return (sc.parallelize(text)
            .map(lambda x: len(x.split(' ')))
           ) # per ogni frase trovata conto le sue parole

def prob_distr_of_sentence_length(RDD_sen_len):
    '''
    Ritorna una lista che contiene la distribuzione di probabilità delle lunghezze delle frasi.
    
    Parameters
    ----------
    RDD_sen_len : RDD
        RDD dell'output di sentence_lengths

    Returns
    -------
    list
        distribuzione di probabilità delle lunghezze delle frasi
    '''
    
    tot = RDD_sen_len.count()

    return (RDD_sen_len.map(lambda x: (x,1))
            .reduceByKey(lambda a,b: a+b)
            .map(lambda x: (x[0], x[1]/tot))
            .sortBy(lambda x: -x[1])
           )

# %% Attributi sulla probabilità delle parole
def prob_distr_of_most_common_words(RDD_word_counter, text_len):
    '''
    Ritorna la distribuzione di probabilità delle parole più comuni.
    
    Parameters
    ----------
    RDD_word_counter : RDD
        RDD dell'output del word count
    text_len : int
        numero di parole totali presenti nel testo

    Returns
    -------
    RDD
        RDD che contiene la distribuzione di probabilità
    '''
    
    return RDD_word_counter.map(lambda x: (x[0], x[1]/text_len))

def prob_of_the_most_common_word(RDD_prob_distr_of_MCWs):
    '''
    Ritorna la probabilità della parola più comune (escludendo 'and' e 'the').
    
    Parameters
    ----------
    RDD_prob_distr_of_MCWs : RDD
        RDD con la distribuzione di probabilità
    
    Returns
    -------
    tuple
        MCW e relativa probabilità
    '''
    
    return (RDD_prob_distr_of_MCWs
            .filter(lambda x: x[0] != "and" and x[0] != "the")
            .take(1)
           )[0]

def prob_of_the_most_common_word_x(RDD_prob_distr_of_MCWs):
    '''
    Ritorna la probabilità della parola più comune (escludendo articoli e preposizioni).
    
    Parameters
    ----------
    RDD_prob_distr_of_MCWs : RDD
        RDD con la distribuzione di probabilità
    
    Returns
    -------
    tuple
        MCWx e relativa probabilità
    '''
    
    prep_art = open("preposizioni_e_articoli.txt").read().splitlines()
    
    return (RDD_prob_distr_of_MCWs
            .filter(lambda x: x[0] not in prep_art)
            .take(1)
           )[0]

def prob_of_The(RDD_prob_distr_of_MCWs):
    '''
    Ritorna la probabilità della parola "the".
    
    Parameters
    ----------
    RDD_prob_distr_of_MCWs : RDD
        RDD con la distribuzione di probabilità
    
    Returns
    -------
    RDD
        RDD che contiene la probabilità della parola "the"
    '''
    
    return (RDD_prob_distr_of_MCWs
            .filter(lambda x: x[0] == "the")
           )

def prob_of_comma(RDD_sentences_data, text_len):
    '''
    Ritorna la probabilità di presenza della virgola.
    
    Parameters
    ----------
    RDD_sentences_data : RDD
        RDD del file in input
    text_len : int
        numero di parole totali presenti nel testo

    Returns
    -------
    int
        probabilità di presenza della virgola
    '''
    
    return (RDD_sentences_data
            .flatMap(lambda x: x)
            .filter(lambda x: "," in x)
            .count()
           ) / text_len

# %% Attributi sulla distanza
def distance_consec_appear(RDD, word):
    '''
    Ritorna una lista che contiene le distanze tra apparenze consecutive di word.
    
    Parameters
    ----------
    RDD : RDD
        RDD del file in input
    word : str
        parola da trattare

    Returns
    -------
    list
        distanze tra apparenze consecutive di word
    '''
    
    if word == ',':
        vect_pos = (RDD.flatMap(lambda x:x)
                    .zipWithIndex()
                    .filter(lambda x: ',' in x[0])
                    .map(lambda x: x[1])
                    .collect()
                   )
    else:
        vect_pos = (RDD.flatMap(lambda x:x)
                    .zipWithIndex()
                    .filter(lambda x: x[0] == word)
                    .map(lambda x: x[1])
                    .collect()
                   )
    
    vect_dis = []
    
    for i in range(1, len(vect_pos)):
        vect_dis.append(vect_pos[i] - vect_pos[i-1])
    
    return vect_dis

# %% Funzioni di supporto
def remove_number_some_punctuation_marks(row):
    '''
    Rimuove i caratteri numerici e i caratteri " e -- dalla stringa e la trasforma in lower-case.

    Parameters
    ----------
    row : str
        riga del file in input

    Returns
    -------
    res : str
        riga senza --, ", e i numeri
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
    Rimuove i caratteri numerici e i segni di punteggiatura dalla stringa e la trasforma in lower-case.

    Parameters
    ----------
    row : str
        riga del file in input

    Returns
    -------
    res : str
        riga senza numeri e segni di punteggiatura
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
    Carica il contenuto di un file in una RDD (tralasciando numeri e segni di punteggiatura).
    
    Parameters
    ----------
    filepath : str
        path del file da caricare

    Returns 
    -------
    RDD
        RDD del contenuto del file
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
    Carica il contenuto di un file in una RDD (tralasciando i numeri e i caratteri " e --).
    
    Parameters
    ----------
    filepath : str
        path del file da caricare

    Returns 
    -------
    RDD
        RDD del contenuto del file
    '''
    
    # caricamento del dataset
    raw_text = sc.textFile(filepath)

    # rimuoviamo i numeri e i segni di punteggiatura
    
    return (raw_text.filter(bool)                    # rimuoviamo le stringhe vuote
        .map(remove_number_some_punctuation_marks)
        .map(lambda x : ' '.join(x.split()))        # rimuoviamo diversi spazi bianchi con uno
        .map(lambda row : row.split(" "))
       )

def getCollection(RDD):
    return RDD.collect()

def getValue(RDD):
    return RDD.collect()[0]

def mean_std_couple(_list, tot_el):
    for i in range(0, tot_el - len(_list)):
        _list.append(0)

    return (statistics.mean(_list), statistics.stdev(_list))

# %% Salvataggio degli attributi
def generate_metrics(file_in):
    '''
    Ritorna un dizionario contenente tutti gli attributi estratti da un testo.
    
    Parameters
    ----------
    file_in : str
        path del file da analizzare
    
    Returns
    -------
    dict
        dizionario degli attributi estratti
    '''
    
    res = {}
    
    # consideriamo il testo SENZA i segni di punteggiatura
    print("Caricamento del file in memoria ...", end=" ")
    data = load_file_without_punctuations_marks(file_in)
    data.persist()
    print("caricamento completato")

    # calcoliamo le prime metriche
    print("Calcolo delle prime metriche, attendere ...", end=" ")
    
    RDD_word_counter, vocabulary_size = word_counter(data)
    RDD_word_counter.persist()
    text_length = text_length_in_words(RDD_word_counter)
    entropy_value = entropy(RDD_word_counter, text_length)
    
    RDD_prob_distr_of_MCWs = prob_distr_of_most_common_words(RDD_word_counter, text_length)
    prob_the_most_common_word = prob_of_the_most_common_word(RDD_prob_distr_of_MCWs)
    prob_the_most_common_word_x = prob_of_the_most_common_word_x(RDD_prob_distr_of_MCWs)
    prob_the = prob_of_The(RDD_prob_distr_of_MCWs)

    MCW = prob_the_most_common_word[0]
    dist_consec_MCW = distance_consec_appear(data, MCW)
    
    MCWx = prob_the_most_common_word_x[0]
    dist_consec_MCWx = distance_consec_appear(data, MCWx)
    
    dist_consec_the = distance_consec_appear(data, 'the')
        
    print("calcolo completato")

    
    # consideriamo il testo CON i segni di punteggiatura
    print("Caricamento del file in memoria ...", end=" ")
    sentences_data = load_file_without_number(file_in)
    sentences_data.persist()
    print("caricamento completato")
    
    # calcoliamo altre metriche
    print("Calcolo di ulteriori metriche, attendere ...", end=" ")
    
    RDD_sen_lengths = sentence_lengths(sentences_data)
    RDD_sen_lengths.persist()

    sen_lengths = RDD_sen_lengths.collect()

    prob_distr_freq_sen = prob_distr_of_sentence_length(RDD_sen_lengths)
    
    p_comma = prob_of_comma(sentences_data, text_length)

    dist_consec_comma = distance_consec_appear(sentences_data, ',')
    
    print("calcolo completato")
    
    
    # popoliamo il dizionario
    
    # attributi sull'intero testo
    res['vocabulary_size'] = vocabulary_size
    res['text_length'] = text_length
    res['V_T'] = vocabulary_size/text_length
    res['entropy'] = entropy_value
    
    # attributi sulle frasi
    res['avg_sentence_len'] = sum(sen_lengths)/len(sen_lengths)
    res['max_sentence_len'] = max(sen_lengths)
    res['min_sentence_len'] = min(sen_lengths)
    res['prob_distr_freq_sen'] = getCollection(prob_distr_freq_sen)
    res['prob_most_freq_sen'] = getValue(prob_distr_freq_sen)[1]
    
    # attributi sulla probabilità delle parole
    res['prob_distr_of_30'] = RDD_prob_distr_of_MCWs.take(30)
    res['prob_of_the_most_common_word'] = prob_the_most_common_word[1]
    res['prob_of_the_most_common_word_x'] = prob_the_most_common_word_x[1]
    res['prob_of_the'] = getValue(prob_the)[1]
    res['prob_of_comma'] = p_comma
    
    # attributi sulla distanza
    res['avg_dist_consec_comma'] = sum(dist_consec_comma)/len(dist_consec_comma)
    res['min_dist_consec_comma'] = min(dist_consec_comma)
    res['max_dist_consec_comma'] = max(dist_consec_comma)
    
    res['avg_dist_consec_MCW'] = sum(dist_consec_MCW)/len(dist_consec_MCW)
    res['min_dist_consec_MCW'] = min(dist_consec_MCW)
    res['max_dist_consec_MCW'] = max(dist_consec_MCW)
    
    res['avg_dist_consec_MCWx'] = sum(dist_consec_MCWx)/len(dist_consec_MCWx)
    res['min_dist_consec_MCWx'] = min(dist_consec_MCWx)
    res['max_dist_consec_MCWx'] = max(dist_consec_MCWx)
    
    res['avg_dist_consec_the'] = sum(dist_consec_the)/len(dist_consec_the)
    res['min_dist_consec_the'] = min(dist_consec_the)
    res['max_dist_consec_the'] = max(dist_consec_the)
    
    return res
    
def save_metrics(file_in, file_out):
    '''
    Salva un dizionario in un file.
    
    Parameters
    ----------
    file_in : str
        path del file da analizzare
    file_out: str
        path del file in cui salvare la entry

    Returns
    -------
    None
    '''

    entry = generate_metrics(file_in)
    
    with open(file_out, 'ab') as fout:
        pickle.dump(entry, fout, pickle.HIGHEST_PROTOCOL)
    
    print("Salvataggio completato")

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
    
    analisi = load_metrics(author_name)
    res = {}
    
    # recupero gli attributi dai dizionari e li metto sotto la stessa chiave
    for diz in analisi:
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

# %% Main
if __name__ == "__main__":    
    path = os.path.abspath(os.path.join('./tests'))
    filelist = os.listdir(path)

    authors = []
    for file in filelist:
        author = file.split('___')[0]
        if author not in authors:
            authors.append(author)

    t = timer()
    for author in authors:
        for file in filelist:
            if author in file:
                save_metrics(path+'/'+file, 'author_metrics/'+author)
    print("TIME: \n{} minuti".format(round((timer() - t)/60, 4)))

    sc.stop()
