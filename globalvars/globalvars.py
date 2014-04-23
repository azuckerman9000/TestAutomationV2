################Global Variables###################
global DBNAME
DBNAME = "CWSData2"

global PROPERTYTYPES
PROPERTYTYPES = ["STRING","INTEGER","LINK","LINKLIST","EMBEDDEDLIST","EMBEDDEDMAP"]

global TENDERTYPES
TENDERTYPES = ["Credit","PINDebit"]

global MESSAGETYPES
MESSAGETYPES = ["SOAP","REST"]

global HOSTNAMES
HOSTNAMES = ["EVO HostCap TestHost","EVO TermCap TestHost","EVO HostCap Sandbox","EVO TermCap Sandbox","EVO TermCap AutoResponder","EVO TermCap TPS","EVO HostCap TPS","EVOIntl HostCap Sandbox"]

global INDUSTRYTYPES
INDUSTRYTYPES = ["Retail","Restaurant","MOTO","Ecommerce"]

global WORKFLOWS
WORKFLOWS = ["None","Magensa","ReD"]

global ENVIRONMENTS
ENVIRONMENTS = ["TEST","CERT","PROD"]

global CARDTYPES
CARDTYPES = ["Visa","MasterCard","Discover","AmericanExpress"]

global AVSARGS
AVSARGS = ["AVSData","IntlAVSData"]

global LEVEL2ARGS
LEVEL2ARGS = ["Exempt","NotExempt"]

global BILLPAYARGS
BILLPAYARGS = ["Recurring","Installment"]

global CARDSECARGS
CARDSECARGS = ["CVData","AVSData","IntlAVSData"]

global TENDERCLASSES
TENDERCLASSES = ["CardData","CardSecurityData","EcommerceSecurityData"]

global SERVICE_CRED_RELATIONS
SERVICE_CRED_RELATIONS = {"911C800001":["6B2866C8FD500001","23CE26C8FD500001"],
                          "39C6700001":["6B2866C8FD500001","23CE26C8FD500001","83D9854308400001","BD92E5C0AEF00001"],
                          "A77A300001":["6B2866C8FD500001","23CE26C8FD500001"],
                          "4C85600001":["6B2866C8FD500001","23CE26C8FD500001","83D9854308400001","BD92E5C0AEF00001"],
                          "A021700011":["6B2866C8FD500001","23CE26C8FD500001","83D9854308400001","BD92E5C0AEF00001"],
                          "A121700011":["6B2866C8FD500001","23CE26C8FD500001","83D9854308400001","BD92E5C0AEF00001"],
                          "1257A00001":["6B2866C8FD500001","23CE26C8FD500001"],
                          "39C671300C":["764B09E37A61300C","C10CF9E37A61300C"],
                          "4C8561300C":["764B09E37A61300C","C10CF9E37A61300C"],
                          "A01391300C":["764B09E37A61300C"],
                          "A02391300C":["764B09E37A61300C"],
                          "5717F1300C":["764B09E37A61300C","C10CF9E37A61300C"],
                          "372EC00001":["6B2866C8FD500001", "23CE26C8FD500001"]}

global CLASS_DEPENDENCIES
CLASS_DEPENDENCIES = {"Credentials":None,
                      "Service":"Credentials",
                      "Merchant":"Service",
                      "Application":"Credentials",
                      "Level2Data":"CardData",
                      "TransactionData":None,
                      "CardData":None,
                      "CardSecurityData":"CardData",
                      "EcommerceSecurityData":"CardData",
                      "InterchangeData":None}

global EMBEDDEDMAPFIELDS
EMBEDDEDMAPFIELDS = ["AVSData:PostalCode","AVSData:Street","TaxExempt:Amount","TaxExempt:IsTaxExempt","TaxExempt:TaxExemptNumber",
                     "IntlAVSData:HouseNumber","IntlAVSData:Street","IntlAVSData:PostalCode","IntlAVSData:City","IntlAVSData:Country"]