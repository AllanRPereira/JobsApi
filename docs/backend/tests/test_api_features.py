from ..jobs.jobs import Jobs
import pytest
import requests
import json
import secrets


def deleteDataInserted(listOfNames, token):
    for name in listOfNames:
        requestToApi = requests.get("http://localhost:5000/api/delete", params={
            "name" : name,
            "token" : token
        }).content
        jsonLoad = json.loads(requestToApi)
        if jsonLoad["status"] == "unsuccess":
            return False
        
    return True

@pytest.fixture
def token_object():
    token_admin = requests.get("http://localhost:5000/api/getoken", params={
        "username" : "adm",
        "password" : "adm"
    }).content
    token_public = requests.get("http://localhost:5000/api/getoken", params={
        "username" : "teste",
        "password" : "teste"
    }).content
    jsonObjectTokenAdmin = json.loads(token_admin)
    jsonObjectTokenPublic = json.loads(token_public)
    assert jsonObjectTokenAdmin["status"] == "success", "Token admin is incorrect status receive"
    assert jsonObjectTokenPublic["status"] == "success", "Token public is incorrect status receive"

    tokensProperties = {
        "admin" : jsonObjectTokenAdmin["token"],
        "teste" : jsonObjectTokenPublic["token"]
    }

    return tokensProperties

@pytest.fixture
def get_jobs_data():
    tasksLists = []
    for tasks in range(4):
        tasksLists.append({
            'name' : secrets.token_urlsafe(4),
            'weight' : secrets.choice([ k for k in range(1,11)]),
            'completed' : secrets.choice([False, True]),
        })

    twoJobNamesDifferentList = []
    for k in range(2):
        twoJobNamesDifferentList.append({
            'name' : secrets.token_urlsafe(8),
            'active' : secrets.choice([False, True]),
            'parentJob' : {
                'name' : secrets.token_urlsafe(10),
                'active' : secrets.choice([False, True])},
            "tasks" : []
            })

    twoJobSameNameList = []
    nameJobEqual = secrets.token_urlsafe(8)
    for k in range(2):
        twoJobSameNameList.append({
            'name' : nameJobEqual,
            'active' : secrets.choice([False, True]),
            'parentJob' : {
                'name' : secrets.token_urlsafe(10),
                'active' : secrets.choice([False, True])},
            "tasks" : []
            })
        
    twoJobsCrossDependenceList = []
    nameJob = secrets.token_urlsafe(10)
    parentJobName = secrets.token_urlsafe(10)
    twoJobsCrossDependenceList.append({
        'name' : nameJob,
        'active' : secrets.choice([False, True]),
        'parentJob' : {
            'name' : parentJobName,
            'active' : secrets.choice([False, True])},
        "tasks" : []
        })
    twoJobsCrossDependenceList.append({
        'name' : parentJobName,
        'active' : secrets.choice([False, True]),
        'parentJob' : {
            'name' : nameJob,
            'active' : secrets.choice([False, True])},
        "tasks" : []
        })
    
    return {
        "tasksList" : tasksLists,
        "NamesDifferent" : twoJobNamesDifferentList,
        "NamesEqual" : twoJobSameNameList,
        "CrossDependenceBetween" : twoJobsCrossDependenceList
    }



def test_api_consult_without_result(token_object):

    for index in range(2):
        apiRequest = requests.get("http://localhost:5000/api/consult", params={
            "token" : token_object["teste"],
            "name" : "dont_exists"
        })
        response = json.loads(apiRequest.content)
        assert response["status"] == "unsuccess", "Status has success but this job doesn't exists"
        assert response["log"] == "This job doesn't exists", "Message incorrect to this case"

    return True

def test_api_insert_data_without_error(token_object, get_jobs_data):
    jobsToWork = get_jobs_data["NamesDifferent"]

    for index in range(2):
        jobsToWork[index].update({"token" : token_object["admin"]})
        jobCodec = json.dumps(jobsToWork[index])
        apiRequest = requests.get("http://localhost:5000/api/insert", data=jobCodec, headers={"Content-Type" : "application/json"})
        response = json.loads(apiRequest.content)
        assert response["status"] == "success", f"Normal job but the status has unsuccess: {response['log']}"

    assert deleteDataInserted([job["name"] for job in jobsToWork], token_object["admin"]) == True, "The data don't has deleted correctly"

    return True

def test_api_insert_with_cross_dependence(token_object, get_jobs_data):
    jobsToWork = get_jobs_data["CrossDependenceBetween"]

    for index in range(2):
        jobsToWork[index].update({"token" : token_object["admin"]})

        jobCodec = json.dumps(jobsToWork[index])
        apiRequest = requests.get("http://localhost:5000/api/insert", data=jobCodec, headers={"Content-Type" : "application/json"})
        response = json.loads(apiRequest.content)
        statusMessage = { 
            "success" : "The first will be work", 
            "unsuccess" : "There is cross dependence in this jobs!"
        }
        if index == 0:
            message = "success"
        else:
            message = "unsuccess"
        assert response["status"] == message, statusMessage[message]

    assert deleteDataInserted([jobsToWork[0]["name"]], token_object["admin"]) == True, "The data don't has deleted correctly"

    return True

def test_api_insert_without_name(token_object, get_jobs_data):
    jobsToWork = get_jobs_data["NamesDifferent"]
    for index in range(2):
        jobsToWork[index].update({"token" : token_object["admin"]})
        jobsToWork[index].pop("name")
        jobCodec = json.dumps(jobsToWork[index])
        apiRequest = requests.get("http://localhost:5000/api/insert", data=jobCodec, headers={"Content-Type" : "application/json"})
        response = json.loads(apiRequest.content)
        assert response["status"] == "unsuccess", "JobName is not passed"
    
    "Don't need delete because nothing was inserted"

    return True

def test_api_insert_same_name(token_object, get_jobs_data):
    jobsToWork = get_jobs_data["NamesEqual"]
    for index in range(2):
        jobsToWork[index].update({"token" : token_object["admin"]})
        jobCodec = json.dumps(jobsToWork[index])
        apiRequest = requests.get("http://localhost:5000/api/insert", data=jobCodec, headers={"Content-Type" : "application/json"})
        response = json.loads(apiRequest.content)
        statusMessage = {
            "success" : "This job will be inserted",
            "unsuccess" : "Don't has detected the same name in the bd"
        }
        if index == 0:
            message = "success"
        else:
            message = "unsuccess"
        assert response["status"] == message, statusMessage[message]
    
    assert deleteDataInserted([jobsToWork[0]["name"]], token_object["admin"]) == True, "The data don't has deleted correctly"

def test_api_consult_with_data(token_object, get_jobs_data):
    jobsToWork = get_jobs_data["NamesDifferent"]
    jobsToWork[0].update({"token" : token_object["admin"]})
    jobCodec = json.dumps(jobsToWork[0])
    apiRequest = requests.get("http://localhost:5000/api/insert", data=jobCodec, headers={"Content-Type" : "application/json"})    
    jsonRequestInsert = json.loads(apiRequest.content)
    jobsToWork[0].pop("token")
    
    toSendConsult = {
        "name" : jobsToWork[0]["name"],
        "token" : token_object["teste"]
    }
    apiRequest = requests.get("http://localhost:5000/api/consult", params=toSendConsult)
    jsonRequestConsult = json.loads(apiRequest.content)

    assert jsonRequestInsert["status"] == "success", "This job will be inserted"
    assert jsonRequestConsult["status"] == "success", "This job will be consulted"
    jsonRequestConsult.pop("status")
    assert jsonRequestConsult == jobsToWork[0], "This data don't returned correct"
    assert deleteDataInserted([jobsToWork[0]["name"]], token_object["admin"]) == True, "The data don't has deleted correctly"

def test_api_delete_without_error(token_object, get_jobs_data):
    jobsToWork = get_jobs_data["NamesDifferent"]
    jobsToWork[0].update({"token" : token_object["admin"]})
    jobCodec = json.dumps(jobsToWork[0])
    apiRequest = requests.get("http://localhost:5000/api/insert", data=jobCodec, headers={"Content-Type" : "application/json"})
    jsonRequestInsert = json.loads(apiRequest.content)

    sendToDelete = {
        "name" : jobsToWork[0]["name"],
        "token" : token_object["admin"]
    }
    apiRequest = requests.get("http://localhost:5000/api/delete", params=sendToDelete)
    jsonRequestDelete = json.loads(apiRequest.content)

    sendToConsult = {
        "name" : jobsToWork[0]["name"],
        "token" : token_object["teste"]
    }
    apiRequest = requests.get("http://localhost:5000/api/consult", params=sendToConsult)
    jsonRequestConsult = json.loads(apiRequest.content)

    assert jsonRequestInsert["status"] == "success", "This job will be insert"
    assert jsonRequestDelete["status"] == "success", "This job exists but don't was deleted"
    assert jsonRequestConsult["status"] == "unsuccess" and jsonRequestConsult["log"] == "This job doesn't exists", "This job don't will be exists"

def test_api_delete_job_not_exists(token_object, get_jobs_data):
    sendToDelete = {
        "name" : "This-jobs-dont-exists",
        "token" : token_object["admin"]
    }
    apiRequest = requests.get("http://localhost:5000/api/delete", params=sendToDelete)
    jsonRequestDelete = json.loads(apiRequest.content)

    assert jsonRequestDelete["status"] == "unsuccess" and jsonRequestDelete["log"] == "This job doesn't exists", "This jobs don't exists but has deleted ??"

def test_api_edit_without_error(token_object, get_jobs_data):
    jobsToWork = get_jobs_data["NamesDifferent"]

    jobsToWork[0].update({"token" : token_object["admin"]})
    jobCodec = json.dumps(jobsToWork[0])
    apiRequest = requests.get("http://localhost:5000/api/insert", data=jobCodec, headers={"Content-Type" : "application/json"})
    jsonRequestInsert = json.loads(apiRequest.content)

    jobsToWork[1].update({
        "token" : token_object["admin"],
        "job_name_edit" : jobsToWork[0]["name"]
    })
    jobCodec = json.dumps(jobsToWork[1])
    apiRequest = requests.get("http://localhost:5000/api/edit", data=jobCodec, headers={"Content-Type" : "application/json"})
    jsonRequestEdit = json.loads(apiRequest.content)
    sendToConsultData = {
        "name" : jobsToWork[1]["name"],
        "token" : token_object["teste"]
    }
    apiRequest = requests.get("http://localhost:5000/api/consult", params=sendToConsultData)
    jsonRequestConsult = json.loads(apiRequest.content)
    jobsToWork[1].pop("token")
    jobsToWork[1].pop("job_name_edit")

    assert jsonRequestInsert["status"] == "success", "Normal job but the status has unsuccess to insert"
    assert jsonRequestEdit["status"] == "success", "The job don't has edited correctly"
    assert jsonRequestConsult["status"] == "success", "The job don't was consult correct"
    jsonRequestConsult.pop("status")
    assert jsonRequestConsult == jobsToWork[1], "The data don't has equal"
    assert deleteDataInserted([jobsToWork[1]["name"]], token_object["admin"]) == True, "The data don't has deleted correctly"

    return True

def test_api_edit_with_cross_dependence(token_object, get_jobs_data):
    jobsToWork = get_jobs_data["CrossDependenceBetween"]

    jobsToWork[0].update({"token" : token_object["admin"]})
    jobCodec = json.dumps(jobsToWork[0])
    apiRequest = requests.get("http://localhost:5000/api/insert", data=jobCodec, headers={"Content-Type" : "application/json"})
    jsonRequestInsert = json.loads(apiRequest.content)

    jobsToWork[1].update({
        "token" : token_object["admin"],
        "job_name_edit" : jobsToWork[0]["name"]
    })
    jobCodec = json.dumps(jobsToWork[1])
    apiRequest = requests.get("http://localhost:5000/api/edit", data=jobCodec, headers={"Content-Type" : "application/json"})
    jsonRequestEdit = json.loads(apiRequest.content)

    assert jsonRequestInsert["status"] == "success", "Normal job but the status has unsuccess to insert"
    assert jsonRequestEdit["status"] == "unsuccess" and jsonRequestEdit["log"] == "There is cross dependence in this jobs!", "The job edtion don't will be working"

def test_api_edit_with_name_exists(token_object, get_jobs_data):
    jobsToWork = get_jobs_data["NamesDifferent"]
    jsonRequestsInsert = []
    for index in range(2):
        jobsToWork[index].update({"token" : token_object["admin"]})
        jobCodec = json.dumps(jobsToWork[index])
        apiRequest = requests.get("http://localhost:5000/api/insert", data=jobCodec, headers={"Content-Type" : "application/json"})
        jsonRequestsInsert.append(json.loads(apiRequest.content)["status"])

    jobToEdit = get_jobs_data["NamesEqual"][0]
    jobToEdit.update({
        "name" : jobsToWork[0]["name"],
        "token" : token_object["admin"],
        "job_name_edit" : jobsToWork[1]["name"]
    })
    jobCodec = json.dumps(jobToEdit)
    apiRequest = requests.get("http://localhost:5000/api/edit", data=jobCodec, headers={"Content-Type" : "application/json"})
    jsonRequestEdit = json.loads(apiRequest.content)

    assert "unsuccess" not in jsonRequestsInsert, "Normal job but the status has unsuccess to insert"
    assert jsonRequestEdit["status"] == "unsuccess" and jsonRequestEdit["log"] == "There is a job with this name", "The job edtion don't will be working"