import re
import subprocess
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
#from PIL import ImageTk,Image

root = Tk()

#Title
root.title('TMR')
#Size
root.geometry("800x650")
root.resizable(width=False, height=True)
#Icon
#root.iconbitmap('')


#Create a main frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

#Create a canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

#Add a scrollbar to the canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

#Configure the canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

#Create ANOTHER frame INSIDE the canvas
second_frame = Frame(my_canvas)

#Add that new frame to a window in the canvas
my_canvas.create_window((0,0), window=second_frame, width=780 , anchor="nw")



##### POP UP¨INFO FONCTION (FRAME PROJECT) #####
def popup_info_prj(value) :
    if value == "XDC_IO_PRJ" or value == "XDC_PAD_PRJ" or value == "XDC_TIMING_PRJ" :
        messagebox.showinfo("Constraints Files Path : Import Info", "Put the constraints file(s) of the circuit. It has to be in .xdc format")
    elif value == "TB_prj" :
        messagebox.showinfo("Test Bench Files Path : Import Info", "Put the test bench file(s) of the circuit. It has to be in VHDL format")
    elif value == "XPR" :
        messagebox.showinfo("Vivado Project Path : Import Info", "Put VIVADO file of the project you want to import. It has to be in XPR format")
    elif value == "OUTPUT" :
        messagebox.showinfo("Output File Location : Info", "Specify the path directory where the output files will be saved")

####### IMPORT FILES FUNCTION (FRAME PROJECT) #######
def import_files_prj(value) :
    if value == "XDC_IO_PRJ" :
        entry_io_xdc_path_prj.delete(0, END)
        xdc_file_name = filedialog.askopenfilename(initialdir="C:", title="Select a RTL file", filetypes=(("Contraints Files (*XDC)",".xdc"),("All Files (*)","*.*")))
        entry_io_xdc_path_prj.insert(0,xdc_file_name)
    elif value == "XDC_PAD_PRJ" :
        entry_pad_xdc_path_prj.delete(0, END)
        xdc_file_name = filedialog.askopenfilename(initialdir="C:", title="Select a RTL file", filetypes=(("Contraints Files (*XDC)",".xdc"),("All Files (*)","*.*")))
        entry_pad_xdc_path_prj.insert(0,xdc_file_name)
    elif value == "XDC_TIMING_PRJ" :
        entry_timing_xdc_path_prj.delete(0, END)
        xdc_file_name = filedialog.askopenfilename(initialdir="C:", title="Select a RTL file", filetypes=(("Contraints Files (*XDC)",".xdc"),("All Files (*)","*.*")))
        entry_timing_xdc_path_prj.insert(0,xdc_file_name)
    elif value == "TB_prj" :
        tb_file_name = filedialog.askopenfilename(initialdir="C:", title="Select a RTL file", filetypes=(("VHDL Files (*VHD)","*.vhd"),("All Files (*)","*.*")))
        entry_tb_path_prj.insert(0, tb_file_name)
    elif value == "XPR" :
        xpr_file_name = filedialog.askopenfilename(initialdir="C:", title="Select a RTL file", filetypes=(("VIVADO Project File (*XPR)","*.xpr"),("All Files (*)","*.*")))
        entry_prj_vivado_path.insert(0, xpr_file_name)
    elif value == "OUTPUT" :
        output_dir = filedialog.askdirectory(initial="C:", title="Specify the Output Diles Directory")
        entry_output_location.insert(0, output_dir)

####### FPGA SELECTION FUNCTION (FRAME CONFIGURATION) #######
def fpga_selection(event) :    
    if fpga_fam_selection.get() == "Artix-7 FPGA" :
        fpga_select['values'] = (   '- Select your Artix FPGA -'    ,
                                    'xc7a12tcpg238-1'               ,
                                    'xc7a12tcsg325-1'               ,

                                    'xc7a15tcpg236-1'               ,
                                    'xc7a15tcsg324-1'               ,
                                    'xc7a15tcsg325-1'               ,
                                    'xc7a15tftg256-1'               ,
                                    'xc7a15tfgg484-1'               ,

                                    'xc7a25tcpg238-1'               ,
                                    'xc7a25tcsg325-1'               ,

                                    'xc7a35tcpg236-1'               ,
                                    'xc7a35tcsg324-1'               ,
                                    'xc7a35tcsg325-1'               ,
                                    'xc7a35tftg256-1'               ,
                                    'xc7a35tfgg484-1'               ,

                                    'xc7a50tcpg236-1'               ,
                                    'xc7a50tcsg324-1'               ,
                                    'xc7a50tcsg325-1'               ,
                                    'xc7a50tftg256-1'               ,
                                    'xc7a50tfgg484-1'               ,

                                    'xc7a75tcsg324-1'               ,
                                    'xc7a75tftg256-1'               ,
                                    'xc7a75tfgg484-1'               ,
                                    'xc7a75tfgg676-1'               ,

                                    'xc7a100tcsg324-1'              ,
                                    'xc7a100tftg256-1'              ,
                                    'xc7a100tfgg484-1'              ,
                                    'xc7a100tfgg676-1'              ,

                                    'xc7a200tsbd484-1'              ,
                                    'xc7a200tfbg484-1'              ,
                                    'xc7a200tfbg676-1'              ,
                                    'xc7a200tffg1156-1'             ,
                                )
        fpga_select.set("- Select your Artix FPGA -")
        fpga_entry.grid_forget()
        fpga_select.grid(row=1, column=1, sticky=W+E)
    elif fpga_fam_selection.get() == "Kintex-7 FPGA" :
        fpga_select['values'] = (   '- Select your Kintex FPGA -'   ,
                                    'xc7k70tfb484-1'                ,
                                    'xc7k70tfbg484-1'               ,
                                    'xc7k70tfb676-1'                ,
                                    'xc7k70tfbg676-1'               ,
                                    
                                    'xc7k160tfb484-1'               ,
                                    'xc7k160tfbg484-1'              ,
                                    'xc7k160tfb676-1'               ,
                                    'xc7k160tfbg676-1'              ,
                                    'xc7k160tff676-1'               ,
                                    'xc7k160tffg676-1'              ,
                                    
                                    'xc7k325tfb676-1'               ,
                                    'xc7k325tfbg676-1'              ,
                                    'xc7k325tfb900-1'               ,
                                    'xc7k325tfbg900-1'              ,
                                    'xc7k325tff676-1'               ,
                                    'xc7k325tffg676-1'              ,
                                    'xc7k325tff900-1'               ,
                                    'xc7k325tffg900-1'              ,
                                    
                                    'xc7k355tff901-1'               ,
                                    'xc7k355tffg901-1'              ,
                                    
                                    'xc7k410tfb676-1'               ,
                                    'xc7k410tfbg676-1'              ,
                                    'xc7k410tfb900-1'               ,
                                    'xc7k410tfbg900-1'              ,
                                    'xc7k410tff676-1'               ,
                                    'xc7k410tffg676-1'              ,
                                    'xc7k410tff900-1'               ,
                                    'xc7k410tffg900-1'              ,
                                    
                                    'xc7k420tff901-1'               ,     
                                    'xc7k420tffg901-1'              ,
                                    'xc7k420tff1156-1'              ,
                                    'xc7k420tffg1156-1'             ,

                                    'xc7k480tff901-1'               ,
                                    'xc7k480tffg901-1'              ,
                                    'xc7k480tff1156-1'              ,
                                    'xc7k480tffg1156-1'
                                )
        fpga_select.set("- Select your Kintex FPGA -")
        fpga_entry.grid_forget()
        fpga_select.grid(row=1, column=1, sticky=W+E)
    elif fpga_fam_selection.get() == "Spartan-7 FPGA" :
        fpga_select['values'] = (
                                    '- Select your Spartan FPGA -'  ,
                                    'xc7s6ftgb196-1'                ,
                                    'xc7s6cpga196-1'                ,
                                    'xc7s6csga225-1'                ,
                                    
                                    'xc7s15ftgb196-1'               ,
                                    'xc7s15cpga196-1'               ,
                                    'xc7s15csga225-1'               ,
                                    
                                    'xc7s25ftbg196-1'               ,
                                    'xc7s25csga225-1'               ,
                                    'xc7s25csga324-1'               ,
                                    
                                    'xc7s50ftgb196-1'               ,
                                    'xc7s50csga324-1'               ,
                                    'xc7s50fgga484-1'               ,
                                    
                                    'xc7s75fgga484-1'               ,
                                    'xc7s75fgga676-1'               ,
                                    
                                    'xc7s100fgga484-1'              ,
                                    'xc7s100fgga676-1'
                                )
        fpga_select.set("- Select your Spartan FPGA -")
        fpga_entry.grid_forget()
        fpga_select.grid(row=1, column=1, sticky=W+E)
    elif fpga_fam_selection.get() == "Virtex-7 FPGA" :
        fpga_select['values'] = (
                                    '- Select your Virtex FPGA -'   ,
                                    
                                    'xc7v585tff1157-1'              ,
                                    'xc7v585tffg1157-1'             ,
                                    'xc7v585tff1761-1'              ,
                                    'xc7v585tffg1761-1'             ,

                                    'xc7v2000tfl1925-1'             ,
                                    'xc7v2000tflg1925-1'            ,
                                    'xc7v2000tfh1761-1'             ,
                                    'xc7v2000tfhg1761-1'            ,

                                    'xc7vx330tff1157-1'             ,
                                    'xc7vx330tffg1157-1'            ,
                                    'xc7vx330tff1761-1'             ,
                                    'xc7vx330tffg1761-1'            ,

                                    'xc7vx415tff1157-1'             ,
                                    'xc7vx415tffg1157-1'            ,
                                    'xc7vx415tff1158-1'             ,
                                    'xc7vx415tffg1158-1'            ,
                                    'xc7vx415tff1927-1'             ,
                                    'xc7vx415tffg1927-1'            ,

                                    'xc7vx485tff1157-1'             ,
                                    'xc7vx485tffg1157-1'            ,
                                    'xc7vx485tff1158-1'             ,
                                    'xc7vx485tffg1158-1'            ,
                                    'xc7vx485tff1761-1'             ,
                                    'xc7vx485tffg1761-1'            ,
                                    'xc7vx485tff1927-1'             ,
                                    'xc7vx485tffg1927-1'            ,
                                    'xc7vx485tff1930-1'             ,
                                    'xc7vx485tffg1930-1'            ,                                     

                                    'xc7vx550tff1158-1'             ,
                                    'xc7vx550tffg1158-1'            ,
                                    'xc7vx550tff1927-1'             ,
                                    'xc7vx550tffg1927-1'            ,

                                    'xc7vx690tff1157-1'             ,
                                    'xc7vx690tffg1157-1'            ,
                                    'xc7vx690tff1158-1'             ,
                                    'xc7vx690tffg1158-1'            ,
                                    'xc7vx690tff1761-1'             ,
                                    'xc7vx690tffg1761-1'            ,
                                    'xc7vx690tff1926-1'             ,
                                    'xc7vx690tffg1926-1'            ,
                                    'xc7vx690tff1930-1'             ,
                                    'xc7vx690tffg1930-1'            ,

                                    'xc7vx980tff1926-1'             ,
                                    'xc7vx980tffg1926-1'            ,
                                    'xc7vx980tff1928-1'             ,
                                    'xc7vx980tffg1928-1'            ,
                                    'xc7vx980tff1930-1'             ,
                                    'xc7vx980tffg1930-1'            ,   

                                    'xc7vx1140tfl1926-1'            ,
                                    'xc7vx1140tflg1926-1'           ,
                                    'xc7vx1140tfl1928-1'            ,
                                    'xc7vx1140tflg1928-1'           ,
                                    'xc7vx1140tfl1930-1'            ,
                                    'xc7vx1140tflg1930-1'
                                )
        fpga_select.set("- Select your Virtex FPGA -")
        fpga_entry.grid_forget()
        fpga_select.grid(row=1, column=1, sticky=W+E)
    elif fpga_fam_selection.get() == "Autre" :
        fpga_select.grid_forget()
        fpga_entry.grid(row=1, column=1, sticky=W+E)
        



## Command file execution
def run_tmr_fctn() :
    #Extraction of path in the entry fields

    ##### XDC
    io_xdc_path_prj = entry_io_xdc_path_prj.get()
    if io_xdc_path_prj != "" :
        flag_io_field = True
    else :
        flag_io_field = False

    pad_xdc_path_prj = entry_pad_xdc_path_prj.get()
    if pad_xdc_path_prj != "" :
        flag_pad_field = True
    else :
        flag_pad_field = False

    timing_xdc_path_prj = entry_timing_xdc_path_prj.get()
    if timing_xdc_path_prj != "" :
        flag_timing_field = True
    else :
        flag_timing_field = False

    ##### TB
    tb_path_prj = entry_tb_path_prj.get()
    if tb_path_prj != "" :
        flag_tb_field = True
    else :
        flag_tb_field = False

    ##### XPR
    prj_from_vivado_path = entry_prj_vivado_path.get()
    if prj_from_vivado_path != "" :
        flag_xpr_field = True
    else :
        flag_xpr_field = False

    ##### OUTPUT DIR
    output_directory = entry_output_location.get()
    if output_directory != "" :
        flag_out_field = True
    else :
        flag_out_field = False


    ##### FPGA Target Name
    if fpga_fam_selection.get() == "Autre" :
        fpga_target_name = fpga_entry.get()
        flag_fpga_name = True
    else :
        fpga_target_name = fpga_select.get()
        
        if fpga_target_name == "- Select your Virtex FPGA -" :
            messagebox.showerror("FPGA Target Invalid","Please choose a valid FPGA target !")
            flag_fpga_name = False
        elif fpga_target_name == "- Select your Spartan FPGA -" :
            messagebox.showerror("FPGA Target Invalid","Please choose a valid FPGA target !")
            flag_fpga_name = False
        elif fpga_target_name == "- Select your Artix FPGA -" :
            messagebox.showerror("FPGA Target Invalid","Please choose a valid FPGA target !")
            flag_fpga_name = False
        elif fpga_target_name == "- Select your Kintex FPGA -" :
            messagebox.showerror("FPGA Target Invalid","Please choose a valid FPGA target !")
            flag_fpga_name = False
        else :
            flag_fpga_name = True
        
    if fpga_target_name != "" :
        flag_fpga_field = True
    else :
        flag_fpga_field = False


    #Start .cmd : for the moment only from .xpr

    
    if flag_fpga_field == True and flag_fpga_name == True and flag_io_field == True and flag_pad_field == True and flag_timing_field == True and flag_tb_field == True and flag_xpr_field == True and flag_xpr_field == True and flag_out_field == True:
        subprocess.Popen(['C:/Users/td264208/Desktop/test.cmd', prj_from_vivado_path, output_directory, fpga_target_name, io_xdc_path_prj, pad_xdc_path_prj, timing_xdc_path_prj, tb_path_prj])
    elif flag_fpga_name == True :
        messagebox.showwarning("Warning","Please, complete all the fields !")
    else :
        pass



def gen_script_fi() :
    prj_from_vivado_path = entry_prj_vivado_path.get()
    print(prj_from_vivado_path)
    path = re.split(r'[/]', prj_from_vivado_path)
    path[-1] = 'temp/'
    prj_from_vivado_path = '/'.join(path)
    print("arg 1 : ", prj_from_vivado_path + 'tb_top.vhd')
    print("arg 2 : ", prj_from_vivado_path + 'test4.tcl')
    subprocess.Popen(['python','C:/Users/td264208/Desktop/NMR.PY/faultInjection.py', prj_from_vivado_path + 'tb_top.vhd', prj_from_vivado_path + 'test4.tcl'])




###########################################################################################





###### Widgets ######
#Frame
frame_project = LabelFrame(second_frame, text="Importer Projet")
frame_project.pack(fill=X, padx=10, pady=10)

frame_output_location = LabelFrame(frame_project, text="Output Files Location")
frame_output_location.grid(row=14, column=0, columnspan=4, sticky=W+E, padx=10, pady=10)

frame_config = LabelFrame(second_frame, text="Target (FPGA)")
frame_config.pack(fill=X, padx=10, pady=10)

frame_run = LabelFrame(second_frame, text="Redundancy")
frame_run.pack(fill=X, padx=10, pady=10)



#Responsive Frames

#Grid.rowconfigure(second_frame, 1, weight=1)
#Grid.columnconfigure(second_frame, 1, weight=1)
Grid.rowconfigure(frame_project, 1, weight=1)
Grid.columnconfigure(frame_project, 1, weight=1)
Grid.rowconfigure(frame_output_location, 1, weight=1)
Grid.columnconfigure(frame_output_location, 1, weight=1)
Grid.rowconfigure(frame_config, 1, weight=1)
Grid.columnconfigure(frame_config, 1, weight=1)


######## Project
        #VIVADO Project
Label(frame_project, text="Vivado project Path : ").grid(row=0, column=0, sticky=W, padx=40)
entry_prj_vivado_path = Entry(frame_project, width=29)
entry_prj_vivado_path.grid(row=0, column=1, sticky=W+E)
btn_xpr_file = Button(frame_project, text="Browse...", command=lambda: import_files_prj("XPR"))
btn_xpr_file.grid(row=0, column=2, padx=10, sticky=E)
btn_xpr_info = Button(frame_project, text="?", command=lambda: popup_info_prj("XPR"))
btn_xpr_info.grid(row=0, column=3, padx=15, pady=5, sticky=E)


        ###### CONSTRAINTS FILES PATH
Label(frame_project, text="Constraints File Paths : ").grid(row=1, column=0, sticky=W, padx=40, pady=(15,5))
        #Constraints PATH : IO_properties
Label(frame_project, text="IO properties : ").grid(row=2, column=0, sticky=W, padx=80)
entry_io_xdc_path_prj = Entry(frame_project, width=29)
entry_io_xdc_path_prj.grid(row=2, column=1, sticky=W+E) 
btn_io_xdc_file_prj = Button(frame_project, text="Browse...", command=lambda: import_files_prj("XDC_IO_PRJ"))
btn_io_xdc_file_prj.grid(row=2, column=2, padx=10, sticky=E)
btn_io_xdc_info_prj = Button(frame_project, text="?", command=lambda: popup_info_prj("XDC_IO_PRJ"))
btn_io_xdc_info_prj.grid(row=2, column=3, padx=15, sticky=E)
        #Constraints PATH : pad_location
Label(frame_project, text="Pad Location : ").grid(row=3, column=0, sticky=W, padx=80)
entry_pad_xdc_path_prj = Entry(frame_project, width=29,)
entry_pad_xdc_path_prj.grid(row=3, column=1, sticky=W+E) 
btn_pad_xdc_file_prj = Button(frame_project, text="Browse...", command=lambda: import_files_prj("XDC_PAD_PRJ"))
btn_pad_xdc_file_prj.grid(row=3, column=2, padx=10, sticky=E)
btn_pad_xdc_info_prj = Button(frame_project, text="?", command=lambda: popup_info_prj("XDC_PAD_PRJ"))
btn_pad_xdc_info_prj.grid(row=3, column=3, padx=15, sticky=E)
        #Constraints PATH : timing
Label(frame_project, text="Timing : ").grid(row=4, column=0, sticky=W, padx=80)
entry_timing_xdc_path_prj = Entry(frame_project, width=29)
entry_timing_xdc_path_prj.grid(row=4, column=1, sticky=W+E) 
btn_timing_xdc_file_prj = Button(frame_project, text="Browse...", command=lambda: import_files_prj("XDC_TIMING_PRJ"))
btn_timing_xdc_file_prj.grid(row=4, column=2, padx=10, sticky=E)
btn_timing_xdc_info_prj = Button(frame_project, text="?", command=lambda: popup_info_prj("XDC_TIMING_PRJ"))
btn_timing_xdc_info_prj.grid(row=4, column=3, padx=15, sticky=E)


        #TB PATH
Label(frame_project, text="Test Bench Files Path : ").grid(row=5, column=0, sticky=W, padx=40, pady=20,)
entry_tb_path_prj = Entry(frame_project, width=29)
entry_tb_path_prj.grid(row=5, column=1, sticky=W+E, pady=20,)
btn_tb_file_prj = Button(frame_project, text="Browse...", command=lambda: import_files_prj("TB_prj"))
btn_tb_file_prj.grid(row=5, column=2, padx=10, pady=20, sticky=E)
btn_tb_info_prj = Button(frame_project, text="?", command=lambda: popup_info_prj("TB_prj"))
btn_tb_info_prj.grid(row=5, column=3, padx=15, pady=20, sticky=E)



    #Output files folder
Label(frame_output_location, text="Output Files Folder Location : ").grid(row=0, column=0, sticky=W, padx=(40,20), pady=20)
entry_output_location = Entry(frame_output_location, width=34)
entry_output_location.grid(row=0, column=1, sticky=W+E)
btn_output_location_file = Button(frame_output_location, text="Browse...", command=lambda: import_files_prj("OUTPUT"))
btn_output_location_file.grid(row=0, column=2, padx=10, sticky=E)
btn_output_location_info = Button(frame_output_location, text="?", command=lambda: popup_info_prj("OUTPUT"))
btn_output_location_info.grid(row=0, column=3, padx=8, pady=5, sticky=E)



###### Config
# FPGA FAMILY SELECTION
fpga_fam_list=["- Select your FPGA Family -","Artix-7 FPGA","Kintex-7 FPGA","Spartan-7 FPGA","Virtex-7 FPGA","Autre"]
Label(frame_config, text="Targeted FPGA - Family : ").grid(row=0, column=0, sticky=W, padx=(40,60), pady=10)
fpga_fam_selection = ttk.Combobox(frame_config, values=fpga_fam_list, width=40)
fpga_fam_selection.grid(row=0, column=1, sticky=E+W)
fpga_fam_selection.bind('<<ComboboxSelected>>', fpga_selection)
Label(frame_config, text=" ").grid(row=0, column=2, sticky=E, padx=25)
Label(frame_config, text=" ").grid(row=0, column=3, sticky=E, padx=25)
#FPGA TARGET SELECTION
Label(frame_config, text="Targeted FPGA : ").grid(row=1, column=0, sticky=W, padx=(40,60), pady=10)
fpga_select = ttk.Combobox(frame_config, width=40)
fpga_select.grid(row=1, column=1, sticky=E+W)
fpga_entry = Entry(frame_config, width=30)
Label(frame_config, text=" ").grid(row=1, column=2, sticky=E, padx=25)
Label(frame_config, text=" ").grid(row=1, column=3, sticky=E, padx=25)



###### Run

def button_hover_quit(event) :
    btn_quit['bg'] = "white"
    status_lbl.config(text="Quit TMR Software")

def button_hover_quit_leave(event) :
    btn_quit['bg'] = "SystemButtonFace"
    status_lbl.config(text="")


def button_hover_simu(event) :
    btn_gen_script_fi['bg'] = "white"
    status_lbl.config(text="Generate a new injection fault script to run a new post-implementation simulation")
    

def button_hover_simu_leave(event) :
    btn_gen_script_fi['bg'] = "SystemButtonFace"
    status_lbl.config(text="")


def button_hover_run(event) :
    btn_run_tmr['bg'] = "white"
    status_lbl.config(text="Run redundancy (TMR) and implemente it in the FPGA")
    

def button_hover_run_leave(event) :
    btn_run_tmr['bg'] = "SystemButtonFace"
    status_lbl.config(text="")


#Button Run TMR
btn_run_tmr = Button(frame_run, text="Run TMR", command=run_tmr_fctn, padx=25, pady=5)
btn_run_tmr.grid(row=0, column=1, sticky=E, padx=(350,20), pady=20)
btn_run_tmr.bind("<Enter>", button_hover_run)
btn_run_tmr.bind("<Leave>", button_hover_run_leave)

#Button Run Simulation Post Implem
btn_gen_script_fi = Button(frame_run, text="Gen FI script", command=gen_script_fi, padx=25, pady=5)
btn_gen_script_fi.grid(row=0, column=2, sticky=E, padx=(10,20), pady=20)
btn_gen_script_fi.bind("<Enter>", button_hover_simu)
btn_gen_script_fi.bind("<Leave>", button_hover_simu_leave)


#Button Quit
btn_quit = Button(frame_run, text="Exit", command=root.quit, padx=25, pady=5)
btn_quit.grid(row=0, column=3, sticky=E, padx=10, pady=20)
btn_quit.bind("<Enter>", button_hover_quit)
btn_quit.bind("<Leave>", button_hover_quit_leave)


#Status Label
status_lbl = Label(second_frame, text="", bd=1, relief=SUNKEN, anchor=E)
status_lbl.pack(fill=X, side=BOTTOM, ipady=2)

root.mainloop()
