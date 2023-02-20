
#N = int(input("What is the order of the whished NMR? "))
#if N < 3 :
#	N = 3
#	print("Wrong value (<3) : N = 3 by default")

N = 3

filename = r'C:\Users\td264208\Desktop\VOTER' + str(N) + ".vhd"
f0 = open(filename, 'w')

library = "library IEEE;\nuse IEEE.STD_LOGIC_1164.ALL;\n"
entityStart = "entity voter is\n\tPort (\n"
entityEnd = "\t\t\tV   : out STD_LOGIC\n\t\t);\nend voter;\n"
architectureStart = "architecture Behavioral of voter is\nbegin\n"
architectureEnd = "end Behavioral;\n"

IN_STD_LOGIC = " : in  STD_LOGIC;\n"

AND = []
OR = ""

f0.write(library)
f0.write(entityStart)
for ii in range(N) :
    f0.write("\t\t\tin" + str(ii) + IN_STD_LOGIC)
f0.write(entityEnd)
f0.write(architectureStart)
for jj in range (0, N) :
             for kk in range (jj + 1, N) :
                 AND.append("(in" + str(jj) + " AND in" + str(kk) + ")")
for ll in range(len(AND)-1) :
    OR += AND[ll] + " OR "
OR += AND[-1]

f0.write("\tV <= " + OR + ";\n")
f0.write(architectureEnd)
f0.close()
