import math
import pickle
import statistics
import numpy as np

# importiamo il modulo authoriship.py
import authorship

def create_metrics_file():
    path = os.path.abspath(os.path.join('./tests'))
    filelist = os.listdir(path)

    authors = []
    for file in filelist:
        author = file.split('___')[0]
        if author not in authors:
            authors.append(author)

    for author in authors:
        for file in filelist:
            if author in file:
                authorship.save_metrics(path + '/' + file, "./author_metrics/" + author)
    return None

def verify_author(metrics_dict, author_name):
    score = 0
    total = 0
    
    author_metrics_var = authorship.author_metrics("./author_metrics/" + author_name)
    
    
    for key in test_metrics:
        if type(test_metrics[key]) != list:
            score += gaussian(test_metrics[key], author_metrics_var[key][0], author_metrics_var[key][1])
            total += 1
        else:
            pass
            for tup in test_metrics[key]:
                res_search = search_tuple(author_metrics_var[key], tup[0])
                
                if res_search != None:
                    score += gaussian(tup[1], res_search[1][0], res_search[1][1])
                    total += 1
                
                else:
                    # penalita' ?????
                    total += 1
    
    return score/total * 100

def gaussian(x, mu, sigma):
    if sigma != 0:
        return np.exp(-np.power((x - mu)/sigma, 2)/2)
    return 1 if x == mu else 0
    
def search_tuple(_list, value):
    for tup in _list:
        if tup[0] == value:
            return tup
    return None

if __name__ == "__main__":
    import os
    
    #create_metrics_file()
    
    
    authors = []
    for author in os.listdir('./author_metrics'):
        authors.append(author)
    
    
    for file in os.listdir('./analize_files'):
        print("\nGenero le metriche del testo", file)
        test_metrics = authorship.generate_metrics('./analize_files/' + file)
        
        _max_response = 0
        _author_response = ""
        
        for author in authors:
            print("Verifico se il testo può appartenere a", author)
            percent_res = verify_author(test_metrics, author)
            
            if _max_response < percent_res:
                _max_response = percent_res
                _author_response = author
            
            print(author, " con percentuale pari a", percent_res)
            
            
        print("Il libro", file, "riteniamo sia dell'autore", _author_response, "al", _max_response ,"%")
    
    
    authorship.sc.stop()