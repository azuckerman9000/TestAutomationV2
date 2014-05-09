from automation import dataops
from views import dataopsview
from globalvars import globalvars
import json

class MainController:
    def __init__(self):
        self.view = dataopsview.MainView()
        self.view.master.title("Data Operations Console")
        self.dbcontrol = DBController(self.view)
        self.querycontrol = ShowRecController(self.view
                                              )
class DBController:
    def __init__(self,mainview):
        self.view = mainview                
        self.model = dataops.Database()
        self.initGUI()
        
    def initGUI(self):
        self.dataloadframe = dataopsview.ButtonFrame(self.view,"Data Load Operations",0,0)        
        self.dataloadframe.createButton("Create New Classes")
        self.dataloadframe.button["Create New Classes"]["command"] = self.model.createClass
        self.dataloadframe.createButton("Create New Class Properties")
        self.dataloadframe.button["Create New Class Properties"]["command"] = self.model.createClassProperties
        self.dataloadframe.createButton("Create New Records")
        self.dataloadframe.button["Create New Records"]["command"] = self.model.addRecords
        self.dataloadframe.createButton("Update ServiceIds")
        self.dataloadframe.button["Update ServiceIds"]["command"] = self.model.updateServices
        
        self.viewrecsframe = dataopsview.ViewRecordFrame(self.view,"View Records",0,1)
        self.viewrecsframe.createLblMenu(["Select Class"],[sorted(list(globalvars.CLASS_DEPENDENCIES.keys())+ ["TestCase"])])
        self.viewrecsframe.createButton("Show All Records")
        self.viewrecsframe.button["Show All Records"]["command"] = self.showData
        self.viewrecsframe.createCanvas("recordview")
        
    def showData(self):
        classname = self.viewrecsframe.menuvars["Select Class"].get()
        if classname == "":
            print("No Class Selected.")
            return
        data = dataops.getCluster(classname)
        self.viewrecsframe.updateCanvas("recordview",json.dumps(data,sort_keys=True, indent=2, separators =(',',':')))

class ShowRecController:
    def __init__(self,mainview):
        self.view = mainview
        self.initGUI()
        
    def initGUI(self):
        self.queryframe = dataopsview.QueryFrame(self.view,"Query Records",0,2)
        self.queryframe.createLblText("Enter Record Id","13:1")
        self.queryframe.textbox["Enter Record Id"].config(height=1,width=5)
        self.queryframe.createButton("Get Record")
        self.queryframe.button["Get Record"]["command"] = self.showRecordFields
        
    def showRecordFields(self):
        if len(self.queryframe.textbox.keys()) > 1:
            for i in range(4,self.queryframe.query_frame.grid_size()[1]):
                for widget in self.queryframe.query_frame.grid_slaves(row=i):
                    widget.destroy()             
        rid = self.queryframe.textbox["Enter Record Id"].get("1.0","1.4")
        if rid == "":
            "No Record Id Entered"
            return
        record = dataops.getRecord(rid)
        for key, val in record.items():
            if key.find("@") == -1:
                self.queryframe.createLblText(key,val)
                self.queryframe.textbox[key].config(height=5,width=45)
                self.queryframe.textbox[key].edit_modified(False)
        self.queryframe.createButton("Update Record")
        self.queryframe.button["Update Record"]["command"] = lambda : self.updateRecord(record)
        
    def updateRecord(self,record):
        fields = {name:text.get("1.0","end").rstrip() for name, text in self.queryframe.textbox.items() if name != "Enter Record Id" and text.edit_modified()}
        if fields != {}:
            print(fields)
        else:
            print("Nothing")
                
        
db = MainController()
db.view.mainloop()