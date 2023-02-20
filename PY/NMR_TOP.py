
import re                                                                                                                       # Module Regular Expression
import subprocess                                                                                                               # Module pour utiliser l'INVITE DE COMMANDE
import time                                                                                                                     # Module TIME
import sys

# Test it out
#N = int(input("What is the order of the whished NMR? "))
#if N < 3 :
#	N = 3
#	print("Wrong value (<3) : N = 3 by default")

N = 3                                                                                                                           # Niveau de redondance

#------------------------------------------------
#		File Name Statement		|
#------------------------------------------------
netlist_name  	= sys.argv[1]                                                                                                   # Chemin de la netlist initiale                                                                                     
netlist_NMR_name= sys.argv[2]                                                                                                   # Chemin de la netlist post réplication

#------------------------------------------------
#		File Gestion			|
#------------------------------------------------
f0 = open(netlist_name,     'r')                                                                                                # Ouverture de la netlist initiale en mode lecture
f1 = open(netlist_NMR_name, 'w')                                                                                                # Ouverture de la netlist post réplication en mode écriture

#----------------------------------------
#		Fonctions		|
#----------------------------------------

def parenthesis_counter(l, paren) :                                                                                             # Compteur de paranthèses à partir d'une ligne et d'une valeur initiale du compteur
        if '(' in l :                                                                                                           # Si détection d'au moins 1 caractère ( dans la ligne
                paren += len(re.findall('\(', l))                                                                               # Ajout du nombre exact de caractère ( détécté
        if ')' in l :                                                                                                           # Si détection d'au moins 1 caractère ) dans la ligne
                paren -= len(re.findall('\)', l))                                                                               # Retrait du nombre exact de caractère ) détécté
        return paren                                                                                                            # Renvoie le nombre de paranthèses                                                                                       


def redundancy_fct(string, index_name, i_NMR) :                                                                                 # Duplication d'une partie d'une chaine de caractères 
	x = string.split()                                                                                                          # Séparation de la chaine de caractères dans une liste 
	x_temp = re.split(r'\W+', x[index_name])                                                                                    # Retrait des caractères non alphanumérique du morceau 
	x_NMR_before = re.split(r'_', x_temp[0])
	if "inst" in x_NMR_before[-1] :                                                                                                 
		x_NMR_before[-1] = "NMR" + str(i_NMR) + "_inst"
	elif "IBUF" in x_NMR_before[-1] :
		x_NMR_before[-1] = "NMR" + str(i_NMR) + "_IBUF"
	elif "OBUF" in x_NMR_before[-1] :
		x_NMR_before[-1] = "NMR" + str(i_NMR) + "_OBUF"
	elif "BUFG" in x_NMR_before[-1] :
		x_NMR_before[-1] = "NMR" + str(i_NMR) + "_BUFG"

	x_temp[0] = '_'.join(x_NMR_before)
	par_temp = re.split(r'\w+', x[index_name])

	if "inst" not in string and "IBUF" not in string and "OBUF" not in string and "BUFG" not in string:
		x_temp[0] = x_temp[0] + "_NMR" + str(i_NMR) + par_temp[len(par_temp)-1]
	else :
		x_temp[0] = x_temp[0] + par_temp[len(par_temp)-1]
	x_temp = ' '.join(x_temp)
	x[index_name] = x_temp
	x = "\t" + ' '.join(x) + '\n'
	return x

def cell_top (l, i_NMR) :
        redundancy = ''
        index = []
        x = l.split()
        #Port Name Modification
        if "port " in l.lower() :
                if "array " in l.lower() :
                        x[3] += "_NMR" + str(i_NMR)
                        renameSplit = re.split(r"\",[ ,]", x[4])
                        string = ""
                        for char in x[4] :
                            if char == '[' :
                                string += '_NMR' + str(i_NMR)
                            string += char
                        x[4] = string
                else :
                        x[1] += "_NMR" + str(i_NMR)
        #Instance Name Modification
        if "instance " in l.lower() :
                if "rename " in l.lower() :
                        x_temp = re.split('_', x[2])
                else :
                        x_temp = re.split('_', x[1])
                if any(ii in keyword for ii in x_temp) :
                        for jj in range(len(keyword)) :
                                try :
                                        index.append(x_temp.index(keyword[jj]))
                                except ValueError :
                                        continue
                        idx = min(index)
                        x_temp.insert(idx, 'NMR' + str(i_NMR))
                else :
                        x_temp.append('NMR' + str(i_NMR))

                if "rename " in l.lower() :
                        x[2] = '_'.join(x_temp)
                        renameSplit = re.split(r"\",[ ,]", x[3])
                        string = ""
                        for char in x[3] :
                            if char == '[' :
                                string += '_NMR' + str(i_NMR)
                            string += char
                        x[3] = string
                else :
                        x[1] = '_'.join(x_temp)
        #Net Name Modification
        if "net " in l.lower() : 
                if "rename " in l.lower() :
                        x_temp = re.split('_', x[2])
                else :
                        x_temp = re.split('_', x[1])
                        
                if any(ii in keyword for ii in x_temp) :
                        for jj in range(len(keyword)) :
                                try :
                                        index.append(x_temp.index(keyword[jj]))
                                except ValueError :
                                        continue
                        idx = min(index)
                        x_temp.insert(idx, 'NMR' + str(i_NMR))
                        if "rename " in l.lower() :
                                x_temp2 = re.split('_', x[3])
                                x_temp2.insert(idx, 'NMR' + str(i_NMR))
                                x[3] = '_'.join(x_temp2)
                else :
                        if "rename " in l.lower() :
                                x_temp.insert(-2, 'NMR' + str(i_NMR))
                                string = ""
                                for char in x[3] :
                                        if char == '[' :
                                                string += '_NMR' + str(i_NMR)
                                        string += char
                                x[3] = string
                        else :
                                x_temp.append('NMR' + str(i_NMR))

                if "rename " in l.lower() :
                        x[2] = '_'.join(x_temp)
                else :
                        x[1] = '_'.join(x_temp)
        #Instanceref Name Modification
        if "portref " in l.lower() and "instanceref " in l.lower() :
                if "member" in l.lower() :
                        x_temp = re.split('_', x[-1])
                else :
                        x_temp = re.split('_', x[3])

                
                if any(ii in keyword for ii in x_temp) :
                        for jj in range(len(keyword)) :
                                try :
                                        index.append(x_temp.index(keyword[jj]))
                                except ValueError :
                                        continue
                        idx = min(index)
                        x_temp.insert(idx, 'NMR' + str(i_NMR))
                else :
                        if '))' in x_temp[0] :
                                x_temp[0] = x_temp[0].replace('))', '_NMR' + str(i_NMR) + '))')
                        else :
                                x_temp[0] += '_NMR' + str(i_NMR)
                
                if "member" in l.lower() :
                        x[-1] = '_'.join(x_temp)
                else :
                        x[3] = '_'.join(x_temp)
        #Portref Name Modification
        if "portref " in l.lower() and "instanceref " not in l.lower() :
                if "member" in l.lower() :
                        x_temp = re.split('_', x[2])
                else :
                        x_temp = re.split('_', x[1])
                
                if any(ii in x_temp for ii in keyword) :
                        for jj in range(len(keyword)) :
                                try :
                                        index.append(x_temp.index(keyword[jj]))
                                except ValueError :
                                        continue
                        idx = min(index)
                        x_temp.insert(idx, 'NMR' + str(i_NMR))
                else :
                        if ')' in x_temp[-1] :
                                x_temp[-1] = x_temp[0].replace(')', '_NMR' + str(i_NMR) + ')')
                        else :
                                x_temp[-1] += '_NMR' + str(i_NMR)

                if "member" in l.lower() :
                        x[2] = '_'.join(x_temp)
                else :
                        x[1] = '_'.join(x_temp)
        
        redundancy = '\t\t ' + ' '.join(x) 
        return redundancy

def writeVoterInstance(f, i) :
        f.write("         (instance VOTER_" + str(i) + " (viewref voter (cellref voter (libraryref work))))\n")
        return

def cell_rename(string, i_NMR) :
        if i_NMR == 1 :
                return string
        else :
                x_NMR_before = re.split(r'_', string)
                idx = []
                for bb in x_NMR_before :
                        for cc in keyword :
                                if cc in bb :
                                        idx.append(x_NMR_before.index(bb))
                                        NMRindex = min(idx)
                                else :
                                        NMRindex = -1
                
                if len(idx) > 0 :
                        NMRindex = min(idx)
                        
                if NMRindex > 0 :
                        x_NMR_before.insert(NMRindex, "NMR" + str(i_NMR))
                        string = '_'.join(x_NMR_before)
                else :
                        string += "_NMR" + str(i_NMR)
                return string

def writeVoterLink(f, net1, net2, cell1, cell2, i, ii_voter, nb) :
        toWrite = ""
        if net1 == "" :
                net1 = "debugNET1_"
        if net2 == "" :
                net2 = "debugNET2_"

        if "OBUF".lower() in net1.lower() or "OBUF".lower() in net2.lower():
                for ii in range(1, N+1) :
                        toWrite += "         (net " + net2 + str(3*i+ii-1) + " (joined\n"
                        toWrite += "          (portref I (instanceref " + cell_rename(cell2,ii) + "))\n"
                        toWrite += "          (portref S (instanceref VOTER_" + str(3*i+ii-1) + "))\n"
                        toWrite += "          )\n"
                        toWrite += "         )\n"

                        if net1 in Arrays :
                                toWrite += "         (net sigVOTER_" + str(3*i+ii-1+ii_voter) + " (joined\n"                              
                                toWrite += "          (portref (member  " + net1 + " " + str(nb) + " ) (instanceref " + cell_rename(cell1,ii) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i+1) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i+2) + "))\n"
                                toWrite += "          )\n"
                                toWrite += "         )\n"
                        else :
                                toWrite += "         (net sigVOTER_" + str(3*i+ii-1+ii_voter) + " (joined\n"
                                toWrite += "          (portref " + net1 + " (instanceref " + cell_rename(cell1,ii) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i+1) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i+2) + "))\n"
                                toWrite += "          )\n"
                                toWrite += "         )\n"
                        
        else :
                for ii in range(1, N+1) :
                        if net1 in Arrays :
                                toWrite += "         (net sigVOTER_" + str(3*i+ii-1+ii_voter) + " (joined\n"                              
                                toWrite += "          (portref (member  " + net1 + str(nb) + " ) (instanceref " + cell_rename(cell1,ii) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i+1) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i+2) + "))\n"
                                toWrite += "          )\n"
                                toWrite += "         )\n"
                        else :       
                                toWrite += "         (net sigVOTER_" + str(3*i+ii-1+ii_voter) + " (joined\n"
                                toWrite += "          (portref " + net1 + " (instanceref " + cell_rename(cell1,ii) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i+1) + "))\n"
                                toWrite += "          (portref in" + str(ii) + " (instanceref VOTER_" + str(3*i+2) + "))\n"
                                toWrite += "          )\n"
                                toWrite += "         )\n"

                        toWrite += "         (net " + net2 + str(3*i+ii-1) + " (joined\n"
                        toWrite += "          (portref " + net2 + " (instanceref " + cell_rename(cell2,ii) + "))\n"
                        toWrite += "          (portref S (instanceref VOTER_" + str(3*i+ii-1) + "))\n"
                        toWrite += "          )\n"
                        toWrite += "         )\n"

        ii_voter += N
        f.write(toWrite)
        return ii_voter

#----------------------------------------
#		    MAIN		|
#----------------------------------------

NMR = {}                                                                                                                        # Dictionnaire pour la duplication des cellules
for i in range(2,N+1) :                                                                                                         # Pour NMR(2) jusqu'à NMR(N)
        NMR[i] = []                                                                                                             # Création de listes pour chaque KEY du dictionnaire

flagLUT = False                                                                                                                 # Initialisation du flagLUT
flagRedondancy = False                                                                                                          # Initialisation du flagRedondancy
flagTopDupli = False                                                                                                            # Initialisation du flagTopDupli
flagVoter = 0                                                                                                                   # Initialisation du flagVoter
paren = 0                                                                                                                       # Initialisation du compteur de paranthèses
keyword = ['IBUF', 'OBUF', 'BUFG', 'inst']                                                                                      # Déclaration des mots clés portant sur les cellules HDI Primitives
LUTParen = 0                                                                                                                    # Initialisation du compteur de paranthèse du LUT
voterParen = 0                                                                                                                  # Initialisation du compteur de paranthèse du Voter
HDIPrimitives = []                                                                                                              # Déclaration d'une liste pour stocker les cellules HDI Primitives utilisées dans le design
# Déclaration du LUT3 à ajouter dans HDI Primitives
LUT3 = "   (cell LUT3 (celltype GENERIC)\n     (view netlist (viewtype NETLIST)\n       (interface\n        (port O (direction OUTPUT))\n        (port I0 (direction INPUT))\n        (port I1 (direction INPUT))\n        (port I2 (direction INPUT))\n       )\n     )\n   )\n"
# Déclaration de la cellule VOTER à ajouter dans library work
VOTER = "   (cell voter (celltype GENERIC)\n     (view voter (viewtype NETLIST)\n       (interface \n        (port S (direction OUTPUT))\n        (port in1 (direction INPUT))\n        (port in2 (direction INPUT))        \n        (port in3 (direction INPUT))\n       )\n       (contents\n         (instance V (viewref netlist (cellref LUT3 (libraryref hdi_primitives)))\n           (property INIT (string \"8'hE8\"))\n         )\n         (net S_VOTER (joined\n          (portref O (instanceref V))\n          (portref S)\n          )\n         )\n         (net in1_VOTER (joined\n          (portref I0 (instanceref V))\n          (portref in1)\n          )\n         )\n         (net in2_VOTER (joined\n          (portref I1 (instanceref V))\n          (portref in2)\n          )\n         )\n         (net in3_VOTER (joined\n          (portref I2 (instanceref V))\n          (portref in3)\n          )\n         )\n       )\n     )\n   )\n"
voterNumber = 0                                                                                                                 # Initialisation du Voter courant
toAppend = []                                                                                                                   # Initialisation d'une liste utile à la récupération du nom des cellules
nbOutputsCells = {}                                                                                                             # Initialisation d'un dictionnaire qui associe une cellule avec son nombre de sortie
outputCounter = 0                                                                                                               # Initialisation du compteur de sorties d'une cellule
indexVoter = 0                                                                                                                  # Initialisation de l'index du Voter courant
OutputsCells = {}                                                                                                               # Initialisation d'un dictionnaire qui associe une cellule avec ses sorties
Outputs = []                                                                                                                    # Initialisation d'un tableau qui contient le nom des sortites du circuit
OUT = []                                                                                                                        # Initialisation d'un tableau qui contient le nom des signaux de sorties de chacune des cellules
IN = []                                                                                                                         # Initialisation d'un tableau qui contient le nom des signaux d'entrées de la TOP cellule
INTop = []                                                                                                                      # Initialisation d'un tableau qui contient le nom des signaux d'entrées de la TOP cellule
OUTtop = []                                                                                                                     # Initialisation d'un tableau qui contient le nom des signaux de sorties de la TOP cellule
aa = 0                                                                                                                          # Initialisation d'un iterateur
cell1 = ""                                                                                                                      # Initialisation de la cellule à interconnecter avec le VOTER (out ?)
cell2 = ""                                                                                                                      # Initialisation de la cellule à interconnecter avec le VOTER (in ?)
tata = ""                                                                                                                       # Initialisation d'une variable temporaire
ii_voter = 0                                                                                                                    # Initialisation d'un iterateur
InstanceNames = {}                                                                                                              # Initialisation d'un dictionnaire contenant le nom de toutes les instances du circuit
Names = []                                                                                                                      # Initialisation d'un tableau contenant le nom de l'instance
outputToAppend = []
Arrays = []
net1 = ""
net2 = ""
busBit = 0
flagCell = False

for count, line in enumerate(f0) :                                                                                              # Lecture ligne à ligne du fichier

        if count == 0 :                                                                                                         # Détection de la 1ere ligne du fichier
                top = line.split()[-1]                                                                                          # Récupération du design top module dans la 1ere ligne du fichier
                topNonDupli = ['(cell ' + top, '(view ' + top, '(interface', '(contents']                                       # Création d'un tableau avec les expressions à ne pas dupliquer

        if flagRedondancy == False :                                                                                            # Si nous ne sommes pas dans la partie à répliquer                                                                    
                if flagLUT == False :                                                                                           # Si nous ne sommes pas dans la library HDI Primitives
                        f1.write(line)                                                                                          # Nous recopions la ligne courante
                else :                                                                                                          # Sinon si nous sommes dans la library HDI Primitives
                        LUTParen = parenthesis_counter(line, LUTParen)                                                          # Mise à jour du compteur de paranthèses 
                        if "cell " in line.lower() :                                                                            # Si nous détectons une cellule dans la ligne
                                primitive = re.split(r"[ ,(,\t]", line)                                                         # Nous séparons la chaine de caractères dans une liste
                                primitive[:] = (value for value in primitive if value != "")                                    # Nous supprimons les caractères nuls de la liste de caractères
                                HDIPrimitives.append(primitive[1])                                                              # Nous récupérons le nom de la cellule et la stockons dans la liste HDIPrimitives



                        if "cell " in line.lower() and not "(comment " in line.lower() :                                        # Si on détecte une cellule
                                toAppend = re.split(r"[ ,(,\t]", line)                                                          # Nous séparons la chaine de caractères dans une liste
                                toAppend[:] = (value for value in toAppend if value != "")                                      # Nous supprimons les caractères nuls de la liste de caractères
                                OutputsCells[toAppend[1]] = ""                                                                  # Nous créons une KEY dans le dictionnaire qui associe cellule/outputs
                                nbOutputsCells[toAppend[1]] = 0                                                                 # Nous créons une KEY dans le dictionnaire qui associe cellule/nb d'outputs                                                                 
                                outputCounter = 0                                                                               # Reset du compteur d'OUTPUTs à la détection d'une nouvelle cellule
                                Outputs = []                                                                                    # Reset de la liste des OUTPUTs de la cellule courante
                                
                        if "input" in line.lower() :                                                                            # Si nous détectons une OUTPUT dans une cellule
                                inputToAppend = re.split(r"[ ,(,\t]", line)                                                     # Nous séparons la chaine de caractères dans une liste
                                inputToAppend[:] = (value for value in inputToAppend if value != "")                            # Nous supprimons les caractères nuls de la liste de caractères
                                if "array" in line.lower() :
                                        IN.append(inputToAppend[3])                                                             # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                                else :
                                        IN.append(inputToAppend[1])                                                             # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                        elif "output" in line.lower() and not "(comment ".lower() in line.lower() :                             # Si nous détectons une OUTPUT dans une cellule
                                if "array " in line.lower() :
                                        nbSplit = re.split(r'\W+', line)
                                        nbSplit[:] = (value for value in nbSplit if value != "")
                                        nb = nbSplit[-3]
                                        outputCounter += int(nb)
                                        Arrays.append(nbSplit[3])
                                else :
                                        outputCounter += 1                                                                      # Nous incrémentons le compteur de OUTPUTs
                                nbOutputsCells[toAppend[1]] = outputCounter                                                     # Nous mettons à jour le nombre d'OUTPUTs de la cellule courante
                                outputToAppend = re.split(r"[ ,(,\t]", line)                                                    # Nous séparons la chaine de caractères dans une liste
                                outputToAppend[:] = (value for value in outputToAppend if value != "")                          # Nous supprimons les caractères nuls de la liste de caractères
                                if "array " in line.lower() :
                                        Outputs.append(outputToAppend[3])                                                       # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                                        OutputsCells[toAppend[1]] = Outputs
                                elif "rename " in line.lower() and not "array " in line.lower() :
                                        Outputs.append(outputToAppend[2])                                                       # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                                        OutputsCells[toAppend[1]] = Outputs
                                else :
                                        Outputs.append(outputToAppend[1])                                                       # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                                        OutputsCells[toAppend[1]] = Outputs                                                     # Nous mettons à jour la liste d'OUTPUTs de la cellule courante




                        if LUTParen < 0 and 'LUT3' not in HDIPrimitives :                                                       # Si le nombre de paranthèse est négatif (=> dernière paranthèse de library HDIPrimitives) et que LUT3 n'a pas déjà été instancié
                                f1.write(LUT3)                                                                                  # Alors on ajoute l'instance LUT3 dans HDIPrimitives
                        f1.write(line)                                                                                          # On écrit la ligne courante dans le fichier
        else :                                                                                                                  # Sinon si nous sommes dans la partie à répliquer (library work)
                if "cell " in line.lower() and top.lower() in line.lower() :                                                    # S'il s'agit de la cellule au top de la hiérarchie                                           
                        flagTopDupli = True                                                                                     # Triplication de la cellule TOP activée
                        OutCells = list(OutputsCells.values())                                                                  # Récupération des noms de signaux de sorties 
                        for i in range(len(OutCells)):                                                                          # Pour chacuune des cellules
                                for j in range(len(OutCells[i])) :                                                              # Pour chacune des sorties de la cellule
                                        OUT.append(OutCells[i][j])                                                              # Nous ajoutons cette sortie à la liste des sorties
                                        
                elif "(comment " in line.lower() :                                                                              # Si on atteint la ligne "(comment" alors nous ne sommes plus dans library work
                        flagTopDupli = False                                                                                    # Triplication de la cellule TOP désactivée

                if flagTopDupli == False :                                                                                      # Si nous ne sommes pas dans la cellule au top de la hiérarchhie
                        f1.write(line)                                                                                          # Nous recopions la ligne courante
                        if "technology" in line.lower() :                                                                       # Si nous arrivons à la 1ere ligne de la déclaration de library work
                                f1.write(VOTER)                                                                                 # Nous ajoutons la cellule VOTER au design
                        if "cell " in line.lower() and not "(comment " in line.lower() :                                        # Si on détecte une cellule
                                toAppend = re.split(r"[ ,(,\t]", line)                                                          # Nous séparons la chaine de caractères dans une liste
                                toAppend[:] = (value for value in toAppend if value != "")                                      # Nous supprimons les caractères nuls de la liste de caractères
                                OutputsCells[toAppend[1]] = ""                                                                  # Nous créons une KEY dans le dictionnaire qui associe cellule/outputs
                                nbOutputsCells[toAppend[1]] = 0                                                                 # Nous créons une KEY dans le dictionnaire qui associe cellule/nb d'outputs                                                                 
                                outputCounter = 0                                                                               # Reset du compteur d'OUTPUTs à la détection d'une nouvelle cellule
                                Outputs = []                                                                                    # Reset de la liste des OUTPUTs de la cellule courante
                                
                        if "input" in line.lower() :                                                                            # Si nous détectons une OUTPUT dans une cellule
                                inputToAppend = re.split(r"[ ,(,\t]", line)                                                     # Nous séparons la chaine de caractères dans une liste
                                inputToAppend[:] = (value for value in inputToAppend if value != "")                            # Nous supprimons les caractères nuls de la liste de caractères
                                if "array" in line.lower() :
                                        IN.append(inputToAppend[3])                                                             # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                                else :
                                        IN.append(inputToAppend[1])                                                             # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                        elif "output" in line.lower() and not "(comment ".lower() in line.lower() :                             # Si nous détectons une OUTPUT dans une cellule
                                if "array " in line.lower() :
                                        nbSplit = re.split(r'\W+', line)
                                        nbSplit[:] = (value for value in nbSplit if value != "")
                                        nb = nbSplit[-3]
                                        outputCounter += int(nb)
                                        Arrays.append(nbSplit[3])
                                else :
                                        outputCounter += 1                                                                      # Nous incrémentons le compteur de OUTPUTs
                                nbOutputsCells[toAppend[1]] = outputCounter                                                     # Nous mettons à jour le nombre d'OUTPUTs de la cellule courante
                                outputToAppend = re.split(r"[ ,(,\t]", line)                                                    # Nous séparons la chaine de caractères dans une liste
                                outputToAppend[:] = (value for value in outputToAppend if value != "")                          # Nous supprimons les caractères nuls de la liste de caractères
                                if "array " in line.lower() :
                                        Outputs.append(outputToAppend[3])                                                       # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                                        OutputsCells[toAppend[1]] = Outputs
                                elif "rename " in line.lower() and not "array " in line.lower() :
                                        Outputs.append(outputToAppend[2])                                                       # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                                        OutputsCells[toAppend[1]] = Outputs
                                else :
                                        Outputs.append(outputToAppend[1])                                                       # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                                        OutputsCells[toAppend[1]] = Outputs                                                     # Nous mettons à jour la liste d'OUTPUTs de la cellule courante

                else :                                                                                                          # Si nous sommes dans la cellule au top de la hiérarchhie 
                        if "input" in line.lower() :                                                                            # Si nous détectons une OUTPUT dans une cellule
                                inputToAppend = re.split(r"[ ,(,\t]", line)                                                     # Nous séparons la chaine de caractères dans une liste
                                inputToAppend[:] = (value for value in inputToAppend if value != "")                            # Nous supprimons les caractères nuls de la liste de caractères
                                if "array" in line.lower() :
                                        INTop.append(inputToAppend[3])                                                          # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                                else :
                                        INTop.append(inputToAppend[1])                                                          # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                        elif "output" in line.lower() :                                                                         # Si nous détectons une OUTPUT dans une cellule
                                ouputTOPToAppend = re.split(r"[ ,(,\t]", line)                                                  # Nous séparons la chaine de caractères dans une liste
                                ouputTOPToAppend[:] = (value for value in ouputTOPToAppend if value != "")                      # Nous supprimons les caractères nuls de la liste de caractères
                                if "array" in line.lower() :
                                        OUTtop.append(ouputTOPToAppend[3])                                                      # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                                else :
                                        OUTtop.append(ouputTOPToAppend[1])                                                      # Nous ajoutons la sortie de la cellule à la liste des sorties de la cellule courante
                                
                        if "instance " in line.lower() :                                                                        # Si nous détectons une instance dans la ligne courante
                                instance = re.split(r"[,(,),\t,\s]", line)                                                      # Nous séparons la chaine de caractères dans une liste 
                                instance[:] = (value for value in instance if value != "")                                      # Nous supprimons les caractères nuls de la liste de caractères
                                if "rename" in line.lower() :                                                                   # S'il n'y a pas d'option de rename
                                        InstanceNames[instance[2]] = instance[-3]                                               # Nous stockons dans un dictionnaire l'instance et son nom (placés à d'autres positions)
                                else :                                                                                          # Sinon
                                        InstanceNames[instance[1]] = instance[3]                                                # Nous stockons dans un dictionnaire l'instance et son nom

                        if any(ll in line.lower() for ll in topNonDupli) :                                                      # Si 1 élément de topNonDupli est détecté dans la ligne courante
                                paren = 0                                                                                       # Nous remettons à 0 le compteur de paranthèses de library work 
                                f1.write(line)                                                                                  # Nous recopions la ligne courante
                        else :                                                                                                  # S'il s'agit d'un élément à dupliquer
                                paren = parenthesis_counter(line, paren)                                                        # Nous mettons à jour le nombre de paranthèses de library work

                                if "net " in line.lower() and not(any(ll.lower() in line.lower() for ll in INTop)) and not(any(" " + ll.lower() + " " in line.lower() for ll in OUTtop)) and not(any("\"" + ll.lower() + "[" in line.lower() for ll in OUTtop)) and not("&_const" in line.lower()) :
                                        flagVoter = 1                                                                           # Ecriture de la connexion avec le VOTER activée
                                elif any(ll in line for ll in nbOutputsCells.keys()) and not("portref " in line.lower()) and not("(joined" in line.lower()) :                                          # Si 1 KEY de nbOutputsCells est détectée dans la ligne courante
                                        for ll in nbOutputsCells.keys() :                                                       # Nous parcourons les KEYs de nbOutputsCells
                                                if ll in line :                                                                 # Si la KEY est dans la ligne
                                                        keyIndex = ll                                                           # Nous récupérons la KEY
                                                        continue                                                                # Nous pouvons passer à la suite du programme, car nous avons déjà trouvé la KEY qui nous intéresse
                                        
                                        for z in range(N*nbOutputsCells[keyIndex]) :                                            # Pour le nombre de sorties de la KEY à répliquer
                                                writeVoterInstance(f1, indexVoter)                                              # Nous écrivons une instance du VOTER_i
                                                indexVoter += 1                                                                 # Nous mettons à jour l'index du VOTER_i
                                                
                                if flagVoter == 1 :                                                                             # Si la connexion avec le VOTER doit être réalisée
                                        voterParen = parenthesis_counter(line, voterParen)                                      # Mise à jour du compteur de paranthèses du VOTER linker
                                        if "portref" in line.lower() :
                                                if "instanceref" in line.lower() :                                              # Si nous détectons une référence à une instance dans la ligne courante 
                                                        cellSplit = re.split(r"[,(,),\t,\s]", line)                             # Nous séparons la chaine de caractères dans une liste
                                                        cellSplit[:] = (value for value in cellSplit if value != "")            # Nous supprimons les caractères nuls de la liste de caractères
                                                        if "member" in line.lower() :                                           # Sinon
                                                                toto = InstanceNames[cellSplit[-1]]                             # Nous stockons dans un dictionnaire l'instance et son nom (placés à d'autres positions)   
                                                        else :                                                                  # Sinon
                                                                toto = InstanceNames[cellSplit[3]]                              # Nous récupérons l'instance lié au nom de l'instance 
                                                        
                                                        if toto in OutputsCells :                                               # Si cette instance est dans la liste des cellules de sortie
                                                                tata = OutputsCells[toto]                                       # Nous récupérons la liste des sorties de cette instance
                                                        else :
                                                                tata = ""
                                                        
                                                        if "member" in line.lower() :                                           # Sinon
                                                                if cellSplit[2] in tata :                                       # Si le signal appartient à l'instance
                                                                        cell1 = cellSplit[-1]                                   # Nous associons le nom de l'instance comme cellule de sortie
                                                                        flagCell = False
                                                                else :                                                          # Sinon
                                                                        cell2 = cellSplit[-1]                                   # Nous associons le nom de l'instance comme cellule d'entrtée (?)
                                                                        flagCell = True
                                                        else :                                                                  # Sinon
                                                                if cellSplit[1] in tata :                                       # Si le signal appartient à l'instance
                                                                        cell1 = cellSplit[3]                                    # Nous associons le nom de l'instance comme cellule de sortie (?)
                                                                        flagCell = False
                                                                else :                                                          # Sinon
                                                                        cell2 = cellSplit[3]                                    # Nous associons le nom de l'instance comme cellule d'entrtée (?)
                                                                        flagCell = True
                                                else :
                                                        cellSplit = re.split(r"[,(,),\t,\s]", line)                             # Nous séparons la chaine de caractères dans une liste
                                                        cellSplit[:] = (value for value in cellSplit if value != "")            # Nous supprimons les caractères nuls de la liste de caractères

                                                        if "member" in line.lower() :
                                                                cell1 = cellSplit[-2] + "[" + cellSplit[-1] + "]"
                                                        else :
                                                                print("Not implemented")                                                              
                                                tata = ""
                                                
                                        if voterParen == 0 :                                                                    # Si le compteur = 0 alors
                                                flagVoter = 2                                                                   # La connexion du VOTER a été réalisée et l'on peut exécuter la suite du code
                                                
                                        if flagCell == False :
                                                flagFind = 0
                                                for value in OUT :                                                              # Pour chacun des signaux de sorties des cellules
                                                        if value.lower() + " " in line.lower() :                                # Nous cherchons lequel est présent dans la ligne courante
                                                                net1 = value                                                    # Nous récupérons ce nom de signal
                                                                flagFind = 1
                                                                break                                                           # Nous arrêtons la recherche
                                                if flagFind == 0 :
                                                        for value in IN :                                                       # Pour chacun des signaux d'entrée des cellules
                                                                if value.lower() + " " in line.lower() :                        # Nous cherchons lequel est présent dans la ligne courante
                                                                        net1 = value                                            # Nous récupérons ce nom de signal
                                                                        flagFind = 1
                                                                        break
                                                if flagFind == 0 :
                                                        for value in HDIPrimitives :                                            # Pour chacun des signaux des primitives des cellules
                                                                if value.lower() + " " in line.lower() :                        # Nous cherchons lequel est présent dans la ligne courante
                                                                        net1 = value                                            # Nous récupérons ce nom de signal
                                                                        flagFind = 1
                                                                        break
                                                        
                                        else :       
                                                flagFind = 0
                                                for value in OUT :                                                              # Pour chacun des signaux de sorties des cellules
                                                        if value.lower() + " " in line.lower() :                                # Nous cherchons lequel est présent dans la ligne courante                                                                
                                                                net2 = value                                                    # Nous récupérons ce nom de signal
                                                                flagFind = 1
                                                                break                                                           # Nous arrêtons la recherche
                                                if flagFind == 0 :
                                                        for value in IN :                                                       # Pour chacun des signaux de sorties des cellules
                                                                if value.lower() + " " in line.lower() :                        # Nous cherchons lequel est présent dans la ligne courante
                                                                        net2 = value                                            # Nous récupérons ce nom de signal
                                                                        flagFind = 1
                                                                        break
                                                if flagFind == 0 :
                                                        for value in HDIPrimitives :                                            # Pour chacun des signaux de sorties des cellules
                                                                if value.lower() + " " in line.lower() :                        # Nous cherchons lequel est présent dans la ligne courante
                                                                        net2 = value                                            # Nous récupérons ce nom de signal
                                                                        flagFind = 1
                                                                        break
                                                                
                                        if flagVoter == 2 :                                                                     # Si nous devons écrire la connexion avec le VOTER
                                                try :
                                                        ii_voter = writeVoterLink(f1, net1, net2, cell1, cell2, aa, ii_voter, busBit)  # Nous écrivons la connexion avec le VOTER
                                                        busBit += 1
                                                        if busBit == nbOutputsCells[InstanceNames[cell1]] :
                                                                busBit = 0
                                                except :
                                                        ii_voter = writeVoterLink(f1, net1, net2, cell1, cell2, aa, ii_voter, -1)      # Nous écrivons la connexion avec le VOTER
                                                aa += 1                                                                         # Nous incrémentons l'itérateur pour les futurs VOTERs
                                                cell1 = ""                                                                      # Nous remettons à zéro la cellule d'entrée
                                                cell2 = ""                                                                      # Nous remettons à zéro la cellule de sortie
                                                net1 = ""
                                                net2 = ""
                                                flagVoter = 0                                                                   # Nous indiquons que la connexion a été faite
                                                
                                else :                                                                                          # Si la connexion avec le VOTER n'est pas à réaliser
                                        f1.write(line)                                                                          # Nous recopions la ligne courante
                                        if paren >= 0 :                                                                         # Si le compteur est > 0 (nous n'avons pas atteint la fin de library work)
                                                if "output" in line.lower() :                                                   # Si "output" est détectée dans la ligne courante
                                                        nb = 1
                                                        if "array " in line.lower() :
                                                                nbSplit = re.split(r'\W+', line)
                                                                nbSplit[:] = (value for value in nbSplit if value != "")
                                                                nb = nbSplit[-3]
                                                        voterNumber += int(nb) * N                                              # Nous ajoutons N VOTERs de plus
                                                for j in range(2,N+1) :                                                         # Pour le nombre de réplications 
                                                        NMR[j].append(cell_top(line, j))                                        # Nous répliquons la cellule dans la cellule au top de la hiérarchie
                                                        if paren == 0 :                                                         # Si le nombre de paranthèses est nul
                                                                for k in range(2, N+1) :                                        # Pour le nombre de réplication
                                                                        for l in range (len(NMR[k])) :                          # Pour chaque indice de réplication
                                                                                for m in range (len(NMR[k][l])) :               # Pour chaque ligne à répliquer
                                                                                        f1.write(NMR[k][l][m])                  # Nous répliquons la cellule ligne à ligne (caractère par caractère ?)
                                                                                f1.write('\n')                                  # Nous sautons une ligne à chaque nouvelle ligne
                                                                        NMR[k].clear()                                          # Nous vidons le dictionnaire une fois la réplication faite
                                                        
                
        if "library work" in line.lower() :                                                                                     # Détection d'une expression dans la ligne
                flagRedondancy = True                                                                                           # Redondance activée
        if "library hdi_primitives" in line.lower() :                                                                           # Détection d'une expression dans la ligne
                flagLUT = True                                                                                                  # Ecriture du LUT activée

f0.close()                                                                                                                      # Fermeture de la netlist d'entrée
f1.close()                                                                                                                      # Fermeture de la netlist tripliqué

