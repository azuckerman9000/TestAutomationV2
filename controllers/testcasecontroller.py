from views import testcaseview
from automation import testcasebuilder
from globalvars import globalvars
import os
import csv

class TCController:
    def __init__(self):
        self.view = testcaseview.MainView()
        self.view.master.title("TestCase Builder")
        self.getTestCases()        
        self.initGUI()
        
    def getTestCases(self):
        self.TestCaseObjs = {}
        Idlist = testcasebuilder.getClassRecordIds("TestCase")
        if Idlist == []:
            return
        for Id in Idlist:
            self.TestCaseObjs[Id] = testcasebuilder.TestCase()
            
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
        self.optmenuframe.createLblCheckbox(optcheckinputs)
        
        self.buildframe = testcaseview.InputFrame(self.view,None,2,0)
        self.buildframe.createButton("Create Test Case")
        self.buildframe.button["Create Test Case"]["command"] = self.createTestCase
        self.buildframe.createButton("Reset Inputs")
        self.buildframe.createButton("Build Authorize")
        self.buildframe.button["Build Authorize"]["command"] = self.populateDataSource 
        
        self.testviewframe = testcaseview.InputFrame(self.view,None,0,1)        
        self.testviewframe.createListbox("soap")
        self.testviewframe.updateListbox("soap",self.TestCaseString.keys())        
        
    def createTestCase(self):
        for value in self.reqmenuframe.menuvars.values():
            if value.get() == "":
                print("Must Enter All Required Fields")
                return
        
        EcommSecInd = self.optmenuframe.checkvars["3DSecure"].get()
        if EcommSecInd == "":
            EcommSecInd = None
        Level2Ind = self.optmenuframe.menuvars["Level2Data"].get()
        if Level2Ind == "":
            Level2Ind = None
        BillPayInd = self.optmenuframe.menuvars["BillPayment"].get()
        if BillPayInd == "":
            BillPayInd = None
        args = []
        if self.optmenuframe.checkvars["CVData"].get() != "":
            args.append(self.optmenuframe.checkvars["CVData"].get())        
        if self.optmenuframe.menuvars["AVSData"].get() != "":
            args.append(self.optmenuframe.checkvars["AVSData"].get())
        
        newtc = testcasebuilder.TestCase()
        newtc.createRecord(self.reqmenuframe.menuvars[self.reqmenuinputs[0]].get(),
                                              self.reqmenuframe.menuvars[self.reqmenuinputs[1]].get(),
                                              self.reqmenuframe.menuvars[self.reqmenuinputs[2]].get(),
                                              self.reqmenuframe.menuvars[self.reqmenuinputs[3]].get(),
                                              self.reqmenuframe.menuvars[self.reqmenuinputs[4]].get(),
                                              self.reqmenuframe.menuvars[self.reqmenuinputs[5]].get(),
                                              self.reqmenuframe.menuvars[self.reqmenuinputs[6]].get(),
                                              EcommSecInd,
                                              Level2Ind,
                                              BillPayInd,
                                              *args)        
        
        if newtc.recordid in self.TestCaseObjs.keys():
            print("Test Case Already Exists")
            return
        self.TestCaseObjs[newtc.recordid] = newtc
        self.TestCaseString[newtc.dispStr] = newtc.recordid
        self.testviewframe.updateListbox("soap",self.TestCaseString.keys())
    
    def populateDataSource(self):
        if self.testviewframe.listbox["soap"].curselection() == ():
            return
        dispstr = self.testviewframe.listbox["soap"].get(self.testviewframe.listbox["soap"].curselection()[0])
        selectedobj = self.TestCaseObjs[self.TestCaseString[dispstr]]
        if "TestData" not in selectedobj.__dict__.keys():
            selectedobj.getRecord(selectedobj.recordid)
        
        columns = []
        values = []
        for classnode,classdata in selectedobj.TestData.items():
            if classnode.find("@") == -1:                
                for fieldname, value in classdata.items():
                    if fieldname.find("@") == -1:                        
                        columns.append(classnode + ":" + fieldname)
                        values.append(value)
                        
        data_files = os.path.join(os.path.dirname( __file__ ), '..', 'files')
        path = os.path.abspath(os.path.join(data_files,"AuthData.csv"))
        authdatafile = open(path, 'w')
        rowwriter = csv.writer(authdatafile,delimiter=",",lineterminator='\n')
        rowwriter.writerow(columns)
        rowwriter.writerow(values)
        authdatafile.close()
                
tc = TCController()
tc.view.mainloop()