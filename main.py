import os, sys
from colorama import init
from termcolor import colored
init()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(colored("Usage: authorship.py [-t path | -f file]", 'red'))
    else:
        if sys.argv[1] == '-t':
            print(colored("MODULO SALVATAGGIO\n\n", 'green'))
            os.system('python authorship.py '+sys.argv[1]+' '+sys.argv[2])
            print(colored("FINE SALVATAGGIO", 'green'))
        if sys.argv[1] == '-f':
            print(colored("MODULO SALVATAGGIO\n\n", 'green'))
            os.system('python authorship.py '+sys.argv[1]+' '+sys.argv[2])
            print(colored("FINE SALVATAGGIO", 'green'))
            
            print(colored("MODULO ANALISI\n\n", 'green'))
            unknown_file = sys.argv[2].split('.')[0]
            os.system('python analysis.py '+unknown_file)
            print(colored("FINE ANALISI", 'green'))
        else:
            print("Usage: authorship.py [-t path | -f file]")
