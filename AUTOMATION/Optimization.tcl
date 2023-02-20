open_project [lindex $argv 0]/NMR.xpr

update_compile_order -fileset sources_1


set_property SOURCE_SET sources_1 [get_filesets sim_1]
import_files -fileset sim_1 -norecurse [lindex $argv 1]
update_compile_order -fileset sources_1

set_property top top [get_filesets sim_1] 
set_property top tb_top [get_filesets sim_1] 
set_property top_lib xil_defaultlib [get_filesets sim_1] 
update_compile_order -fileset sim_1 


add_files -fileset constrs_1 -norecurse [lindex $argv 2] 
add_files -fileset constrs_1 -norecurse [lindex $argv 3] 
add_files -fileset constrs_1 -norecurse [lindex $argv 4] 
add_files -fileset constrs_1 -norecurse [lindex $argv 5] 

import_files -fileset constrs_1 [lindex $argv 2] 
import_files -fileset constrs_1 [lindex $argv 3]
import_files -fileset constrs_1 [lindex $argv 4]
import_files -fileset constrs_1 [lindex $argv 5]


update_compile_order -fileset sources_1
update_compile_order -fileset sim_1

launch_runs impl_1 -jobs 4 
wait_on_run impl_1 

close_project
exit

#open_run impl_1 -name impl_1 

#launch_simulation -mode post-implementation -type functional
#start_gui 