import re
import time
import random as rand
import sys

rand.seed(time.time())

filename1 = sys.argv[1]
filename2 = sys.argv[2]


try :
    f1 = open(filename1, 'r')
except FileNotFoundError :
    print(re.split(r"[\\]", filename1)[-1], "Not Found")
    exit(-1)

try :
    f2 = open(filename2, 'w')
except FileNotFoundError :
    print(re.split(r"[\\]", filename2)[-1], "Not Found")
    exit(-1)
    
sig = []
for count, line in enumerate(f1) :
    if "signal" in line :
        sig.append(line.split()[1])
    elif "entity " in line and "is" in line :
        tb_name = line.split()[1]
    else :
        pass


hazard = rand.randint(0, len(sig)-1)
value_to_force = rand.randint(0, 1)

to_write = "open_project [lindex $argv 0]"
to_write += "\n\nupdate_compile_order -fileset sources_1 \n"
to_write += "set_property top top [current_fileset] \n"
to_write += "update_compile_order -fileset sources_1 \n"
to_write += "set_property top tb_top [get_filesets sim_1] \n"
to_write += "set_property top_lib xil_defaultlib [get_filesets sim_1] \n"
to_write += "update_compile_order -fileset sim_1 \n"
to_write += "\n\nlaunch_simulation -mode post-implementation -type functional \n\n"
to_write += "restart\n\n"

fault_injection_line = "\nadd_force {/"
fault_injection_line += tb_name + "/" + sig[hazard]
fault_injection_line += "} -radix bin {"
fault_injection_line += str(value_to_force)
fault_injection_line += " 0ns}"

to_write += fault_injection_line
to_write += "\nrun 500 ns\n"
to_write += "start_gui\n"



f2.write(to_write)

f2.close()
f1.close()
