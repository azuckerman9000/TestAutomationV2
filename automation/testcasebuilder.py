import abc
import requests
import json
from globalvars import globalvars
from requests.auth import HTTPBasicAuth

class CWSDataQuery(object):
    __metaclass__ = abc.ABCMeta    
        
    @abc.abstractmethod
    def getRecord(self):
        pass
        #Abstract Method for querying OrientDB for data
        
    @property
    @abc.abstractmethod       
    def recordid(self):
        pass
        #Abstract property for recordid
        
    @property
    @abc.abstractmethod       
    def classkey(self):
        pass
        #Abstract property for class specific keys - eg. ServiceId, ServiceKey   
    
    @property
    @abc.abstractmethod       
    def exists(self):
        pass
    
    @classmethod
    def __subclasshook__(cls,C):
        if cls is CWSDataQuery:
            if hasattr(C,"getRecord"):
                return True
        return NotImplemented
    
class TestCase(CWSDataQuery):
    def __init__(self):
        self._exists = False
        
    def getRecord(self,recordid):
        url = "http://localhost:2480/document/" + globalvars.DBNAME + "/" + recordid[1:] +"/*:1"
        r = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
        tc_resp = json.loads(r.text)
        self._recordid = tc_resp["@rid"]
        self._exists = True
        self.TestCaseInfo = tc_resp["TestCaseInfo"]
        del tc_resp["TestCaseInfo"]
        self.TestData = tc_resp
    
    def createRecord(self,TenderType,MessageType,Host,IndustryType,Workflow,Environment,CardType,EcommSecInd,Level2Ind,BillPayInd,*cardsecargs):
        self.Environment = Environment
        self.MessageType = MessageType
        self.Host = Host
        self.Workflow = Workflow
        self.IndustryType = IndustryType
        self.TenderType = TenderType
        self.CardType = CardType
        self.EcommSecInd = EcommSecInd
        self.Level2Ind = Level2Ind
        self.BillPayInd = BillPayInd
        self.cardsecargs = cardsecargs
        self.checkExists()
        if self._exists:
            return
        
        self.RecordObjects = {"Credentials":Credentials(self.Environment,self.MessageType),"Service":Service(self.Host,self.Workflow),"Merchant":Merchant(self.IndustryType,self.Environment,self.MessageType),
                              "Application":Application(),"Level2Data":Level2Data(self.Level2Ind),"TransactionData":TransactionData(self.TenderType,self.IndustryType,self.BillPayInd),
                              "CardData":CardData(self.Environment,self.CardType),"CardSecurityData":CardSecurityData(self.TenderType,*self.cardsecargs),
                              "EcommerceSecurityData":EcommerceSecurityData(self.EcommSecInd),"InterchangeData":InterchangeData(self.BillPayInd)}
        
        for classname, classobj in self.RecordObjects.items():
            if not classobj.exists:
                self.getDependentRecord(classname,classobj)
        
        TestCase = {}        
        for classname, classobj in self.RecordObjects.items():
            if classobj.exists:
                TestCase[classname] = classobj.recordid
        
        TestCase["TestCaseInfo"] = self.TestCaseInfo
        TestCase["@class"] = "TestCase"
        header = {"content-type":"application/json"}
        r = requests.post("http://localhost:2480/document/" + globalvars.DBNAME, data=json.dumps(TestCase), headers=header, auth=HTTPBasicAuth('admin','admin'))
        self._exists = True
        self._recordid = r.text
    
    def checkExists(self):
        query = "select from TestCase where"
        self.TestCaseInfo = {}
        for key, value in self.__dict__.items():
            if key not in ["_exists","cardsecargs","TestCaseInfo"]:
                query += " TestCaseInfo." + key + " = '" + str(value) + "' and"
                self.TestCaseInfo[key] = str(value)
        for arg in globalvars.CARDSECARGS:
            if arg in self.cardsecargs:
                query += " TestCaseInfo." + arg + " = 'True' and"
                self.TestCaseInfo[arg] = "True"
            else:
                query += " TestCaseInfo." + arg + " = 'False' and"
                self.TestCaseInfo[arg] = "False"
        query = query[:-4]
        r1 = requests.get("http://localhost:2480/query/" + globalvars.DBNAME + "/sql/" + query,auth=HTTPBasicAuth('admin','admin'))
        if json.loads(r1.text)["result"] == []:
            print("Creating New TestCase...")
            self._exists = False            
        else:
            self._exists = True
            self._recordid = json.loads(r1.text)["result"][0]["@rid"]
    
    def getDependentRecord(self,classname,classobj):
        DepClassName = globalvars.CLASS_DEPENDENCIES[classname]        
        if DepClassName != None:
            DepClassObj = self.RecordObjects[globalvars.CLASS_DEPENDENCIES[classname]]
            if not DepClassObj.exists:
                self.getDependentRecord(DepClassName,DepClassObj)
            else:
                classobj.getRecord(DepClassObj.classkey)
        else:
            classobj.getRecord()           
            
    @property    
    def recordid(self):
        return self._recordid
    
    @property  
    def classkey(self):
        return None
    
    @property    
    def exists(self):
        return self._exists
    
    @property
    def dispStr(self):
        if not self._exists:
            return None
        self._dispStr = self.TestCaseInfo["MessageType"]
        self._dispStr += "-" + self.TestCaseInfo["Host"].replace(" ","-")
        self._dispStr += "-" + self.TestCaseInfo["IndustryType"]
        self._dispStr += "-" + self.TestCaseInfo["CardType"]
        if self.TestCaseInfo["Workflow"] != "None":
            self._dispStr += "-" + self.TestCaseInfo["Workflow"]
        if self.TestCaseInfo["EcommSecInd"] != "None":
            self._dispStr += "-" + self.TestCaseInfo["EcommSecInd"]
        if self.TestCaseInfo["Level2Ind"] != "None":
            self._dispStr += "-" + "Level2:" + self.TestCaseInfo["Level2Ind"]
        if self.TestCaseInfo["BillPayInd"] != "None":
            self._dispStr += "-" + "BillPay:" + self.TestCaseInfo["BillPayInd"]
        if self.TestCaseInfo["CVData"] != "False":
            self._dispStr += "-" + "CVData"
        if self.TestCaseInfo["AVSData"] != "False":
            self._dispStr += "-" + "AVSData"
        if self.TestCaseInfo["IntlAVSData"] != "False":
            self._dispStr += "-" + "IntlAVSData"
        return self._dispStr    
   
class Credentials(CWSDataQuery):
    def __init__(self,Environment,MessageType):
        self.Environment = Environment
        self.MessageType = MessageType
        self._exists = False        
    
    def getRecord(self):
        url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select from Credentials where Environment = '" + self.Environment + "' and MessageType = '" + self.MessageType + "'"
        r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
        cred_resp = json.loads(r1.text)
        self._recordid = cred_resp["result"][0]["@rid"]
        self._ServiceKey = cred_resp["result"][0]["ServiceKey"]
        self._exists = True
        
    @property    
    def recordid(self):
        return self._recordid
    
    @property  
    def classkey(self):
        return self._ServiceKey
    
    @property    
    def exists(self):
        return self._exists
    
class Service(CWSDataQuery):
    def __init__(self,Host,Workflow):
        self.Host = Host
        self.Workflow = Workflow
        self._exists = False     
            
    def getRecord(self,ServiceKey):
        url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select from Service where Host = '" + self.Host + "' and Workflow = '" + self.Workflow + "' and '" + ServiceKey + "' in ServiceKeys"
        r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))        
        svc_resp = json.loads(r1.text)        
        self._recordid = svc_resp["result"][0]["@rid"]
        self._ServiceId = svc_resp["result"][0]["ServiceId"]
        self._exists = True
    
    @property  
    def recordid(self):
        return self._recordid
    
    @property  
    def classkey(self):
        return self._ServiceId
    
    @property    
    def exists(self):
        return self._exists
    
class Merchant(CWSDataQuery):
    def __init__(self,IndustryType,Environment,MessageType):
        self.IndustryType = IndustryType
        self.Environment = Environment
        self.MessageType = MessageType
        self._exists = False         
    
    def getRecord(self,ServiceId):
        url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select from Merchant where IndustryType = '" + self.IndustryType + "' and Environment = '" + self.Environment + "' and ServiceId = '" + ServiceId + "' and MessageType = '" + self.MessageType + "'"
        r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
        merch_resp = json.loads(r1.text)
        self._recordid = merch_resp["result"][0]["@rid"]
        self._MerchantProfileId = merch_resp["result"][0]["MerchantProfileId"]
        self.CustomerPresent = merch_resp["result"][0]["CustomerPresent"]
        self.EntryMode = merch_resp["result"][0]["EntryMode"]
        self._exists = True
    
    @property    
    def recordid(self):
        return self._recordid
    
    @property  
    def classkey(self):
        return self._MerchantProfileId
    
    @property    
    def exists(self):
        return self._exists
    
class Application(CWSDataQuery):
    def __init__(self):
        self._exists = False 
    
    def getRecord(self,ServiceKey):
        url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select from Application where ServiceKey = '" + ServiceKey + "'"
        r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
        app_resp = json.loads(r1.text)
        self._recordid = app_resp["result"][0]["@rid"]
        self._ApplicationProfileId = app_resp["result"][0]["ApplicationProfileId"]        
        self._exists = True        
    
    @property    
    def recordid(self):
        return self._recordid
    
    @property  
    def classkey(self):
        return self._ApplicationProfileId
    
    @property    
    def exists(self):
        return self._exists
    
class Level2Data(CWSDataQuery):
    def __init__(self,Level2Ind):
        self.Level2Ind = Level2Ind
        self._exists = False         
    
    def getRecord(self,PAN):
        if self.Level2Ind == None:
            self._recordid = None
            self._exists = False
            return
        url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select from Level2Data where PAN = '" + PAN + "' and TaxExempt containsvalue '" + self.Level2Ind + "'"
        r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
        lvl2_resp = json.loads(r1.text)
        self._recordid = lvl2_resp["result"][0]["@rid"]
        self._exists = True
    
    @property    
    def recordid(self):
        return self._recordid
    
    @property  
    def classkey(self):
        return None
    
    @property    
    def exists(self):
        return self._exists

class TransactionData(CWSDataQuery):
    def __init__(self,TenderType,IndustryType,BillPayInd):
        self.TenderType = TenderType
        self.IndustryType = IndustryType               
        self.BillPayInd = BillPayInd
        self._exists = False         
        
    def getRecord(self):
        query = "select from TransactionData where TenderType = '" + self.TenderType + "'"
        query += " and IndustryType = '" + self.IndustryType + "'"        
        if self.BillPayInd != None:
            query += " and CustomerPresent = 'BillPayment'"
         
        r1 = requests.get("http://localhost:2480/query/" + globalvars.DBNAME + "/sql/" + query,auth=HTTPBasicAuth('admin','admin'))
        self._recordid = json.loads(r1.text)["result"][0]["@rid"]
        self._exists = True
    
    @property    
    def recordid(self):
        return self._recordid
    
    @property  
    def classkey(self):
        return None
    
    @property    
    def exists(self):
        return self._exists        
        
class CardData(CWSDataQuery):
    def __init__(self,Environment,CardType):
        self.CardType = CardType
        self.Environment = Environment
        self._exists = False 
         
    def getRecord(self):
        url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select from CardData where Environment = '" + self.Environment + "' and CardType = '" + self.CardType + "'"
        r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
        card_resp = json.loads(r1.text)
        self._recordid = card_resp["result"][0]["@rid"]
        self._PAN = card_resp["result"][0]["PAN"]
        self._exists = True
    
    @property    
    def recordid(self):
        return self._recordid
    
    @property  
    def classkey(self):
        return self._PAN
    
    @property    
    def exists(self):
        return self._exists
        
class CardSecurityData(CWSDataQuery):
    def __init__(self,TenderType,*cardsecargs):
        self.TenderType = TenderType
        self.cardsecargs = cardsecargs
        self._exists = False 
                
    def getRecord(self,PAN):
        if len(self.cardsecargs) == 0:
            self._recordid = None
            self._exists = False
            return            
        url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select from CardSecurityData where PAN = '" + PAN + "' and "
        for arg in globalvars.CARDSECARGS:
            if arg in self.cardsecargs:
                url += arg + " is not null and "
            else:
                url += arg + " is null and "
        if self.TenderType == "PINDebit":
            url += "PIN is not null"
        else:
            url += "PIN is null"
        r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
        cardsec_resp = json.loads(r1.text)
        if cardsec_resp["result"] == []:
            self._recordid = None
            self._exists = False
            return
        self._recordid = cardsec_resp["result"][0]["@rid"]
        self._exists = True
        
    @property    
    def recordid(self):
        return self._recordid
    
    @property  
    def classkey(self):
        return None
    
    @property    
    def exists(self):
        return self._exists

class EcommerceSecurityData(CWSDataQuery):
    def __init__(self,EcommSecInd):
        self.EcommSecInd = EcommSecInd
        self._exists = False 
        
    def getRecord(self,PAN):
        if self.EcommSecInd == None:
            self._recordid = None
            self._exists = False
            return
        url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select from EcommerceSecurityData where PAN = '" + PAN + "'"
        r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
        ecommsec_resp = json.loads(r1.text)
        if ecommsec_resp["result"] == []:
            self._recordid = None
            self._exists = False
            return
        self._recordid = ecommsec_resp["result"][0]["@rid"]
        self._exists = True
        
    @property    
    def recordid(self):
        return self._recordid
    
    @property  
    def classkey(self):
        return None
    
    @property    
    def exists(self):
        return self._exists
    
class InterchangeData(CWSDataQuery):
    def __init__(self,BillPayInd):
        self.BillPayInd = BillPayInd
        self._exists = False 
        
    def getRecord(self):
        if self.BillPayInd == None:
            self._recordid = None
            self._exists = False
            return
        url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select from InterchangeData where BillPayment = '" + self.BillPayInd + "'"
        r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
        billpay_resp = json.loads(r1.text)
        if billpay_resp["result"] == []:
            self._recordid = None
            self._exists = False
            return
        self._recordid = billpay_resp["result"][0]["@rid"]
        self._exists = True
        
    @property    
    def recordid(self):
        return self._recordid
    
    @property  
    def classkey(self):
        return None
    
    @property    
    def exists(self):
        return self._exists
            
def getClassRecordIds(classname):
    url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select @rid from " + classname
    r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
    rids = []
    queryresults = json.loads(r1.text)["result"]
    if queryresults == []:
        return rids
    for result in queryresults:
        rids.append(result["rid"])
    return rids
"""
def getRecordById(rid):
    url = "http://localhost:2480/document/" + globalvars.DBNAME + "/" + rid[1:] + "/*:1"
    r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
    return json.loads(r1.text)
"""
