import tkinter as tk

class MainView(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)        
    
class ButtonFrame:
    def __init__(self,frame,title,row,column):
        self.button_frame = tk.Frame(frame,bd=4,relief="groove")
        self.button_frame.grid(sticky=tk.N+tk.S+tk.E+tk.W,row=row,column=column)
        frame.rowconfigure(row,weight=1)
        frame.columnconfigure(column,weight=1)      
        if title != None:
            self.title = tk.Label(self.button_frame,text=title,fg="blue")
            self.title.grid(row=0,column=0)
            
    def createButton(self,name):
        if "button" not in self.__dict__.keys():
            self.button = {}
        rowind = self.button_frame.grid_size()[1]
        self.button[name] = tk.Button(self.button_frame,text=name)
        self.button[name].grid(sticky=tk.W+tk.E,row=rowind+1,column=0)
        
class ViewRecordFrame:
    def __init__(self,frame,title,row,column):
        self.view_frame = tk.Frame(frame,bd=4,relief="groove")
        self.view_frame.grid(sticky=tk.N+tk.S+tk.E+tk.W,row=row,column=column)
        frame.rowconfigure(row,weight=1)
        frame.columnconfigure(column,weight=1)      
        if title != None:
            self.title = tk.Label(self.view_frame,text=title,fg="blue")
            self.title.grid(row=0,column=0,columnspan=2)
            
    def createLblMenu(self,menufields,menuvalues):
        self.menulabelwidgets = {}
        self.menuvars = {}        
        self.menus = {}
        rowind = self.view_frame.grid_size()[1]
        for i, fieldname in enumerate(menufields):
            rowind += 1            
            self.menulabelwidgets[fieldname] = tk.Label(self.view_frame,text=fieldname + ": ")
            self.menulabelwidgets[fieldname].grid(sticky=tk.W+tk.E,row=rowind,column=0)
            self.menuvars[fieldname] = tk.StringVar()            
            self.menus[fieldname] = tk.OptionMenu(self.view_frame,self.menuvars[fieldname],*menuvalues[i])
            self.menus[fieldname].grid(sticky=tk.W+tk.E,row=rowind,column=1)
        self.view_frame.columnconfigure(0, weight=1)
        self.view_frame.columnconfigure(1, weight=1)
            
    def createButton(self,name):
        if "button" not in self.__dict__.keys():
            self.button = {}
        rowind = self.view_frame.grid_size()[1]
        self.button[name] = tk.Button(self.view_frame,text=name)
        self.button[name].grid(sticky=tk.W+tk.E,row=rowind+1,column=0,columnspan=2)
    
    def createCanvas(self,name):
        if "canvas" not in self.__dict__.keys():
            self.canvas = {}
            self.scroll = {}
        rowind = self.view_frame.grid_size()[1]
        self.scroll[name] = tk.Scrollbar(self.view_frame,orient=tk.VERTICAL)
        self.scroll[name].grid(sticky=tk.NE+tk.SE,row=rowind+1,column=2)
        self.canvas[name] = tk.Canvas(self.view_frame,relief=tk.RIDGE,bd=2,yscrollcommand=self.scroll[name].set)
        self.scroll[name]["command"] = self.canvas[name].yview        
        self.canvas[name].grid(sticky=tk.N+tk.S,row=rowind+1,column=0,columnspan=2)
        self.view_frame.rowconfigure(rowind+1, weight=1)
        self.view_frame.columnconfigure(0, weight=1)
        
    def updateCanvas(self,name,text):
        for Id in self.canvas[name].find_all():
            self.canvas[name].delete(Id)
        self.canvas[name].create_text(0,0,anchor=tk.NW,text=text)
        self.canvas[name]["scrollregion"] = self.canvas[name].bbox(tk.ALL)
        
class QueryFrame:
    def __init__(self,frame,title,row,column):
        self.query_frame = tk.Frame(frame,bd=4,relief="groove")
        self.query_frame.grid(sticky=tk.N+tk.S+tk.E+tk.W,row=row,column=column)
        frame.rowconfigure(row,weight=1)
        frame.columnconfigure(column,weight=1)      
        if title != None:
            self.title = tk.Label(self.query_frame,text=title,fg="blue")
            self.title.grid(row=0,column=0,columnspan=2)
    
    def createLblText(self,name,value):
        if "textbox" not in self.__dict__.keys():
            self.textlabel = {}
            self.textbox = {}
        rowind = self.query_frame.grid_size()[1]
        self.textlabel[name] = tk.Label(self.query_frame,text=name + ": ")
        self.textlabel[name].grid(sticky=tk.W+tk.E,row=rowind,column=0)
        self.textbox[name] = tk.Text(self.query_frame)
        self.textbox[name].insert(tk.INSERT,value)
        self.textbox[name].grid(sticky=tk.W+tk.E,row=rowind,column=1)
        
    def createButton(self,name):
        if "button" not in self.__dict__.keys():
            self.button = {}
        rowind = self.query_frame.grid_size()[1]
        self.button[name] = tk.Button(self.query_frame,text=name)
        self.button[name].grid(sticky=tk.W+tk.E,row=rowind+1,column=0,columnspan=2)
    