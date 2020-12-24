import pyspark
sc = pyspark.SparkContext('local[*]')

def remove_roman_numbers(row):
    res = row
    
    for n in roman_numbers:
        res = res.replace(n, " ")
    
    return res

def uniform_phrases(row):
    lowercase = row.lower()
    res = ""
    
    for char in lowercase:
        if 'a' <= char <= 'z' or char == ' ':
            res += char

    return res
	
# DICHIARAZIONE VARIABILI GLOBALI

roman_numbers = {"II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", 
                 "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"}

# CARICAMENTO DATASET

rawData = sc.textFile("datasets/Andrew Lang___A Short History of Scotland.txt")

# RIMOZIONE NUMERI ROMANI, NUMERI, SEGNI DI PUNTEGGIATURA + LOWERCASE

data = (rawData.map(remove_roman_numbers)
        .map(uniform_phrases)
        .map(lambda x : ' '.join(x.split()))    # rimuoviamo diversi spazi bianchi con uno
        .map(lambda row : row.split(" "))
       )

# POSIAMO I DATI NELLA CACHE

data.persist()

word_counter = (data.flatMap(lambda x: x)
                .map(lambda x: (x,1))
                .reduceByKey(lambda a,b: a+b)
                .sortBy(lambda x: -x[1])
               )
print('\n\n\n\n', word_counter.take(5))
