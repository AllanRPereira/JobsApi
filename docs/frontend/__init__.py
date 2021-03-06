from docs.backend.database.database import DatabaseConnection
from docs.backend.jobs.jobs import Jobs

"This is the secret key for all values encoding in aplication, change this value only here"
secret_key = "7a537406a8200f8e3f457cca721b04bc0a7197b3bb8447a80fb9bb3e8ae64356"

"Connection to database for all aplication"
databaseConn = DatabaseConnection()

"Alias to use backend Jobs class"
def createJob(jobInformationDictionary):
    try:
        jobInstance = Jobs(**jobInformationDictionary)
    except Exception as error:
        logs = {
            "status" : "unsuccess",
            "log" : error.args[0]
        }
        if error.args[0] == "ParentJob can't have same name of the principal job":
            return (False, logs, 417)
        else:
            return (False, logs, 500)
    return (True, jobInstance)

"User of the system"
roles = {
    "ADMIN" : [{
            "adm" : "adm"
    }, {
        "privilege" : ["consult", "insert", "edit", "delete"]        
    }]
    ,
    "PUBLIC" : [{
            "teste" : "teste"
    },{
        "privilege" : ["consult",] 
    }]
    
}