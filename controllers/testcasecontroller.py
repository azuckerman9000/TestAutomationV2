from views import testcaseview
from automation import testcasebuilder
from globalvars import globalvars

class TCController:
    def __init__(self):
        self.view = testcaseview.MainView()
        self.view.master.title("TestCase Builder")
        self.buildGUI()
        
    def buildGUI(self):
        self.reqmenuinputs = ["TenderType","MessageType","Host","IndustryType","Workflow","Environment","CardType"]
        reqmenuvalues = [globalvars.TENDERTYPES,globalvars.MESSAGETYPES,globalvars.HOSTNAMES,globalvars.INDUSTRYTYPES,globalvars.WORKFLOWS,globalvars.ENVIRONMENTS,globalvars.CARDTYPES]
        self.reqmenuframe = testcaseview.InputFrame(self.view.main_frame,"Required Inputs",0,0)
        self.reqmenuframe.title["fg"] ="red"
        self.reqmenuframe.createLblMenu(self.reqmenuinputs,reqmenuvalues)
        
        optmenuinputs = ["Level2Data","BillPayment","AVSData"]
        optmenuvalues = [globalvars.LEVEL2ARGS,globalvars.BILLPAYARGS,globalvars.AVSARGS]
        optcheckinputs = ["3DSecure","CVData"]
        self.optmenuframe = testcaseview.InputFrame(self.view.main_frame,"Optional Inputs",1,0)
        self.optmenuframe.title["fg"] ="blue"
        self.optmenuframe.createLblMenu(optmenuinputs,optmenuvalues)        
        self.optmenuframe.createLblCheckbox(optcheckinputs)
        
        self.buildframe = testcaseview.InputFrame(self.view.main_frame,None,2,0)
        self.buildframe.createButton("Create Test Case")
        self.buildframe.button["Create Test Case"]["command"] = self.createTestCase
        self.buildframe.createButton("Reset Inputs")
        self.buildframe.createButton("Build Authorize")
        self.buildframe.button["Build Authorize"]["command"] = self.populateDataSource        
        
        self.testviewframe = testcaseview.InputFrame(self.view.main_frame,None,0,1)
        self.testviewframe.createListbox("soap")
        self.testviewframe.updateListbox("soap",self.showExistingTests())
        
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
                
        self.model = testcasebuilder.TestCase(self.reqmenuframe.menuvars[self.reqmenuinputs[0]].get(),
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
        self.model.getRecord()
        if self.model.exists == False:
            self.model.createRecord()
            self.testviewframe.updateListbox("soap",self.showExistingTests())          
            
    def showExistingTests(self):
        testcases = testcasebuilder.getClassRecords("TestCase")
        if testcases["result"] == []:
            return []
        selections = []
        for record in testcases["result"]:
            temp = record["TestCaseInfo"]["MessageType"]
            temp += "-" + record["TestCaseInfo"]["Host"].replace(" ","-")
            temp += "-" + record["TestCaseInfo"]["IndustryType"]
            temp += "-" + record["TestCaseInfo"]["CardType"]
            if record["TestCaseInfo"]["Workflow"] != "None":
                temp += "-" + record["TestCaseInfo"]["Workflow"]
            if record["TestCaseInfo"]["EcommSecInd"] != "None":
                temp += "-" + record["TestCaseInfo"]["EcommSecInd"]
            if record["TestCaseInfo"]["Level2Ind"] != "None":
                temp += "-" + "Level2:" + record["TestCaseInfo"]["Level2Ind"]
            if record["TestCaseInfo"]["BillPayInd"] != "None":
                temp += "-" + "BillPay:" + record["TestCaseInfo"]["BillPayInd"]
            if record["TestCaseInfo"]["CVData"] != "False":
                temp += "-" + "CVData"
            if record["TestCaseInfo"]["AVSData"] != "False":
                temp += "-" + "AVSData"
            if record["TestCaseInfo"]["IntlAVSData"] != "False":
                temp += "-" + "IntlAVSData"
            selections.append(temp)
        return selections
    
    def populateDataSource(self):
        if self.model.exists == False:
            return
        data = testcasebuilder.getRecordById(self.model.recordid)
        print(data)
                
tc = TCController()
tc.view.mainloop()