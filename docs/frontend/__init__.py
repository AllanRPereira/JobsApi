from docs.backend.database.database import DatabaseConnection
from docs.backend.jobs.jobs import Jobs

"This is the secret key for all values encoding in aplication, change this value only here"
secret_key = "7a537406a8200f8e3f457cca721b04bc0a7197b3bb8447a80fb9bb3e8ae64356"

"Connection to database for all aplication"
databaseConn = DatabaseConnection()

"Alias to use backend Jobs class"
createJob = Jobs

"User of the system"
roles = {
    "ADMIN" : [{
            "adm" : "adm"
    }, {
        "privilege" : ("insert", "delete", "consult", "edit")        
    }]
    ,
    "PUBLIC" : [{
            "teste" : "teste"
    },{
        "privilege" : ("consult",)        
    }]
    
}