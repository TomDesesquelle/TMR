import re
import sys

filename1 = sys.argv[1]                                                                                                                 # Fichier contenant toutes les primitives du circuit, hormis les VCC, les GND                                                                 
filename2 = sys.argv[2]                                                                                                                 # Nouveau fichier de contraintes

strat = 2                                                                                                                               # Choix de la stratégie

try :
    f1 = open(filename1, 'r')                                                                                                           # On essaye d'ouvrir le fichier contenant les primitives
    f2 = open(filename2, 'w')                                                                                                           # On essaye d'ouvrir le nouveau fichier de contraines

    i = .0                                                                                                                              # On initialise une variable i à 0
    
    flagBreak = False                                                                                                                   # On initialise flagBreak comme faux
    Cells = {}                                                                                                                          # On initialise un dictionnaire
    Elements = f1.readline().split()                                                                                                    # On extrait les mots de la première ligne
    for ii in Elements :                                                                                                                # Pour chacun de ses éléments
        Cells.setdefault(ii, [])                                                                                                        # On crée un KEY associé à une liste vide dans le dictionnaire
    LeafCells = f1.readline().split()                                                                                                   # On extrait les mots de la seconde ligne
    for jj in range(len(LeafCells)) :                                                                                                   # Pour chacunes de ses cellules
        Cells[Elements[jj]].append(LeafCells[jj])                                                                                       # On complète les listes du dictionnaire

    toRemove = []                                                                                                                       # On initialise une liste vide des éléments à supprimer
    for ii in Cells.keys() :                                                                                                            # Pour chacun des éléments du dictionnaire
        if(not "LUT" in ii.upper()) :                                                                                                   # S'il ne s'agit pas d'un LUT
            toRemove.append(ii)                                                                                                         # On ajoute cet élément à la liste des éléments à supprimer
    for tt in toRemove :                                                                                                                # Pour chacun des éléments de la liste à supprimer
        del Cells[tt]                                                                                                                   # On supprime cet élément du dictionnaire
    
    while(len(Cells) > 0 and flagBreak == False) :                                                                                      # Tant que la liste des éléments n'est pas vide et que le flagBreak est faux
        if("LUT6_2" in list(map(lambda x:x.upper(),Cells.keys()))) :                                                                    # Si le dictionnaire contient des LUT6_2
            del Cells["LUT6_2"]                                                                                                         # On les supprime du dictionnaire

        if("LUT6" in list(map(lambda x:x.upper(),Cells.keys()))) :                                                                      # Si le dictionnaire contient des LUT6
            del Cells["LUT6"]                                                                                                           # On les supprime du dictionnaire
            
        if("LUT5" in list(map(lambda x:x.upper(),Cells.keys()))) :                                                                      # Si le dictionnaire contient des LUT5
            del Cells["LUT5"]                                                                                                           # On les supprime du dictionnaire

        while("LUT4" in list(map(lambda x:x.upper(),Cells.keys()))) :                                                                   # Tant que le dictionnaire contient des LUT4
            if("LUT1" in list(map(lambda x:x.upper(),Cells.keys()))) :                                                                  # Si le dictionnaire contient des LUT1
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT4"][0] + "]\n")                      # On écrit une contrainte de groupement sur le LUT4 
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT1"][0] + "]\n")                      # On écrit une contrainte de groupement sur le LUT1
                i += 1                                                                                                                  # On met à jour la valeur de la contrainte de groupement
                Cells["LUT4"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le LUT4 contraint
                Cells["LUT1"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le LUT1 contraint
                if len(Cells["LUT4"]) == 0 :                                                                                            # S'il n'y a plus de valeurs pour l'élément LUT4
                    del Cells["LUT4"]                                                                                                   # On supprime l'élément LUT4 du dictionnaire
                if len(Cells["LUT1"]) == 0 :                                                                                            # S'il n'y a plus de valeurs pour l'élément LUT1
                    del Cells["LUT1"]                                                                                                   # On supprime l'élément LUT1 du dictionnaire
            else :                                                                                                                      # Sinon 
                break                                                                                                                   # On sort de la boucle while
                
                i += 1                                                                                                                  # On met à jour la valeur de la contrainte de groupement
                Cells["LUT1"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le premier LUT1 contraint
                Cells["LUT1"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le premier LUT1 contraint
                if len(Cells["LUT1"]) == 0 :                                                                                            # S'il n'y a plus de valeurs pour l'élément LUT1
                    del Cells["LUT1"]                                                                                                   # On supprime l'élément LUT1 du dictionnaire
            else :                                                                                                                      # Sinon
                break                                                                                                                   # On sort de la boucle while

        flagBreak = True                                                                                                                # Toutes les opérations ont été réalisées, flagBreak passe vrai                                                                                             # Message pour l'utilsateur
        while("LUT3" in list(map(lambda x:x.upper(),Cells.keys()))) :                                                                   # Tant que le dictionnaire contient des LUT3                                  
            if("LUT2" in list(map(lambda x:x.upper(),Cells.keys()))) :                                                                  # Si le dictionnaire contient des LUT2
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT3"][0] + "]\n")                      # On écrit une contrainte de groupement sur le LUT3
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT2"][0] + "]\n")                      # On écrit une contrainte de groupement sur le LUT2
                i += 1                                                                                                                  # On met à jour la valeur de la contrainte de groupement
                Cells["LUT3"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le LUT3 contraint
                Cells["LUT2"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le LUT2 contraint
                if len(Cells["LUT3"]) == 0 :                                                                                            # S'il n'y a plus de valeurs pour l'élément LUT3
                    del Cells["LUT3"]                                                                                                   # On supprime l'élément LUT3 du dictionnaire
                if len(Cells["LUT2"]) == 0 :                                                                                            # S'il n'y a plus de valeurs pour l'élément LUT2
                    del Cells["LUT2"]                                                                                                   # On supprime l'élément LUT2 du dictionnaire
            elif("LUT1" in list(map(lambda x:x.upper(),Cells.keys()))) :                                                                # Sinon s'il n'y a plus de LUT2, mais qu'il reste des LUT1
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT3"][0] + "]\n")                      # On écrit une contrainte de groupement sur le LUT3           
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT1"][0] + "]\n")                      # On écrit une contrainte de groupement sur le LUT1
                i += 1                                                                                                                  # On met à jour la valeur de la contrainte de groupement
                Cells["LUT3"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le LUT3 contraint
                Cells["LUT1"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le LUT1 contraint
                if len(Cells["LUT3"]) == 0 :                                                                                            # S'il n'y a plus de valeurs pour l'élément LUT3
                    del Cells["LUT3"]                                                                                                   # On supprime l'élément LUT3 du dictionnaire
                if len(Cells["LUT1"]) == 0 :                                                                                            # S'il n'y a plus de valeurs pour l'élément LUT1
                    del Cells["LUT1"]                                                                                                   # On supprime l'élément LUT1 du dictionnaire
            else :                                                                                                                      # Sinon
                break                                                                                                                   # On sort de la boucle while
            
        while("LUT2" in list(map(lambda x:x.upper(),Cells.keys()))) :                                                                   # Tant que le dictionnaire contient des LUT2
            if(len(Cells["LUT2"]) > 1) :                                                                                                # S'il reste au moins deux LUT2
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT2"][0] + "]\n")                      # On écrit une contrainte de groupement sur le premier LUT2
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT2"][1] + "]\n")                      # On écrit une contrainte de groupement sur le second LUT2
                i += 1                                                                                                                  # On met à jour la valeur de la contrainte de groupement
                Cells["LUT2"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le premier LUT2 contraint
                Cells["LUT2"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le second LUT2 contraint
                if len(Cells["LUT2"]) == 0 :                                                                                            # S'il n'y a plus de valeurs pour l'élément LUT2
                    del Cells["LUT2"]                                                                                                   # On supprime l'élément LUT2 du dictionnaire
            elif("LUT1" in list(map(lambda x:x.upper(),Cells.keys()))) :                                                                # Sinon s'il n'y a plus qu'un LUT2, mais qu'il reste des LUT1
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT2"][0] + "]\n")                      # On écrit une contrainte de groupement sur le LUT2
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT1"][0] + "]\n")                      # On écrit une contrainte de groupement sur le LUT1
                i += 1                                                                                                                  # On met à jour la valeur de la contrainte de groupement
##                    Cells["LUT2"].pop(0)                                                                                              # On supprime de la liste du dictionnaire le LUT2 contraint
                Cells["LUT1"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le LUT1 contraint
##                    if len(Cells["LUT2"]) == 0 :
                del Cells["LUT2"]                                                                                                       # On supprime l'élément LUT2 du dictionnaire
                if len(Cells["LUT1"]) == 0 :                                                                                            # S'il n'y a plus de valeurs pour l'élément LUT1
                    del Cells["LUT1"]                                                                                                   # On supprime l'élément LUT1 du dictionnaire
            else :                                                                                                                      # Sinon
                break                                                                                                                   # On sort de la boucle while

        while("LUT1" in list(map(lambda x:x.upper(),Cells.keys()))) :                                                                   # Tant que le dictionnaire contient des LUT1
            if(len(Cells["LUT1"]) > 1) :                                                                                                # S'il reste au moins deux LUT1
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT1"][0] + "]\n")                      # On écrit une contrainte de groupement sur le premier LUT1
                f2.write("set_property LUTNM LUT_group" + str(int(i)) + " [get_cells " + Cells["LUT1"][1] + "]\n")                      # On écrit une contrainte de groupement sur le second LUT1
                i += 1                                                                                                                  # On met à jour la valeur de la contrainte de groupement
                Cells["LUT1"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le premier LUT1 contraint
                Cells["LUT1"].pop(0)                                                                                                    # On supprime de la liste du dictionnaire le premier LUT1 contraint
                if len(Cells["LUT1"]) == 0 :                                                                                            # S'il n'y a plus de valeurs pour l'élément LUT1
                    del Cells["LUT1"]                                                                                                   # On supprime l'élément LUT1 du dictionnaire
            else :                                                                                                                      # Sinon
                break                                                                                                                   # On sort de la boucle while

        flagBreak = True                                                                                                                # Toutes les opérations ont été réalisées, flagBreak passe vrai

    f2.close()                                                                                                                          # On ferme le fichier
    f1.close()                                                                                                                          # On ferme le fichier

except FileNotFoundError:                                                                                                               # Si un des deux fichiers n'est pas trouvé
    print(re.split(r"[\\]", filename1)[-1], " or ", re.split(r"[\\]", filename2)[-1], "not found")                                      # Message d'erreur associé
