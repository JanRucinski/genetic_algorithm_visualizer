#a class responsible for the simulation
from decimal import ROUND_UP
from random import randrange
from re import L
from textwrap import wrap
import time
from tkinter import messagebox


import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from math import ceil

from Specimen import *
from Specimen_handler import *


def ceil_to_tens(x):
    return int(ceil(x / 10.0)) * 10

wdt = 400
hgt = 400

def scroll_y(*args):
    global canvas1, canvas2, canvas3
    canvas1.yview(*args)
    canvas2.yview(*args)
    canvas3.yview(*args)

class main(Frame):

    def __init__(self, master = None):
        self.root = master
        self.root.title("genetic algorithm ilustrator")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.close = True
                self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        self.running = False
        self.close = False
        self.is_initialized = False
        self.population_size = tk.IntVar()
        self.specimen_handler = SpecimenHandler()

        self.size_of_osobnik = 40
        self.target = Specimen(0)
        self.iteration_counter = 0
        self.found_first = False
        self.pad_after_table = 0
        self.control_panel_width = 200
        self.control_panel_height = 200
        self.flag_for_warunkowy_start = False
        self.flag_warunek_first = True
        self.warunek = IntVar()
        self.warunek.set(0)

        self.run()
        pass

    def run(self):
        counter = self.iteration_counter
        
        self.draw_master_frame()

        while(counter<1000):
            if(self.running and self.flag_for_warunkowy_start and counter > self.warunek.get() and self.flag_warunek_first):
                self.stop_button_command()
                self.flag_warunek_first = False
            if(self.close):
                break
            if(self.running):
                self.iterate()
                time.sleep(0.1)
                counter+=1
            self.root.update()
        pass

    def draw_master_frame(self):
        try:
            self.master_frame.destroy()
        except:
            pass
        self.master_frame = Frame(self.root)
        master_frame = self.master_frame

        self.create_status()

        self.information_and_control_frame = Frame(master_frame)
        information_and_control_frame = self.information_and_control_frame

        self.iteration_counter_frame = Frame(information_and_control_frame, width=40, height=40)

        control_frame = Frame(information_and_control_frame, width=40, height=40)
        self.populations_frame = Frame(master_frame, width=100, height=40)
        populations_frame = self.populations_frame

        information_and_control_frame.pack(side=TOP, fill=BOTH, expand=TRUE)
        control_frame.pack(side=LEFT, fill=Y)
        populations_frame.pack(side=BOTTOM, fill=X)

        master_frame.pack(expand=True, fill=BOTH)

        self.draw_control(control_frame)
        pass
    

    def start_button_command(self):

        if (self.warunek.get() > 0):
            self.flag_for_warunkowy_start = True
        else:
            self.flag_for_warunkowy_start = False

        if(not self.is_initialized):
            self.initialize()
        if(self.is_initialized):
            self.running = True
            self.stop_button['state'] = 'normal'
            self.start_button['state'] = 'disabled'

            self.spin_box['state'] = 'disabled'
        pass

    def stop_button_command(self):
        self.running = False
        self.start_button['state'] = 'normal'

        self.stop_button['state'] = 'disabled'
        self.reset_button['state'] = 'normal'

        self.specimen_handler.write_history_of_found_to_file('history_of_best.txt')
        pass

    def reset_button_command(self):
        self.iteration_counter = 0
        self.is_initialized = False

        self.target = Specimen(0)

        self.found_first = False
        self.spin_box['state'] = 'normal'
        self.running = False
        self.flag_for_warunkowy_start = False
        self.flag_warunek_first = True
        self.root.update()

        self.run()
        pass


    def draw_control(self, frame):

        control_frame = Frame(frame, width= self.control_panel_width, height= self.control_panel_height)

        self.start_button = tk.Button(control_frame, text='start', command= self.start_button_command)
        start_button = self.start_button
        start_button.pack(fill='x')

        self.stop_button = tk.Button(control_frame, text='stop', command= self.stop_button_command, state='disabled')
        stop_button = self.stop_button
        stop_button.pack(fill='x')

        self.reset_button = tk.Button(control_frame, text='reset', command= self.reset_button_command, state='disabled')
        reset_button = self.reset_button
        reset_button.pack(fill='x')

        populacja_label = tk.Label(control_frame, text='Population:')
        populacja_label.pack()


        self.spin_box = ttk.Spinbox(control_frame, from_=0, to=50, values=(10, 20, 30, 40, 50, 100), 
            textvariable=self.population_size, wrap=True)
        spin_box = self.spin_box
        spin_box.pack()
    
        #create warunek_label
        warunek_label = tk.Label(control_frame, text='Ilość iteracji (opcjonalne):')
        warunek_label.pack()

        #create self.warunek_box
        self.warunek_box = ttk.Spinbox(control_frame, values=(10, 20, 30, 40, 50),
            textvariable=self.warunek, wrap=True)
        warunek_box = self.warunek_box
        warunek_box.pack()

        control_frame.grid(column=2, row=0 ,sticky=NE)


    def initialize(self): #modified
        target = self.target
        population_size = self.population_size.get()

        if(population_size < 2):
            print("za mała populacja")
            self.setStatusBar("za mała populacja")
        else:
            self.specimen_handler = SpecimenHandler(target, population_size= population_size)
            self.is_initialized = True

    def iterate(self): 
        self.specimen_handler.iterate()
    
        self.draw_osobniki_scrollbar(self.populations_frame)
        self.draw_wskazniki_osobnikow_scrollbar(self.populations_frame)
        self.draw_osobniki_start_scrollbar(self.populations_frame)

        try:
            for widget in self.iteration_counter_frame.winfo_children():
                widget.destroy()
            self.iteration_counter_frame.destroy()
        except:
            pass

        self.iteration_counter_frame = Frame(self.information_and_control_frame, width=40, height=40)
        iteration_counter_frame = self.iteration_counter_frame
        Label(iteration_counter_frame, text="Iteration (generation) number:").pack()
        Label(iteration_counter_frame, text= self.iteration_counter).pack()
        iteration_counter_frame.pack(side=LEFT)

        self.root.update()
        self.iteration_counter += 1
        pass

    def draw_osobniki_scrollbar(self, frame):
        size = self.size_of_osobnik
        specimens = self.specimen_handler.get_specimens()
        population = self.specimen_handler.get_population_size()
        global canvas1

        for widget in frame.winfo_children():
            widget.destroy()
        frame.pack(fill=BOTH, expand=True)


        self.canvas=Canvas(frame,bg='#FFFFFF', scrollregion=(0,0,500,500))
        canvas = self.canvas
        canvas1 = canvas
        self.vbar=Scrollbar(frame,orient=VERTICAL)
        vbar = self.vbar
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=scroll_y)
        canvas.config(width=10 * size,height= 200)
        canvas.config(yscrollcommand=vbar.set)
        counter = 0
        found_specimens = []

        
        self.draw_target_and_best()

        final_hgt = 0
        i=0
        while(True):
            if(final_hgt > 0):
                break
            for j in range((int)(hgt/size) ):
                if(counter<population):
                    canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill=specimens[counter].getToRgb())
                    if(specimens[counter].getToRgb() == self.target.getToRgb()):
                        found = canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill=specimens[counter].getToRgb(), outline=specimens[counter].negative_color())
                        found_specimens.append(found)
                        self.found_perfect()

                    counter += 1
                else:
                    final_hgt = i*size
                    break
            i+=1
        for specimen in found_specimens:
            canvas.tag_raise(specimen)

        canvas.config(scrollregion= canvas.bbox("all"))
        canvas.pack(side=LEFT,expand=True,fill=BOTH)
        pass

    def draw_target_and_best(self):
        size = self.size_of_osobnik

        try:
            self.frame_for_target.destroy()
        except:
            pass

        try:
            self.frame_for_best.destroy()
        except:
            pass

        self.frame_for_target = Frame(self.information_and_control_frame, width=40, height=40)
        self.frame_for_best = Frame(self.information_and_control_frame, width=40, height=40)

        frame_for_target = self.frame_for_target
        frame_for_best = self.frame_for_best

        Label(frame_for_target, text="Target:").pack()
        Label(frame_for_best, text="Current Best:").pack()

        canvas_target = Canvas(frame_for_target, width=size, height=size)
        canvas_best = Canvas(frame_for_best, width=size, height=size)
        
        target = self.target
        best = self.specimen_handler.get_best_specimen()

        canvas_target.create_rectangle(0, 0, size, size, fill=target.getToRgb())
        canvas_target.pack()
        canvas_best.create_rectangle(0, 0, size, size, fill=best.getToRgb())
        canvas_best.pack()

        Label(frame_for_target, text=target.rgb_to_string()).pack()
        Label(frame_for_best, text=best.rgb_to_string()).pack()

        frame_for_target.pack(side=LEFT)
        frame_for_best.pack(side=LEFT)
        pass

  
    def draw_wskazniki_osobnikow_scrollbar(self, frame):
        size = self.size_of_osobnik
        specimens = self.specimen_handler.get_specimens()
        
        global canvas2
        canvas2 = frame

        frame.pack(fill=BOTH, expand=True)

        self.canvas_wskaznik=Canvas(frame,bg='#FFFFFF', scrollregion=(0,0,500,500))
        canvas = self.canvas_wskaznik
        canvas2 = canvas

        vbar = self.vbar
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=(scroll_y))
        canvas.config(width=10 * size,height= 200)
        canvas.config(yscrollcommand=vbar.set)
        counter = 0
        found_specimens = []

        final_hgt = 0
        i=0
        while(True):
            if(final_hgt > 0):
                break

            for j in range((int)(hgt/size) ):
                if(counter<specimens.__len__()):
                    canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill=specimens[counter].getToRgbStren())

                    if(specimens[counter].getToRgb() == self.target.getToRgb()):
                        found = canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill=specimens[counter].getToRgbStren(), outline=specimens[counter].negative_color())
                        found_specimens.append(found)

                    counter += 1

                else:
                    final_hgt = i*size
                    break
            i+=1
        
        for specimen in found_specimens:
            canvas.tag_raise(specimen)
        
        canvas.config(scrollregion= canvas.bbox("all"))
        canvas.pack(side=LEFT,expand=True,fill=BOTH)
        pass

    
   
    def draw_osobniki_start_scrollbar(self, frame):
        size = self.size_of_osobnik
        specimens = self.specimen_handler.get_start_specimens()
        specimens_modified = self.specimen_handler.get_specimens()

        global canvas3

        frame.pack(fill=BOTH, expand=True)

        self.canvas_start=Canvas(frame,bg='#FFFFFF')
        canvas = self.canvas_start
        canvas3 = canvas
        canvas.config(width=10 * size,height= 200)
        canvas.config(scrollregion= (0,0,500,500))
        counter = 0
        found_specimens = []

        final_hgt = 0
        i=0
        while(True):
            if(final_hgt > 0):
                break

            for j in range((int)(hgt/size) ):
                if(counter<specimens.__len__()):
                    canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill=specimens[counter].getToRgb())

                    if (specimens_modified[counter].getToRgb() == self.target.getToRgb()):
                        found = canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill=specimens[counter].getToRgb(), outline=self.target.negative_color())
                        found_specimens.append(found)

                    counter += 1
                else:
                    final_hgt = i*size
                    break
            i+=1

        for specimen in found_specimens:
            canvas.tag_raise(specimen)

        canvas.config(scrollregion= canvas.bbox("all"))
        canvas.pack(side=LEFT,expand=True,fill=BOTH)
        pass

    def found_perfect(self):
        if(self.found_first):
            return

        self.found_first = True
        self.stop_button_command()
        self.open_popup()


    def open_popup(self):
        top= Toplevel()
        top.geometry("400x50")
        top.title("Found perfect")
        Label(top, text= ("Perfect specimen found in: " + str(self.iteration_counter) + " generations" )).pack()
       
        def exit_btn():
            top.destroy()
            top.update()

        Button(top, text= 'ok', command= exit_btn ).pack()
        
    
    def create_status(self):
        self.statusbar = tk.Label(self.master_frame, text="Welcome",
                                       anchor=tk.W)
        self.statusbar.after(1000, self.clearStatusBar)
        self.statusbar.pack(side=BOTTOM)
        pass
    
    def setStatusBar(self, txt):
        self.statusbar["text"] = txt
        self.statusbar.after(1000, self.clearStatusBar)
        
    def clearStatusBar(self):
        self.statusbar["text"] = ""



if __name__ == '__main__':
    root = tk.Tk()
    app = main(master=root)
    pass