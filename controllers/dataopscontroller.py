from automation import dataops
from views import dataopsview

class DBController:
    def __init__(self):        
        self.view = dataopsview.MainView()
        self.view.master.title("Data Operations Console")
        self.view.createWidgets()
        self.model = dataops.Database()
        self.setCallbacks()
        
    def setCallbacks(self):
        self.view.createclasses_button["command"] = self.model.createClass
        self.view.createprops_button["command"] = self.model.createClassProperties
        self.view.addrecords_button["command"] = self.model.addRecords
        self.view.updatesvc_button["command"] = self.model.updateServices
        
        
db = DBController()
db.view.mainloop()