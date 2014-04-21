import tkinter as tk

class MainView(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.main_frame = tk.Frame(self,height=200, width=400, bd=3)           
        self.main_frame.grid(sticky=tk.NW,row=0,column=0)
        self.main_frame.grid_propagate(0)
        
    def createWidgets(self):        
        self.createclasses_button = tk.Button(self.main_frame,text='Create New Classes')
        self.createclasses_button.grid(sticky=tk.NW,row=0,column=0)
        
        self.createprops_button = tk.Button(self.main_frame, text='Create New Class Properties')
        self.createprops_button.grid(sticky=tk.NW,row=1,column=0)
        
        self.addrecords_button = tk.Button(self.main_frame, text='Create New Records')
        self.addrecords_button.grid(sticky=tk.NW,row=2,column=0)
        
        self.updatesvc_button = tk.Button(self.main_frame, text='Update ServiceIds')
        self.updatesvc_button.grid(sticky=tk.NW,row=3,column=0)