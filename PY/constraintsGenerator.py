import re
import random as rand
import time
import sys

rand.seed(time.time())
# Test it out
#N = int(input("What is the order of the whished NMR? "))
##if N < 3 :
##    N = 3
##    print("Wrong value (<3) : N = 3 by default")

N = 3


filename1 = sys.argv[1]                                                                                             # Fichier de contraintes sur les propriétés 
filename2 = sys.argv[2]                                                                                             # Fichier de contraintes sur le placement des PADs
filename3 = sys.argv[3]                                                                                             # Fichier de contraintes sur les timings

filename4 = sys.argv[4]                                                                                             # Nouveau fichier de contraintes sur les propriétés
filename5 = sys.argv[5]                                                                                             # Nouveau fichier de contraintes sur le placement des PADs
filename6 = sys.argv[6]                                                                                             # Nouveau fichier de contraintes sur les timings

filename10 = sys.argv[7]                                                                                            # Fichier contenant le pinout du FPGA choisi

clkKeyword = [r'CLK', r'Clock', r'inClock', r'C ']

try :                                                                                                               
    f10 = open(filename10, 'r')                                                                                     # On essaye d'ouvrir le fichier contenant le pinout du FPGA
    L = []                                                                                                          # On initialise une liste
    for count10, line10 in enumerate (f10) :                                                                        # On lit ligne à ligne la suite du fichier (à partir de la troisième ligne du coup)
        toto = line10.split()                                                                                       # On extrait les mots de la ligne
        if len(toto) > 1 :                                                                                          # Si la ligne contient plus d'un mot
            if toto[3] in str(15) and "IO" in toto[1]: #[12,13,14,15,16]                                            # On regarde s'il s'agit d'une IO et s'il appartient à une banque d'IO souhaitée
                L.append(toto[0])                                                                                   # On ajoute le nom du PAD associé à cette IO à la liste
    f10.close()                                                                                                     # On ferme le fichier du pinout
    print('PinOut read')                                                                                            # Message pour l'utilisateur
except FileNotFoundError :                                                                                          # Si le fichier n'est pas trouvé
    print(re.split(r"[\\]", filename10)[-1], "not found")                                                           # Message d'erreur associé
    exit(-1)                                                                                                        # On quitte le programme

try :
    f2 = open(filename2, 'r')                                                                                       # On essaye d'ouvrir le fichier de placement des PADs
    for count11, line11 in enumerate (f2) :                                                                         # On lit une à une les lignes du fichier
        if line11 != '\n' :                                                                                         # Si la ligne ne contient pas seulement un retour à la ligne 
            if ("#" in line11.split()[0]) :                                                                         # Si la ligne commence par un commentaire
                pass                                                                                                # On ne fait rien
            else :                                                                                                  # Sinon
                while line11.split()[2] in L :                                                                      # On récupère le nom du PAD utilisé et on vérifie s'il est dans la liste extraite précédemment
                    L.remove(line11.split()[2])                                                                     # On le supprime de la liste
    f2.close()                                                                                                      # On ferme le fichier
    print('List updated')                                                                                           # Message pour l'utilisateur
except FileNotFoundError :                                                                                          # Si le fichier n'est pas trouvé
    print(re.split(r"[\\]", filename2)[-1], "not found")                                                            # Message d'erreur associé

try :
    f1 = open(filename1, 'r')                                                                                       # On essaye d'ouvrir le fichier de contraintes sur les propriétés
    f4 = open(filename4, 'w')                                                                                       # On essaye d'ouvrir le nouveau fichier de contraintes sur les propriétés
    for count, line in enumerate(f1):                                                                               # On lit une à une les lignes du fichier de contraintes initial
        if line != '\n' :                                                                                           # Si la ligne ne contient pas seulement un retour à la ligne
            if ("#" in line.split()[0]) :                                                                           # Si la ligne commence par un commentaire
                pass                                                                                                # On ne fait rien
            else :                                                                                                  # Sinon
                f4.write(line)                                                                                      # On écrit la ligne courrante
                if '\n' not in line :                                                                               # Si cette ligne ne contient pas de retour à la ligne
                    f4.write('\n')                                                                                  # On ajoute un retour à la ligne
                if "get_ports" in line.lower() :                                                                    # Si la ligne contient le mot clé 'get_ports'
                        for k in range(N-1) :                                                                       # On va faire la redondance sur la ligne actuelle
                            dupliK = line.split()                                                                   # On extrait les mots de la ligne
                            dupliK4 = re.split(r"[\],}]", dupliK[4])                                                # On récupère le nom du signal à tripliquer (sans les accolades et les crochets)
                            dupliK[4] = ''.join(dupliK4) + "_NMR" + str(k+2)                                        # On lui ajoute la marque de redondance 
                            if '{' in dupliK[4] :                                                                   # S'il y a une accolade ouvrante
                                dupliK[4] += '}'                                                                    # On ajoute l'accolade fermante associée (supprimer précédemment pour ajouter la marque de redondance)
                            dupliK[4] += ']'                                                                        # On ajoute le crochet fermant (supprimer précédemment pour ajouter la marque de redondance)
                            dupliK = ' '.join(dupliK) + '\n'                                                        # On ré-assemble la ligne
                            f4.write(dupliK)                                                                        # On écrit la ligne
    f4.close()                                                                                                      # On ferme le fichier
    f1.close()                                                                                                      # On ferme le fichier
    print('Properties replicated')                                                                                  # Message pour l'utilisateur
except FileNotFoundError :                                                                                          # Si un des deux fichiers n'est pas trouvé
    print(re.split(r"[\\]", filename1)[-1], " or ", re.split(r"[\\]", filename4)[-1], "not found")                  # Message d'erreur associé

try :
    f2 = open(filename2, 'r')                                                                                       # On essaye d'ouvrir le fichier de contraintes sur le placement des PADs
    f5 = open(filename5, 'w')                                                                                       # On essaye d'ouvrir le nouveau fichier de contraintes sur le placement des PADs
    for count2, line2 in enumerate(f2):                                                                             # On lit une à une les lignes du fichier initial
        if line2 != '\n' :                                                                                          # Si cette ligne ne contient pas de retour à la ligne
            if ("#" in line2.split()[0]) :                                                                          # Si la ligne commence par un commentaire                                                                        
                pass                                                                                                # On ne fait rien
            else :                                                                                                  # Sinon
                f5.write(line2)                                                                                     # On écrit la ligne courrante
                if '\n' not in line2 :                                                                              # S'il n'y a de retour à la ligne
                    f5.write('\n')                                                                                  # On en ajoute un
                if "get_ports" in line2.lower() :                                                                   # Si on détecte le mot clé 'get_ports' dans la ligne
                    if any(ii in line2 for ii in clkKeyword) :
                        continue
                    else :
                        for k in range(N-1) :                                                                       # On va faire la redondance sur la ligne actuelle
                            dupliK = line2.split()                                                                  # On extrait les mots de la ligne
                            dupliK4 = re.split(r"[\],}]", dupliK[4])                                                # On récupère le nom du signal
                            hazard = rand.randint(0, len(L)-1)                                                      # On génère un nombre aléatoire dans une tranche voulue
                            dupliK[2] = L[hazard]                                                                   # On change le nom du PAD associé à partir d'un élément disponible dans le pinout, extrait auparavant
                            del L[hazard]                                                                           # On supprime cet élément
                            dupliK[4] = ''.join(dupliK4) + "_NMR" + str(k+2)                                        # On ajoute la marque de redondance au siganl
                            if '{' in dupliK[4] :                                                                   # S'il y a une accolade ouvrante dans le nom du signal
                                dupliK[4] += '}'                                                                    # On ajoute une accolade fermante, précédemment supprimée
                            dupliK[4] += ']'                                                                        # On ajoute un crochet fermant, précédemment supprimé
                            dupliK = ' '.join(dupliK) + '\n'                                                        # On ré-assemble la ligne modifiée
                            f5.write(dupliK)                                                                        # On écrit la ligne
    f5.close()                                                                                                      # On ferme le fichier
    f2.close()                                                                                                      # On ferme le fichier
    print('Pin mapping replicated')                                                                                 # Message pour l'utilisateur
except FileNotFoundError :                                                                                          # Si un des deux fichiers n'est pas trouvé
    print(re.split(r"[\\]", filename2)[-1], " or ", re.split(r"[\\]", filename5)[-1], "not found")                  # Message d'erreur associé

try :
    f3 = open(filename3, 'r')                                                                                       # On essaye d'ouvrir le fichier de contraintes sur le timing
    f6 = open(filename6, 'w')                                                                                       # On essaye d'ouvrir le nouveau fichier de contraintes sur le timing
    for count3, line3 in enumerate(f3):                                                                             # On lit une à une les lignes du fichier initial
        if line3 != '\n' :                                                                                          # Si la ligne ne contient pas seulement un retour à la ligne
            if ("#" in line3.split()[0]) :                                                                          # Si la ligne commence par un commentaire
                pass                                                                                                # On ne fait rien 
            else :                                                                                                  # Sinon
                f6.write(line3)                                                                                     # On écrit la ligne
                if '\n' not in line3 :                                                                              # Si la ligne ne contient pas de retour à la ligne
                    f6.write('\n')                                                                                  # On en ajoute un

                if "create_clock" in line3.lower() :                                                                # Si on détecte le mot clé 'create_clock' dans la ligne
                    for k in range(N-1) :                                                                           # On va faire la redondance sur la ligne courrante
                            dupliK = line3.split()                                                                  # On extrait les mots de la ligne
                            dupliK[4] += "_NMR" + str(k+2)                                                          # On récupère le nom du signal physique et on ajoute la marque de redondance
                            dupliKN = re.split(r"[\],}]", dupliK[-1])                                               # On extrait le nom du signal virtuel
                            dupliK[-1] = ''.join(dupliKN) + "_NMR" + str(k+2)                                       # On ajoute la marque de redondance
                            if '{' in dupliK[-1] :                                                                  # S'il y a une accolade ouvrante dans le nom du signal virtuel
                                dupliK[-1] += '}'                                                                   # On ajoute une accolade fermante, précédemmment supprimée
                            dupliK[-1] += ']'                                                                       # On ajoute un crochet fermant, précédemmment supprimé
                            dupliK = ' '.join(dupliK) + '\n'                                                        # On ré-assemble la ligne
                            f6.write(dupliK)                                                                        # On écrit la ligne
                elif "set_false_path" in line3.lower() :                                                            # Si on détecte le mot clé 'set_false_path' dans la ligne 
                    for k in range(N-1) :                                                                           # On va faire la redondance sur la ligne courrante
                            dupliK = line3.split()                                                                  # On extrait les mots de la ligne
                            dupliK3 = re.split(r"[\],}]", dupliK[3])                                                # On récupère le nom du signal
                            dupliK[3] = ''.join(dupliK3) + "_NMR" + str(k+2)                                        # On ajoute la marque de redondance
                            if '{' in dupliK[3] :                                                                   # S'il y a une accolade ouvrante dans le nom du signal extrait
                                dupliK[3] += '}'                                                                    # On ajoute une accolade fermante, précédemment supprimée
                            dupliK[3] += ']'                                                                        # On ajoute un crochet fermant, précédemment fermé
                            dupliK = ' '.join(dupliK) + '\n'                                                        # On ré-assemble la ligne
                            f6.write(dupliK)                                                                        # On écrit la ligne
    f6.close()                                                                                                      # On ferme le fichier
    f3.close()                                                                                                      # On ferme le fichier
    print('Timing replicated')                                                                                      # Message pour l'utilisateur
except FileNotFoundError :                                                                                          # Si un des deux fichier n'est pas trouvé
    print(re.split(r"[\\]", filename3)[-1], " or ", re.split(r"[\\]", filename5)[-1], "not found")                  # Message d'erreur associé

