open_project [lindex $argv 0]

update_compile_order -fileset sources_1
set_property top top [current_fileset] 
update_compile_order -fileset sources_1 

#set_property top tb_top [get_filesets sim_1] 
#set_property top_lib xil_defaultlib [get_filesets sim_1] 
#update_compile_order -fileset sim_1 

#launch_simulation -quiet
#source tb_top.tcl
#export_simulation -force -simulator xsim -directory C:/Users/td264208/Desktop/NMR/SIM -absolute_path -quiet
#close_sim -quiet

reset_run synth_1 
launch_runs synth_1 -jobs 4 
wait_on_run synth_1 
open_run synth_1 -name synth_1 
write_edif -force [lindex $argv 1] 
report_utilization -file [lindex $argv 2]
close_design

close_project 
exit