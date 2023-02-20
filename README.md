# TMR
This project aims to implement a TMR (Triple Modular Redundancy) solution on Xilinx FPGAs.
The purpose of this solution is to optimize the available space to occupy as little space as possible.

The 'PY' folder contains all the useful Python scripts to perform redundancy on a circuit and optimize the space occupied.
PY contains: 
  - CellsCombining.py
  - constraintsGenerator.py
  - faultInjection.py
  - internet.py
  - NMR_TOP.py
  - tbenchGenerator.py
  - TMR_GUI.py
  - topModuleGenerator.py
  - utilization.py
  - voterNGenerator.py
  
The 'AUTOMATION' folder contains all the TCL scripts and the CMD script useful to use the Xilinx Vivado software and run our solution.
AUTOMATION contains: 
  - netlistGenerator.tcl
  - TMRProjectCreator.tcl
  - Optimization.tcl
  - TMR.cmd

The 'REPORT' folder contains the project report and the user manual.
REPORT contains:
  - Guide d'utilisation PROJET TMR Baldacchino Desesquelle Guessard.pdf
  - RAPPORT_PROJET_TMR_BALDACCHINO_DESESQUELLE_GUESSARD.pdf

The 'STATE OF THE ART' folder contains files about the current techniques to do TMR.
STATE OF THE ART contains:
  - ASQED13 - FPGA.pdf
  - IOLTS13 - FPGA Mitigation.pdf
  - LASCAS12 - FPGA Mitigation.pdf
  - ReConFig13 - FPGA Mitigation.pdf


####################################################################
##                        GRENOBLE INP PHELMA                     ##
####################################################################
##                           SUPERVISOR                           ##
##                         Régis Leveugle                         ##
##              Regis.Leveugle@univ-grenoble-alpes.fr             ##
##                                                                ##
##                          CONTRIBUTORS                          ##
##                        Axel Baldacchino                        ##
##                 axel.baldacchino@grenoble-inp.org              ##
##                                                                ##
##                         Tom Désesquelle                        ##
##                  tom.desesquelle@grenoble-inp.org              ##
##                                                                ##
##                       Pierre-Olivier Guessard                  ##
##            pierre-olivier.guessard@grenoble-inp.org            ##
####################################################################
