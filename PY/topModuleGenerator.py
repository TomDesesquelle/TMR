
import re

filename1 = r'C:\Users\td264208\Desktop\NMR\2021\Sujet Protection\Projet_protection_Archive\Validations\Modules\ALU4\alu4.vhd'
filename2 = r'C:\Users\td264208\Desktop\topModule.vhd'                                                  # New top module

def topModule(f, top, L) :
    f.write("TOP : entity work." + top + "\n\tPort Map (\n")
    for ll in range(len(L)) :
        f.write("\t\t" + L[ll] + " => " + L[ll])
        if ll != len(L) - 1 :
            f.write("\t,\n")
        else :
            f.write("\n\t\t);\n")
    return


try :                                                                                                   
    f1  = open(filename1,  'r')                                                                         # Try to open the initial testbench file
except FileNotFoundError :                                                                              # If the file can't be found
    print(re.split(r"[\\]", filename1)[-1], "not found")                                                # Corresponding error message
    exit(-1)                                                                                            # Exit program

flagWriteTopModule = False

for count, line in enumerate(f1):                                                                       # Lecture une à une des lignes du fichier initial
        if "process" in line :
               flagWriteTopModule = True
               break
        else :
            flagWriteTopModule = False
f1.close()

if(flagWriteTopModule == True) :
    print("Create a new top module")
    try :                                                                                                   
        f1  = open(filename1,  'r')                                                                     # Try to open the initial testbench file
    except FileNotFoundError :                                                                          # If the file can't be found
        print(re.split(r"[\\]", filename1)[-1], "not found")                                            # Corresponding error message
        exit(-1)                                                                                        # Exit program

    try :                                                                                                
        f2  = open(filename2,  'w')                                                                     # Try to open the initial testbench file
    except FileNotFoundError :                                                                          # If the file can't be found
        print(re.split(r"[\\]", filename2)[-1], "not found")                                            # Corresponding error message
        exit(-1)                                                                                        # Exit program

    flagEntity = False
    flagArchitecture = False
    top = ""
    archi = ""
    L = []
    
    for count2, line2 in enumerate(f1): 
        if "entity " in line2.lower() :
            temp = line2.split()
            top = temp[1]
            temp[1] = "top"
            f2.write(' '.join(temp) + '\n')
            flagEntity = True
        elif flagEntity == True and ("in " in line2.lower() or "out " in line2.lower()  or "inout " in line2.lower()) :
            if "port" in line2.lower() :
                name = re.split(r"[(, , :]", line2)
                name[:] = (value for value in name if value != "")                                      # Nous supprimons les caractères nuls de la liste de caractères
                for jj in range(len(name)) :
                    if name[jj].lower() == "port" :
                        pass
                    elif name[jj].lower() != "in" and name[jj].lower() != "out" and name[jj].lower() != "inout" :
                        L.append(name[jj])
                    else :
                        break
            else :
                name = re.split(r"[:, ]", line2)
                name[:] = (value for value in name if value != "")
                for ii in range(len(name)) :
                    if name[ii].lower() != "in" and name[ii].lower() != "out" and name[ii].lower() != "inout" :
                        L.append(name[ii])
                    else :
                        break
            f2.write(line2)
        elif "end " in line2.lower() and flagEntity == True :
            temp = line2.split()
            temp[-1] = "top;"
            f2.write(' '.join(temp) + '\n')
            flagEntity = False
        elif "architecture " in line2.lower() :
            archi = line2.split()[1]
            arch = line2.split()
            arch[3] = "top"
            line2 = " ".join(arch) + '\n'
            flagArchitecture = True
            f2.write(line2)
        elif "begin" in line2.lower() and len(line2.split()) == 1 and flagArchitecture == True :
            f2.write(line2)
            topModule(f2, top, L)
            f2.write("\nend " + archi + ";\n")
            break;
        elif flagEntity == False and flagArchitecture == False :
            f2.write(line2)
        else :
            pass
       
    f2.close()
    f1.close()
else :
    print("Don't need a new top module")
