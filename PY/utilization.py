import re
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

filename = sys.argv[1]

utilization_lut = []
utilization_buf = []
utilization_IO = []

try :
    f1 = open(filename, 'r')
    
    for count, line in enumerate(f1) :
        if "slice luts" in line.lower() :
            utilization_lut.append(line.split()[4])
            utilization_lut.append(line.split()[8])
        if "slice registers" in line.lower() :
            utilization_buf.append(line.split()[4])
            utilization_buf.append(line.split()[8])
        if "bonded iob" in line.lower() :
            utilization_IO.append(line.split()[4])
            utilization_IO.append(line.split()[8])
                
            
    # LUT
    cur_usage_LUT_ratio = (int(utilization_lut[0])/int(utilization_lut[1]))*100
    cur_remaining_LUT_space = 100 - cur_usage_LUT_ratio
    nb_LUT_remaining = int(utilization_lut[1]) - int(utilization_lut[0])
    print("Remaining LUT number : " + str(nb_LUT_remaining))
    print("LUT Usage (%) : " + str(round(cur_usage_LUT_ratio,3)) + "%\n")
    

    # BUF
    cur_usage_BUF_ratio = (int(utilization_buf[0])/int(utilization_buf[1]))*100
    cur_remaining_BUF_space = 100 - cur_usage_BUF_ratio
    nb_BUF_remaining = int(utilization_buf[1]) - int(utilization_buf[0])
    print("Remaining BUF number : " + str(nb_BUF_remaining))
    print("BUF Usage (%) : " + str(round(cur_usage_BUF_ratio,3)) + "%\n")

    #Assez de place pour la redondance pour les BUFFER
    if cur_usage_BUF_ratio < (1/3)*100 :
        TMR_for_buf = 1
    else  :
        TMR_for_buf = 0
    

    # IO
    cur_usage_IO_ratio = (int(utilization_IO[0])/int(utilization_IO[1]))*100
    cur_remaining_IO_space = 100 - cur_usage_IO_ratio
    nb_IO_remaining = int(utilization_IO[1]) - int(utilization_IO[0])
    print("Remaining IO number : " + str(nb_IO_remaining))
    print("IO Usage (%) : " + str(round(cur_usage_IO_ratio,3)) + "%")
    
    #Assez de place pour la redondance pour les IO
    if cur_usage_IO_ratio < (1/3)*100 :
        TMR_for_io = 1
    else  :
        TMR_for_io = 0
  

    f1.close()

    # Add plt figure
    
    fig, (ax1, ax2, ax3) = plt.subplots(3,1)
    fig.suptitle('Utilization')
    yLUT = np.array([int(utilization_lut[0]), int(utilization_lut[1]) - int(utilization_lut[0])])
    labelsLUT = ["Used", "Availables"]
    ax1.set_title('LUTs Utilization')
    ax1.pie(yLUT, labels = labelsLUT, colors  = ['coral', 'skyblue'])
    yBUF = np.array([int(utilization_buf[0]), int(utilization_buf[1]) - int(utilization_buf[0])])
    labelsBUF = ["Used", "Availables"]
    ax2.set_title('BUFs Utilization')
    ax2.pie(yBUF, labels = labelsBUF, colors  = ['coral', 'skyblue'])
    yIO = np.array([int(utilization_IO[0]), int(utilization_IO[1]) - int(utilization_IO[0])])
    labelsIO = ["Used", "Availables"]
    ax3.set_title('IOs Utilization')
    ax3.pie(yIO, labels = labelsIO, colors  = ['coral', 'skyblue'])
    plt.show()
except FileNotFoundError :
    print(re.split(r"[\\]", filename)[-1], "Not Found")
    exit(-1)   
