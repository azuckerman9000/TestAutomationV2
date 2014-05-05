import json
import os
from globalvars import globalvars

class RestJsonRequest:
    def __init__(self,data):
        
        self.data_files = os.path.join(os.path.dirname( __file__ ), '..', 'files')
        JsonTemp = os.path.abspath(os.path.join(self.data_files,"Auth_RestJson_Template.json"))
        AuthPath = os.path.abspath(os.path.join(self.data_files,"Auth_RestJson_Request.json")) 
        
        self.json_file = open(JsonTemp, "r")        
        self.json_template = json.loads(self.json_file.read())
        self.json_file.close()
        
        self.inputdata = data        
        self.includedmaps = set([mapname.split(":")[0] for mapname in globalvars.EMBEDDEDMAPFIELDS if self.inputdata[mapname] != ""])               
        
        auth_file = open(AuthPath, "w")
        auth_file.write(json.dumps(self.populateFields(self.json_template),sort_keys=True, indent=2, separators =(',',':')))
        auth_file.close()
       
    def populateFields(self,fieldmap):
        struct = {}
        for key,value in fieldmap.items():
            if isinstance(value, dict):                             
                populateddict = self.populateFields(value)
                if bool(populateddict):
                    if key in self.includedmaps:
                        populateddict = {popkey.split(":")[1]:popval for popkey,popval in populateddict.items()}                    
                    struct[key] = populateddict                
            elif value is not None:
                try:                    
                    if self.inputdata[key] != "":               
                        struct[key] = self.inputdata[key]
                    elif value != "":
                        struct[key] = value                                                                                                      
                except KeyError:
                    if value != "":
                        struct[key] = value
        return struct