import tkinter as tk

class MainView(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)

class InputFrame:
    def __init__(self,frame,title,row,column):
        self.input_frame = tk.Frame(frame,bd=4,relief="groove")
        self.input_frame.grid(sticky=tk.N+tk.S+tk.E+tk.W,row=row,column=column)
        frame.rowconfigure(row,weight=1)
        frame.columnconfigure(column,weight=1)      
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
            self.checkvars[label].set("False")
            self.checkboxes[label] = tk.Checkbutton(self.input_frame,text=label,variable=self.checkvars[label],onvalue="True",offvalue="False")
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
        self.scroll[name].grid(sticky=tk.NE+tk.SE,row=rowind+1,column=1)
        self.listbox[name] = tk.Listbox(self.input_frame,listvariable=self.listvar[name],activestyle="dotbox",yscrollcommand=self.scroll[name].set)
        self.scroll[name]["command"] = self.listbox[name].yview
        self.listbox[name].grid(sticky=tk.N+tk.S+tk.E+tk.W,row=rowind+1,column=0)
        self.input_frame.rowconfigure(rowind+1, weight=1)
        self.input_frame.columnconfigure(0, weight=1)
        self.input_frame.columnconfigure(1, weight=1)              
                
        
    def updateListbox(self,name,selectionlist):        
        temp = ""
        length = 20
        for item in sorted(selectionlist):
            temp += item + " "
            if len(item) > length:
                length = len(item)            
        self.listvar[name].set(temp)
        self.listbox[name]["width"] = length+10
        
    def createCanvas(self,name):
        if "canvas" not in self.__dict__.keys():
            self.canvas = {}
            self.scroll = {}
        rowind = self.input_frame.grid_size()[1]
        self.scroll[name] = tk.Scrollbar(self.input_frame,orient=tk.VERTICAL)
        self.scroll[name].grid(sticky=tk.NE+tk.SE,row=rowind+1,column=1)
        self.canvas[name] = tk.Canvas(self.input_frame,relief=tk.RIDGE,bd=2,yscrollcommand=self.scroll[name].set)
        self.scroll[name]["command"] = self.canvas[name].yview        
        self.canvas[name].grid(sticky=tk.N+tk.S,row=rowind+1,column=0)
        self.input_frame.rowconfigure(rowind+1, weight=1)
        self.input_frame.columnconfigure(0, weight=1)
        
    def updateCanvas(self,name,text):
        for Id in self.canvas[name].find_all():
            self.canvas[name].delete(Id)
        self.canvas[name].create_text(0,0,anchor=tk.NW,text=text)
        self.canvas[name]["scrollregion"] = self.canvas[name].bbox(tk.ALL)

class MerchantFrame:
    def __init__(self,frame,title,row,column):
        self.merch_frame = tk.Frame(frame,bd=4,relief="groove")
        self.merch_frame.grid(sticky=tk.N+tk.S+tk.E+tk.W,row=row,column=column)
        frame.rowconfigure(row,weight=1)
        frame.columnconfigure(column,weight=1)      
        if title != None:
            self.title = tk.Label(self.merch_frame,text=title)
            self.title.grid(row=0,column=0,columnspan=3)
            
    def createButton(self,name,row,column):
        if "button" not in self.__dict__.keys():
            self.button = {}                       
        self.button[name] = tk.Button(self.merch_frame,text=name)
        self.button[name].grid(sticky=tk.W+tk.E,row=row,column=column)
        
    def createListbox(self,name,row,column):        
        if "listbox" not in self.__dict__.keys():
            self.listvar = {}
            self.scroll = {}
            self.listbox = {}                
        self.listvar[name] = tk.StringVar()        
        self.scroll[name] = tk.Scrollbar(self.merch_frame,orient=tk.VERTICAL)
        self.scroll[name].grid(sticky=tk.NE+tk.SE,row=row,column=column+3)
        self.listbox[name] = tk.Listbox(self.merch_frame,listvariable=self.listvar[name],activestyle="dotbox",yscrollcommand=self.scroll[name].set)
        self.scroll[name]["command"] = self.listbox[name].yview
        self.listbox[name].grid(sticky=tk.N+tk.S+tk.E+tk.W,row=row,column=column,columnspan=3)
        self.merch_frame.rowconfigure(row, weight=1)
        self.merch_frame.columnconfigure(column, weight=1)
        self.merch_frame.columnconfigure(column+1, weight=1)
        self.merch_frame.columnconfigure(column+2, weight=1)               
        
    def updateListbox(self,name,selectionlist):        
        temp = ""
        length = 20
        for item in sorted(selectionlist):
            temp += item + " "
            if len(item) > length:
                length = len(item)            
        self.listvar[name].set(temp)
        self.listbox[name]["width"] = length+10
        
    def createCanvas(self,name):
        if "canvas" not in self.__dict__.keys():
            self.canvas = {}
            self.scroll = {}
        colind = self.merch_frame.grid_size()[0]
        rowind = self.merch_frame.grid_size()[1]
        self.scroll[name] = tk.Scrollbar(self.merch_frame,orient=tk.VERTICAL)
        self.scroll[name].grid(sticky=tk.NE+tk.SE,row=0,column=colind+2,rowspan=rowind)
        self.canvas[name] = tk.Canvas(self.merch_frame,relief=tk.RIDGE,bd=2,yscrollcommand=self.scroll[name].set)
        self.scroll[name]["command"] = self.canvas[name].yview        
        self.canvas[name].grid(sticky=tk.N+tk.S,row=0,column=colind+1,rowspan=rowind)
        
    def updateCanvas(self,name,text):
        for Id in self.canvas[name].find_all():
            self.canvas[name].delete(Id)
        self.canvas[name].create_text(0,0,anchor=tk.NW,text=text)
        self.canvas[name]["scrollregion"] = self.canvas[name].bbox(tk.ALL) 