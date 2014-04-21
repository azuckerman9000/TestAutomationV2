import tkinter as tk

class MainView(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.main_frame = tk.Frame(self,bd=3)           
        self.main_frame.grid(sticky=tk.NW,row=0,column=0)
        #self.main_frame.grid_propagate(0)

class InputFrame:
    def __init__(self,frame,title,row,column):
        self.input_frame = tk.Frame(frame,bd=4,relief="groove")
        self.input_frame.grid(sticky=tk.N+tk.E+tk.S+tk.W,row=row,column=column)
        if title != None:
            self.title = tk.Label(self.input_frame,text=title)
            self.title.grid(row=0,column=0,columnspan=2)
    
    def createLblMenu(self,menufields,menuvalues):
        self.menulabelwidgets = {}
        self.menuvars = {}        
        self.menus = {}
        rowind = self.input_frame.grid_size()[1]
        for i, fieldname in enumerate(menufields):
            rowind += 1            
            self.menulabelwidgets[fieldname] = tk.Label(self.input_frame,text=fieldname + ": ")
            self.menulabelwidgets[fieldname].grid(sticky=tk.E,row=rowind,column=0)
            self.menuvars[fieldname] = tk.StringVar()            
            self.menus[fieldname] = tk.OptionMenu(self.input_frame,self.menuvars[fieldname],*menuvalues[i])
            self.menus[fieldname].grid(sticky=tk.W+tk.E,row=rowind,column=1)    
            
    def createLblCheckbox(self,labels):
        self.checklabelwidgets = {}
        self.checkvars = {}
        self.checkboxes = {}
        rowind = self.input_frame.grid_size()[1]
        for label in labels:
            rowind += 1
            self.checklabelwidgets[label] = tk.Label(self.input_frame,text=label + ": ")
            self.checklabelwidgets[label].grid(sticky=tk.E,row=rowind,column=0)
            self.checkvars[label] = tk.StringVar()
            self.checkboxes[label] = tk.Checkbutton(self.input_frame,text=label,variable=self.checkvars[label],onvalue=label,offvalue="")
            self.checkboxes[label].grid(sticky=tk.W+tk.E,row=rowind,column=1)
            
    def createButton(self,name):
        if "button" not in self.__dict__.keys():
            self.button = {}
        rowind = self.input_frame.grid_size()[1]
        self.button[name] = tk.Button(self.input_frame,text=name)
        self.button[name].grid(sticky=tk.W+tk.E,row=rowind+1,column=0)
        
    def createListbox(self,name):
        if "listbox" not in self.__dict__.keys():
            self.listvar = {}
            self.scroll = {}
            self.listbox = {}
        self.listvar[name] = tk.StringVar()
        rowind = self.input_frame.grid_size()[1]
        self.scroll[name] = tk.Scrollbar(self.input_frame,orient=tk.VERTICAL)
        self.scroll[name].grid(sticky=tk.NW+tk.SW,row=rowind+1,column=1)
        self.listbox[name] = tk.Listbox(self.input_frame,listvariable=self.listvar[name],activestyle="dotbox",yscrollcommand=self.scroll[name].set)
        self.listbox[name].grid(sticky=tk.W,row=rowind+1,column=0)
        self.scroll[name]["command"] = self.listbox[name].yview
        
    def updateListbox(self,name,selectionlist):
        temp = ""
        length = 20
        for item in sorted(selectionlist):
            temp += item + " "
            if len(item) > length:
                length = len(item)            
        self.listvar[name].set(temp)
        self.listbox[name]["width"] = length+1
        
    def createCanvas(self,name,disptext):
        if "canvas" not in self.__dict__.keys():
            self.canvas = {}
        rowind = self.input_frame.grid_size()[1]
        self.canvas[name] = tk.Canvas(self.input_frame,relief=tk.RIDGE,bd=2)
        self.canvas[name].create_text(0,0,anchor=tk.NW,text=disptext)
        self.canvas[name].grid(sticky=tk.W,row=rowind+1,column=0)
"""            
     def createLblMenu(self,menufields,menuvalues):       
        self.menulabelwidgets = {}
        self.menuvars = {}
        self.menuitemvars = {}
        self.menubuttons = {}
        rowind = self.menu_frame.grid_size()[1]       
        for i, fieldname in enumerate(menufields):
            rowind += 1            
            self.menulabelwidgets[fieldname] = tk.Label(self.menu_frame,text=fieldname + ": ")
            self.menulabelwidgets[fieldname].grid(sticky=tk.W,row=rowind,column=0)
            self.menuvars[fieldname] = tk.StringVar()
            self.menuvars[fieldname].set(fieldname)
            self.menubuttons[fieldname] = tk.Menubutton(self.menu_frame,relief="raised",textvariable=self.menuvars[fieldname])
            self.menubuttons[fieldname].grid(sticky=tk.W,row=rowind,column=1)
            self.menubuttons[fieldname].menu = tk.Menu(self.menubuttons[fieldname])
            self.menubuttons[fieldname]["menu"] = self.menubuttons[fieldname].menu            
            self.menuitemvars[fieldname] = tk.StringVar()
            for value in menuvalues[i]:                
                self.menubuttons[fieldname].menu.add_checkbutton(label=value,variable=self.menuitemvars[fieldname],onvalue=value,offvalue="",command=self.updateMenuButton)
"""            