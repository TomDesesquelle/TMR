set initialProject_PATH=%~dp1
cd %initialProject_PATH%
MD temp
set TEMP_PATH=%initialProject_PATH%temp\


IF EXIST %1 (
	cd C:\Xilinx\Vivado\2018.3\bin
	
	ECHO Netlist will be generated 
	CALL vivado -mode tcl -source %~dp0\netlistGenerator.tcl -tclargs %1 %TEMP_PATH%topInitial.edf %TEMP_PATH%utilization_report.txt
	ECHO Netlist generated without redundancy


	cd C:\Users\td264208\Desktop\NMR.PY
	
	ECHO Estimated utilization will be calculated
	CALL utilization.py %TEMP_PATH%utilization_report.txt
	ECHO Utilization calculated
	ECHO If the results obtained do not allow TMR, close the current program and make modifications (designs? FPGA? etc.)
	
	
	ECHO Pinout will be downloaded
	CALL internet.py %3 %TEMP_PATH%
	ECHO Pinout downloaded
	
	ECHO Constraints will be replicated
	CALL constraintsGenerator.py %4 %5 %6 %TEMP_PATH%IO_properties.xdc %TEMP_PATH%liste_NOM_PIN.xdc %TEMP_PATH%timing.xdc %TEMP_PATH%pinout.txt
	ECHO Constraints replicated
	
	ECHO TOP will be replicated
	CALL NMR_TOP.py %TEMP_PATH%topInitial.edf %TEMP_PATH%top.edf
	ECHO TOP replicated

	
	cd C:\Xilinx\Vivado\2018.3\bin
	
	ECHO Project will be created
	CALL vivado -mode tcl -source %~dp0\TMRProjectCreator.tcl -tclargs %2 %3 %TEMP_PATH%top.edf %TEMP_PATH%LUTCombining.txt %TEMP_PATH%top.v 
	ECHO Project created
	
	
	cd C:\Users\td264208\Desktop\NMR.PY
	
	ECHO LUT will be combined
	CALL CellsCombining.py %TEMP_PATH%LUTCombining.txt %TEMP_PATH%LUTCombining.xdc
	ECHO LUT combined
	
	ECHO Testbench will be replicated
	CALL tbenchGenerator.py %7 %TEMP_PATH%tb_top.vhd %TEMP_PATH%top.v 
	ECHO Testbench replicated
	
	
	cd C:\Xilinx\Vivado\2018.3\bin
	
	ECHO Project will be optimized 
	CALL vivado -mode tcl -source %~dp0\Optimization.tcl -tclargs %2 %TEMP_PATH%tb_top.vhd %TEMP_PATH%IO_properties.xdc %TEMP_PATH%liste_NOM_PIN.xdc %TEMP_PATH%timing.xdc %TEMP_PATH%LUTCombining.xdc
	ECHO Project optimized 
	
	cd C:\Users\td264208\Desktop\NMR.PY
	
	ECHO Fault injection will be created
	CALL faultInjection.py %TEMP_PATH%tb_top.vhd %TEMP_PATH%Simulation.tcl
	ECHO Fault injection created
	
	cd C:\Xilinx\Vivado\2018.3\bin
	
	ECHO Project will be simulated
	CALL vivado -mode tcl -source %TEMP_PATH%Simulation.tcl -tclargs %2/NMR.xpr 
	ECHO Project simulated
	
	)
	
IF NOT EXIST %1 (
	ECHO %1 NOT FOUND
	)
