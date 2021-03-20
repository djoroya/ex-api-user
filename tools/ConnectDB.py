import pgeocode
import pandas as pd
import json
nomi = pgeocode.Nominatim('es')

############################################################


path_details_DB = 'datasets/db_users_details.json'
path_user_DB    = 'datasets/db_users.json'


class user:
    # Properties
    UserName = ""
    PC = 0
    city = ""
    # Constructor
    def __init__(self,UserName,PC):
        self.PC = PC
        self.UserName = UserName
        self.set_city()
    # Methods 
    def set_city(self):
        "geonames services to obtain the city name"
        nomi = pgeocode.Nominatim('es')
        PandaDS = nomi.query_postal_code(self.PC)
        self.city = PandaDS.community_name

    def show(self):
        "show all properties and its values"
        temp = vars(self)
        for item in temp:
            print(item, ':', temp[item])

    def isinDB(self,db_users):
        return sum(db_users['UserName']==self.UserName) != 0

    def saveinUserDB(self,db_users):

        d1 = {"UserName":pd.Series([self.UserName],dtype="str")}
        new_user = pd.DataFrame(d1)
        #
        db_users = db_users.append(new_user,ignore_index=True)
        db_users.to_json(path_user_DB,orient='records')

    def saveinDetails(self):
        db_users_details = pd.read_json(path_details_DB)

        d2 = {"UserName"  :pd.Series([self.UserName],dtype="str"),
                "PC"      :pd.Series([self.PC]      ,dtype="str"),
                "City"    :pd.Series([self.city]    ,dtype="str")}

        new_user_details = pd.DataFrame(d2)
        #
        db_users_details = db_users_details.append(new_user_details,ignore_index=True)
        db_users_details.to_json(path_details_DB,orient='records')

def communications(UserName,PC):

    iuser = user(UserName,PC)
    # iuser city is a float when PC doesn't exist
    if isinstance(iuser.city,float):
        cod = 1
    else:
        # load data base
        db_users = pd.read_json(path_user_DB)

        if iuser.isinDB(db_users):
            # This username already exist!!
            cod = 2
        else:
            # Add new user 
            iuser.saveinUserDB(db_users)
            # Add details 
            iuser.saveinDetails()
            cod = 0
    return cod


def startDB():
    d1 = { "UserName" : pd.Series([""],dtype="str") }
    db_users = pd.DataFrame(d1)
    db_users.to_json('datasets/db_users.json',orient='records')

    #####

    d2={  "UserName" : pd.Series([""],dtype="str"),
        "PC"       : pd.Series([""],dtype="str"),
        "City"     : pd.Series([""],dtype="str")  }

    db_users_details = pd.DataFrame(d2)
    db_users_details.to_json('datasets/db_users_details.json',orient='records')
