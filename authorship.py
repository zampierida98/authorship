import pyspark, os
sc = pyspark.SparkContext('local[*]')

'''
Definizione delle funzioni di supporto
'''
def remove_number(row):
    '''
    remove_number:   rimuove i caratteri numerici dalla stringa e la trasforma in lower-case
    '''
    lowercase = row.lower()
    res = ""
    
    for char in lowercase:
        if not ('0' <= char <= '9'):
            res += char

    return res

def remove_number_punctuation_marks(row):
    '''
    remove_number:   rimuove i caratteri numerici dalla stringa e i segni di punteggiatura 
                     e la trasforma in lower-case
    '''
    
    lowercase = row.lower()
    res = ""
    
    for char in lowercase:
        if 'a' <= char <= 'z' or char == ' ' or char == '-' or char == "'":
            res += char

    return res
	
	
'''
Definizione delle funzioni che calcolano le metriche per la Authorship Attribution
'''
def word_counter(RDD):
    '''
    word_counter:   è la funzione che dato un RDD conta il numero di volte che compare una parola.
                    Inoltre per risparmiare operazioni ritorna anche l'ATTRIBUTO VOCABULARY_SIZE
    '''
    word_counter = (RDD.flatMap(lambda x: x)
                .map(lambda x: (x,1))
                .reduceByKey(lambda a,b: a+b)
                .sortBy(lambda x: -x[1])
               )
    return word_counter.collect(), len(word_counter.collect())

def text_length_in_words(word_count):
    '''
    text_length_in_words:   calcola il numero di parole del testo usando word_counter
    '''
    s = 0
    for couple in word_count:
        s += couple[1]
    return s

def ratio_V_T(voc_size, text_len):
    '''
    ratio_V_T:   calcola il rapporto fra la dimensione del vocabolario e il numero totale di parole
                 nel testo
    '''
    return voc_size / text_len

def hentropy(word_count,text_len):
    import math
    '''
    hentropy:   funzione che calcola l'entropia usando l'Entropia di Gibbs. L'unica differenza
                è la mancanza della costante di Boltzmann
    '''
    s = 0
    
    for couple in word_count:
        s += (couple[1]/text_len) * math.log2(couple[1]/text_len)
    
    return -s

def maximum_sentence_length(sentence_collection):
    '''
    maximum_sentence_length:   funzione che calcola la lunghezza (in numero di parole) della frase
                               più lunga
    '''
    _max = float("-inf")
    
    for sentence in sentence_collection:
        if len(sentence) > _max:
            _max = len(sentence)
    return _max

def minimum_sentence_length(sentence_collection):
    '''
    minimum_sentence_length:   funzione che calcola la lunghezza (in numero di parole) della frase
                               più corta
    '''
    _min = float("inf")
    
    for sentence in sentence_collection:
        if len(sentence) < _min:
            _min = len(sentence)
    return _min

def average_sentence_length(sentence_collection):
    '''
    average_sentence_length:   funzione che calcola la lunghezza media(in numero di parole)
                               delle frasi del testo
    '''
    _sum = 0
    
    for sentence in sentence_collection:
        _sum += len(sentence)
    return _sum / len(sentence_collection)
	

'''
Funzione che lavora su un singolo file
'''
def main(file):
	rawData = sc.textFile(file)

	# RIMUOVIAMO NUMERI + SEGNI DI PUNTEGGIATURA
	data = (rawData.filter(bool)                    # rimuoviamo le stringhe vuote
			.map(remove_number_punctuation_marks)
			.map(lambda x : ' '.join(x.split()))    # rimuoviamo diversi spazi bianchi con uno
			.map(lambda row : row.split(" "))
		   )

	# POSIAMO I DATI NELLA CACHE
	data.persist()

	# word_counter, e ATTRIBUTO vocabulary_size
	word_count, voc_size = word_counter(data)

	# SOMMA LE FREQUENZE DENTRO word_count PER TROVARE L'ATTRIBUTO text_length_in_words
	text_len = text_length_in_words(word_count)

	# ATTRIBUTO definito rapporto vocabulary_size / text_length_in_words
	V_T = ratio_V_T(voc_size, text_len)

	# ENTROPIA misura formalmente la quantità di disordine
	print('\n\n\n'+file)
	print(hentropy(word_count,text_len))

	print(maximum_sentence_length(data.collect()))
	print(minimum_sentence_length(data.collect()))
	print(average_sentence_length(data.collect()))
	print('\n\n\n')



path = ("./datasets/") #meglio usare os (vedi ia)
filelist = os.listdir(path)
#print(filelist)
for file in filelist:
	main(path+file)
