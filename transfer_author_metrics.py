# -*- coding: utf-8 -*-
import os

if __name__ == "__main__":
    print("Processo di trasferimento della cartella author_metrics su HDFS ...", end=" ")
            
    path_author_metrics = \
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'author_metrics')
    
    os.system('hadoop fs -mkdir -p ' + path_author_metrics)
            
    file_list =  os.listdir(path_author_metrics)
            
    for i in range(0, len(file_list)):
        file_list[i] = '"' + path_author_metrics +'/' + file_list[i].replace(" ", "%20") + '"'
            
    string_files_argument = " ".join(file_list)         
    os.system('hadoop fs -put -f ' + string_files_argument + " " + path_author_metrics)
    
    print("operazione completata")    
