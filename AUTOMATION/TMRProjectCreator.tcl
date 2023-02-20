
create_project NMR [lindex $argv 0] -part [lindex $argv 1] -force

set_property design_mode GateLvl [current_fileset] 
set_property target_language VHDL [current_project] 

import_files -norecurse [lindex $argv 2]

set_property top top [current_fileset]

link_design -name netlist_1 

reorder_files -auto 

set fp [open [lindex $argv 3] w]
set toto [get_property REF_NAME [get_cells -hier -filter {IS_PRIMITIVE==1 && NAME !~ "*inst" && NAME !~ "*VCC*" && NAME !~ "*GND*"}]]
puts $fp $toto
set toto [get_cells -hier -filter {IS_PRIMITIVE==1 && NAME !~ "*inst" && NAME !~ "*VCC*" && NAME !~ "*GND*"}]
puts $fp $toto
close $fp

write_verilog -mode synth_stub [lindex $argv 4] -force

close_design

close_project 

exit
