from docs.backend.jobs import Jobs
import pytest
import requests
import json
import secrets

@pytest.fixture
def token_object():
    token_admin = requests.get("http:/localhost:5000/api/getoken", params={
        "username" : "adm",
        "password" : "adm"
    }).content
    token_public = requests.get("http:/localhost:5000/api/getoken", params={
        "username" : "teste",
        "password" : "teste"
    }).content
    jsonObjectTokenAdmin = json.loads(token_admin)
    jsonObjectTokenPublic = json.loads(token_public)
    assert jsonObjectTokenAdmin["status"] == "success", "Token admin is incorrect status receive"
    assert jsonObjectTokenPublic["status"] == "success", "Token public is incorrect status receive"

    return (jsonObjectTokenAdmin["token"], jsonObjectTokenPublic["token"])

@pytest.fixture
def get_jobs_data():
    tasksLists = []
    for tasks in range():
        tasksLists.append({
            'name' : secrets.token_urlsafe(4),
            'weight' : secrets.choice([ k for k in range(1.11)]),
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
            "tasks" : ""
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
            "tasks" : ""
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
        "tasks" : ""
        })
    twoJobsCrossDependenceList.append({
        'name' : parentJobName,
        'active' : secrets.choice([False, True]),
        'parentJob' : {
            'name' : nameJob,
            'active' : secrets.choice([False, True])},
        "tasks" : ""
        })
    
    return {
        "tasksList" : tasksLists,
        "NamesDifferent" : twoJobNamesDifferentList,
        "NamesEqual" : twoJobSameNameList,
        "CrossDependenceBetween" : twoJobsCrossDependenceList
    }



def test_api_consult_without_result(token_object):
    permissions = ["all", "consult"]
    tokensPropertys = zip(token_object, permissions)

    for index in range(2):
        apiRequest = requests.get("http://localhost:5000/api/consult", params={
            "token" : tokensPropertys[index][0],
            "name" : "dont_exists"
        })
        response = json.loads(apiRequest.content)
        assert response["status"] == "unsuccess", "Status has success but this job doesn't exists"
        assert response["log"] == "This job doesn't exists", "Message incorrect to this case"

def test_api_insert_data_without_error(token_object, get_jobs_data):
    permissions = ["all", "consult"]
    tokensPropertys = zip(token_object, permissions)

    for index in range(2):
        apiRequest = requests.get("http://localhost:5000/api/insert", params={
            "token" : tokensPropertys[index][0],
            "name" : "dont_exists"
        })
        response = json.loads(apiRequest.content)
        assert response["status"] == "unsuccess", "Status has success but this job doesn't exists"
        assert response["log"] == "This job doesn't exists", "Message incorrect to this case"
        
