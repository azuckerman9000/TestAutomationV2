from views import testcaseview
from automation import testcasebuilder
from globalvars import globalvars
import os
import csv
import json

class TCController:
    def __init__(self):
        self.view = testcaseview.MainView()
        self.view.master.title("TestCase Builder")
        self.getTestCases()
        self.getTestStrings()        
        self.initGUI()
        
    def getTestCases(self):
        self.TestCaseObjs = {}
        Idlist = testcasebuilder.getClassRecordIds("TestCase")
        if Idlist == []:
            return
        for Id in Idlist:
            self.TestCaseObjs[Id] = testcasebuilder.TestCase()
    
    def getTestStrings(self):         
        self.TestCaseString = {}
        for Id, obj in self.TestCaseObjs.items():
            obj.getRecord(Id)
            self.TestCaseString[obj.dispStr] = Id
        
    def initGUI(self):
        self.reqmenuinputs = ["TenderType","MessageType","Host","IndustryType","Workflow","Environment","CardType"]
        reqmenuvalues = [globalvars.TENDERTYPES,globalvars.MESSAGETYPES,globalvars.HOSTNAMES,globalvars.INDUSTRYTYPES,globalvars.WORKFLOWS,globalvars.ENVIRONMENTS,globalvars.CARDTYPES]
        self.reqmenuframe = testcaseview.InputFrame(self.view,"Required Inputs",0,0)
        self.reqmenuframe.title["fg"] ="red"
        self.reqmenuframe.createLblMenu(self.reqmenuinputs,reqmenuvalues)
        
        optmenuinputs = ["Level2Data","BillPayment","AVSData"]
        optmenuvalues = [globalvars.LEVEL2ARGS,globalvars.BILLPAYARGS,globalvars.AVSARGS]        
        optcheckinputs = ["3DSecure","CVData"]
        self.optmenuframe = testcaseview.InputFrame(self.view,"Optional Inputs",1,0)
        self.optmenuframe.title["fg"] ="blue"
        self.optmenuframe.createLblMenu(optmenuinputs,optmenuvalues)
        for menuvar in self.optmenuframe.menuvars.values():
            menuvar.set("None")        
        self.optmenuframe.createLblCheckbox(optcheckinputs)
        
        self.buildframe = testcaseview.InputFrame(self.view,None,2,0)
        self.buildframe.createButton("Create Test Case")
        self.buildframe.button["Create Test Case"]["command"] = self.createTestCase
        self.buildframe.createButton("Reset Inputs")
        self.buildframe.button["Reset Inputs"]["command"] = self.resetInputs
        self.buildframe.createButton("Build Authorize")
        self.buildframe.button["Build Authorize"]["command"] = self.populateDataSource 
        
        self.SOAPviewframe = testcaseview.InputFrame(self.view,None,0,1)        
        self.SOAPviewframe.createListbox("soap")
        self.SOAPviewframe.updateListbox("soap",[dispstr for dispstr in self.TestCaseString.keys() if dispstr[:4] == "SOAP"])
        self.RESTviewframe = testcaseview.InputFrame(self.view,None,0,2)        
        self.RESTviewframe.createListbox("rest")
        self.RESTviewframe.updateListbox("rest",[dispstr for dispstr in self.TestCaseString.keys() if dispstr[:4] == "REST"])
        
        self.SOAPviewframe.listbox["soap"].bind("<ButtonRelease>",self.showTestCase)
        self.RESTviewframe.listbox["rest"].bind("<ButtonRelease>",self.showTestCase)
        
        self.displayframe = testcaseview.InputFrame(self.view,None,1,1)
        self.displayframe.createCanvas("tcdisplay")
        self.displayframe.input_frame.grid(columnspan=2)
        
    def showTestCase(self,event):
        dispstr = event.widget.get(event.widget.curselection()[0])
        tcobj = self.TestCaseObjs[self.TestCaseString[dispstr]]
        self.displayframe.updateCanvas("tcdisplay",json.dumps(tcobj.TestData,sort_keys=True, indent=2, separators =(',',':')))
        
    def createTestCase(self):
        for value in self.reqmenuframe.menuvars.values():
            if value.get() == "":
                print("Must Enter All Required Fields")
                return
        kwparams = dict([(key,val.get())for key, val in self.reqmenuframe.menuvars.items()] +
                        [(key,val.get())for key, val in self.optmenuframe.menuvars.items()] +
                        [(key,val.get())for key, val in self.optmenuframe.checkvars.items()])
        
        newtc = testcasebuilder.TestCase()
        newtc.createRecord(**kwparams)        
        
        if newtc.recordid in self.TestCaseObjs.keys():
            print("Test Case Already Exists")
            return
        self.TestCaseObjs[newtc.recordid] = newtc
        self.TestCaseString[newtc.dispStr] = newtc.recordid        
        self.SOAPviewframe.updateListbox("soap", [dispstr for dispstr in self.TestCaseString.keys() if dispstr[:4] == "SOAP"])
        self.RESTviewframe.updateListbox("rest", [dispstr for dispstr in self.TestCaseString.keys() if dispstr[:4] == "REST"])
    
    def populateDataSource(self):        
        if self.view.focus_get().curselection() == ():
            return
        dispstr = self.view.focus_get().get(self.view.focus_get().curselection()[0])
        selectedobj = self.TestCaseObjs[self.TestCaseString[dispstr]]
        if "TestData" not in selectedobj.__dict__.keys():
            selectedobj.getRecord(selectedobj.recordid)
        
        data = dict.fromkeys(testcasebuilder.getFieldNames(),"")
        for classnode,classdata in selectedobj.TestData.items():
            if classnode.find("@") == -1:
                for fieldname, value in classdata.items():
                    if fieldname.find("@") == -1 and not isinstance(value,dict):
                        data[fieldname] = value
                    elif isinstance(value,dict):
                        for dictfieldname, dictvalue in value.items():
                            data[fieldname + ":" + dictfieldname] = dictvalue
                        
        data_files = os.path.join(os.path.dirname( __file__ ), '..', 'files')
        path = os.path.abspath(os.path.join(data_files,"AuthData.csv"))
        authdatafile = open(path, 'w')
        rowwriter = csv.writer(authdatafile,delimiter=",",lineterminator='\n')
        rowwriter.writerow(list(data.keys()))
        rowwriter.writerow(list(data.values()))
        authdatafile.close()
        
    def resetInputs(self):
        for var in self.reqmenuframe.menuvars.values():
            var.set("")
        for var in self.optmenuframe.menuvars.values():
            var.set("None")
        for var in self.optmenuframe.checkvars.values():
            var.set("False")
        
                
tc = TCController()
tc.view.mainloop()