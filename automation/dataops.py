import json
import requests
from requests.auth import HTTPBasicAuth
import os
from globalvars import globalvars


class Database:    
    def __init__(self):
        #Gets list of classes already created in DB, minus the OrientDB default classes
        self.DBname = globalvars.DBNAME
        self.ClassNames = []
        excludedclasses = ["OFunction","OGraphEdge","OIdentity","OGraphVertex","ORIDs","ORestricted","ORole","OUser","_version"]        
        dbURL = "http://localhost:2480/database/" + self.DBname
        r = requests.get(dbURL, auth=HTTPBasicAuth('admin','admin'))
        db_resp = json.loads(r.text)
        for record in db_resp["classes"]:
            if record["name"] not in excludedclasses:
                self.ClassNames.append(record["name"])
            else:
                continue
        print(self.ClassNames)        
        
        data_files = os.path.join(os.path.dirname( __file__ ), '..', 'files')
        self.RecordFile = os.path.abspath(os.path.join(data_files,"DataPop.txt"))
        self.PropertyFile = os.path.abspath(os.path.join(data_files,"class_Properties.txt"))
        self.NewRecordFile = os.path.abspath(os.path.join(data_files,"NewRecords.txt")) 
        
    def createClass(self):
        propertyfile = open(self.PropertyFile, 'r')
        for line in propertyfile:
            linegroup = line.split('|')
            if linegroup[0] not in self.ClassNames:
                URL = "http://localhost:2480/class/" + self.DBname + "/" + linegroup[0]
                requests.post(URL, auth=HTTPBasicAuth('admin','admin'))
                print("Created class " + linegroup[0])
                self.ClassNames.append(linegroup[0])            
        propertyfile.close()
    
    def createClassProperties(self):        
        propertyfile = open(self.PropertyFile, 'r')
        for line in propertyfile:            
            linegroup = line.split('|')
            propsexist = False
            classURL = "http://localhost:2480/class/" + self.DBname + "/" + linegroup[0]
            r1 = requests.get(classURL, auth=HTTPBasicAuth('admin','admin'))
            class_resp = json.loads(r1.text)
            if "properties" in class_resp.keys():
                propsexist = True
            if linegroup[0] in self.ClassNames and not propsexist:
                propURL = "http://localhost:2480/property/" + self.DBname + "/" + linegroup[0]
                payload = linegroup[1]
                headers = {"content-type":"application/json"}
                r2 = requests.post(propURL, data=payload, headers=headers, auth=HTTPBasicAuth('admin','admin'))
                print("Created " + r2.text + " new properties for class " + linegroup[0])            
        propertyfile.close()
        
    def addRecords(self):
        file = self.RecordFile
        access = "r"
        for name in self.ClassNames:
            url = "http://localhost:2480/class/" + self.DBname + "/" + name
            r = requests.get(url, auth=HTTPBasicAuth('admin','admin'))
            if json.loads(r.text)["records"] > 0:
                file = self.NewRecordFile                
                access = "r+"
                break
        datasource = open(file,access)
        docURL = "http://localhost:2480/document/" + self.DBname
        header = {"content-type":"application/json"}
        for line in datasource:
            if line != "\n":
                linegroup = line.split("|")
                requests.post(docURL, data=linegroup[1], headers=header, auth=HTTPBasicAuth('admin','admin'))
                print("Record of class " + linegroup[0] + " added to database")                
        if access == "r+":
            masterfile = open(self.RecordFile,"a")
            masterfile.write(datasource.read())
            masterfile.close()
            datasource.seek(0,0)
            datasource.truncate()
        datasource.close()
    
    def updateServices(self):
        clusturl = "http://localhost:2480/query/" + self.DBname + "/sql/select from Service"
        docurl = "http://localhost:2480/document/" + self.DBname + "/"
        headers = {"content-type":"application/json"}
        param = {"updateMode":"partial"}
        r = requests.get(clusturl, auth=HTTPBasicAuth('admin','admin'))
        for record in json.loads(r.text)["result"]:
            if "ServiceKeys" in record.keys():
                if set(globalvars.SERVICE_CRED_RELATIONS[record["ServiceId"]]) & set(record["ServiceKeys"]) != set(record["ServiceKeys"]) or set(globalvars.SERVICE_CRED_RELATIONS[record["ServiceId"]]) & set(record["ServiceKeys"]) != set(globalvars.SERVICE_CRED_RELATIONS[record["ServiceId"]]):
                    record["ServiceKeys"] = globalvars.SERVICE_CRED_RELATIONS[record["ServiceId"]]
                    r2 = requests.put(docurl + record["@rid"][1:], params=param, headers=headers, data=json.dumps(record), auth=HTTPBasicAuth('admin','admin'))
                    print(r2.text)
            else:
                record["ServiceKeys"] = globalvars.SERVICE_CRED_RELATIONS[record["ServiceId"]]
                r2 = requests.put(docurl + record["@rid"][1:], params=param, headers=headers, data=json.dumps(record), auth=HTTPBasicAuth('admin','admin'))
                print(r2.text)
                
def getCluster(classname):
    clusturl = "http://localhost:2480/cluster/" + globalvars.DBNAME + "/" + classname + "/100"
    r = requests.get(clusturl,auth=HTTPBasicAuth('admin','admin'))
    return json.loads(r.text)

def getRecord(rid):
    docurl = "http://localhost:2480/document/" + globalvars.DBNAME + "/" + rid
    r = requests.get(docurl,auth=HTTPBasicAuth('admin','admin'))
    return json.loads(r.text)
        
        