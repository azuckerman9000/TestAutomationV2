import abc
import requests
import json
from globalvars import globalvars
from requests.auth import HTTPBasicAuth
import sys

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
        if tc_resp["TestCaseInfo"]["IndustryType"] in ["Retail","Resturant"]:
            del tc_resp["CardData"]["PAN"]
        else:
            del tc_resp["CardData"]["Track2Data"]
        del tc_resp["TestCaseInfo"]        
        self.TestData = tc_resp
    
    def createRecord(self,**kwargs):
        self.checkExists(**kwargs)
        if self._exists:
            return
        
        self.RecordObjects = {"Credentials":Credentials(kwargs["Environment"],kwargs["MessageType"]),"Service":Service(kwargs["Host"],kwargs["Workflow"]),
                              "Merchant":Merchant(kwargs["IndustryType"],kwargs["Environment"],kwargs["MessageType"]),
                              "Application":Application(),"Level2Data":Level2Data(kwargs["Level2Data"]),"TransactionData":TransactionData(kwargs["TenderType"],kwargs["IndustryType"],kwargs["BillPayment"]),
                              "CardData":CardData(kwargs["Environment"],kwargs["CardType"]),"CardSecurityData":CardSecurityData(kwargs["TenderType"],kwargs["AVSData"],kwargs["CVData"]),
                              "EcommerceSecurityData":EcommerceSecurityData(kwargs["3DSecure"]),"InterchangeData":InterchangeData(kwargs["BillPayment"])}
        
        for classname, classobj in self.RecordObjects.items():
            if not classobj.exists:
                try:
                    self.getDependentRecord(classname,classobj)
                except IndexError:
                    print("Exiting Create TestCase...")
                    raise
        
        TestCase = {}        
        for classname, classobj in self.RecordObjects.items():
            if classobj.exists:
                TestCase[classname] = classobj.recordid
        
        self.TestCaseInfo = kwargs
        TestCase["TestCaseInfo"] = self.TestCaseInfo
        TestCase["@class"] = "TestCase"
        header = {"content-type":"application/json"}
        r = requests.post("http://localhost:2480/document/" + globalvars.DBNAME, data=json.dumps(TestCase), headers=header, auth=HTTPBasicAuth('admin','admin'))
        self._exists = True
        self._recordid = r.text
    
    def checkExists(self,**kwargs):
        query = "select from TestCase where"        
        for key, value in kwargs.items():            
            query += " TestCaseInfo." + key + " = '" + str(value) + "' and"                      
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
        try:
            if DepClassName != None:
                DepClassObj = self.RecordObjects[globalvars.CLASS_DEPENDENCIES[classname]]
                if not DepClassObj.exists:
                    self.getDependentRecord(DepClassName,DepClassObj)            
                classobj.getRecord(DepClassObj.classkey)            
            else:
                classobj.getRecord()
        except IndexError:
            print("No record exists of type: " + classname + " for given inputs.")
            raise                      
            
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
        if self.TestCaseInfo["TenderType"] == "PINDebit":
            self._dispStr += "-PINDebit"
        if self.TestCaseInfo["Workflow"] != "None":
            self._dispStr += "-" + self.TestCaseInfo["Workflow"]
        if self.TestCaseInfo["3DSecure"] != "False":
            self._dispStr += "-" + self.TestCaseInfo["3DSecure"]
        if self.TestCaseInfo["Level2Data"] != "None":
            self._dispStr += "-Level2:" + self.TestCaseInfo["Level2Data"]
        if self.TestCaseInfo["BillPayment"] != "None":
            self._dispStr += "-BillPay:" + self.TestCaseInfo["BillPayment"]
        if self.TestCaseInfo["CVData"] != "False":
            self._dispStr += "-CVData"
        if self.TestCaseInfo["AVSData"] != "None":
            self._dispStr += "-" + self.TestCaseInfo["AVSData"]        
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
        if self.Level2Ind == "None":
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
        if self.BillPayInd != "None":
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
    def __init__(self,TenderType,AVSData,CVData):
        self.TenderType = TenderType
        self.AVSData = AVSData
        self.CVData = CVData
        self._exists = False 
                
    def getRecord(self,PAN):
        if self.TenderType == "Credit" and self.CVData == "False" and self.AVSData == "None":
            self._recordid = None
            self._exists = False
            return            
        url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select from CardSecurityData where PAN = '" + PAN + "' and "
        if self.AVSData == "AVSData":
            url += " AVSData is not null and "
        else:
            url += " AVSData is null and "
        if self.CVData == "True":
            url += " CVData is not null and "
        else:
            url += " CVData is null and "
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
        if self.EcommSecInd == "False":
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
        if self.BillPayInd == "None":
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
            
def getClassRecordIds(classname,withdata=False):
    url = "http://localhost:2480/query/" + globalvars.DBNAME + "/sql/select from " + classname + "/100"
    r1 = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
    queryresults = json.loads(r1.text)["result"]
    if withdata:
        data = {}
        try:
            for result in queryresults:
                data[result["@rid"]] = result
        except (IndexError, KeyError):
            pass
        return data
    else:
        data = []
        try:
            for result in queryresults:
                data.append(result["@rid"])
        except (IndexError, KeyError):
            pass
        return data

def getFieldNames():
        fieldnames = []
        for classname in globalvars.CLASS_DEPENDENCIES.keys():
            url = "http://localhost:2480/class/" + globalvars.DBNAME + "/" + classname
            r = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
            properties = json.loads(r.text)["properties"]
            for prop in properties:
                if prop["type"] == "STRING" or prop["type"] == "INTEGER":
                    fieldnames.append(prop["name"])
            fieldnames += globalvars.EMBEDDEDMAPFIELDS
        return list(set(fieldnames))