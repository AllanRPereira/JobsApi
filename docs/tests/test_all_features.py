from ..jobs.jobs import Jobs, Tasks
from ..database.database import DatabaseConnection

exampleJobCorrectOne = {
        'name' : 'First Job Teste',
        'active' : True,
        'parentJob' : {
            'name' : 'Second Job Teste',
            'active' : False
        },
        'tasks' : [{
                'name' : 'Task open Mp3 Test',
                'weight' : 4,
                'completed' : False,
                'createdAt' : '2020-04-20'
            }, {
                'name' : 'Task open Manager Test',
                'weight' : 2,
                'completed' : True,
                'createdAt' : '2020-04-15'
            }
        ]
    }
exampleJobCorrectTwo = {
        'name' : 'First Job Teste',
        'active' : True,
        'parentJob' : {
            'name' : 'Three Job Teste',
            'active' : False
        },
        'tasks' : [{
                'name' : 'Task open Mp4 Test',
                'weight' : 4,
                'completed' : False,
                'createdAt' : '2020-04-20'
            }, {
                'name' : 'Task open Chrome Test',
                'weight' : 2,
                'completed' : True,
                'createdAt' : '2020-04-15'
            }
        ]
    }

exampleJobCorrecThree = {
        'name' : 'Four Job Teste',
        'active' : True,
        'parentJob' : {
            'name' : 'Three Job Teste',
            'active' : False
        },
        'tasks' : [{
                'name' : 'Task open Vscode Test',
                'weight' : 4,
                'completed' : False,
                'createdAt' : '2020-04-20'
            }, {
                'name' : 'Clean logs',
                'weight' : 2,
                'completed' : True,
                'createdAt' : '2020-04-15'
            }
        ]
    }

exampleJobCorrectFour = {
        'name' : 'Five Job Teste',
        'active' : True,
        'parentJob' : {
            'name' : 'Three Job Teste',
            'active' : False
        },
        'tasks' : [{
                'name' : 'Test application',
                'weight' : 4,
                'completed' : False,
                'createdAt' : '2020-04-20'
            }, {
                'name' : 'Generation logs',
                'weight' : 2,
                'completed' : True,
                'createdAt' : '2020-04-15'
            }
        ]
    }

exampleTaskCorrect = {
        'name' : 'Task open Browser Test',
        'weight' : 8,
        'completed' : True,
        'createdAt' : '2020-04-08'
    }

exampleJobSameNames = {
        'name' : 'First Job Teste',
        'active' : True,
        'parentJob' : {
            'name' : 'First Job Teste',
            'active' : False
        },
        'tasks' : [{
                'name' : 'Task open Mp3 Test',
                'weight' : 4,
                'completed' : False,
                'createdAt' : '2020-04-20'
            }, {
                'name' : 'Task open Manager Test',
                'weight' : 2,
                'completed' : True,
                'createdAt' : '2020-04-15'
            }
        ]
    }
exampleJobWithCrossDependence = {
        'name' : 'Second Job Teste',
        'active' : True,
        'parentJob' : {
            'name' : 'First Job Teste',
            'active' : False
        },
        'tasks' : [{
                'name' : 'Task open Mp3 Test',
                'weight' : 4,
                'completed' : False,
                'createdAt' : '2020-04-20'
            }, {
                'name' : 'Task open Manager Test',
                'weight' : 2,
                'completed' : True,
                'createdAt' : '2020-04-15'
            }
        ]
    }

def test_create_a_task():
    global exampleTaskCorrect
    taskInstance = Tasks(**exampleTaskCorrect)
    assert taskInstance.getAttributes() == exampleTaskCorrect, "Task não foi criada corretamente!"

def test_create_job():
    global exampleJobCorrectOne
    jobInstance = Jobs(**exampleJobCorrectOne)
    assert jobInstance.getAttributes() == exampleJobCorrectOne, "Job não foi criado corretamente!"

def test_create_job_with_name_equal_parent():
    global exampleJobSameNames
    try:
        Jobs(**exampleJobSameNames)
    except Exception:
        return True
    assert False,"Don't possible create job with the same name' parent"
        
def test_cross_dependency_without_error():
    global exampleJobCorrectOne
    jobInstance = Jobs(**exampleJobCorrectOne)

    database = DatabaseConnection()
    assert database.checkCrossDependence(jobInstance) == True, "Check Cross Dependence is not working"

def test_insert_database_with_cross_dependecy():
    global exampleJobCorrectOne
    jobInstanceOne = Jobs(**exampleJobCorrectOne)

    global exampleJobWithCrossDependence
    jobInstanceTwo = Jobs(**exampleJobWithCrossDependence)
    database = DatabaseConnection()
    database.insert(jobInstanceOne)
    try:
        database.insert(jobInstanceTwo)
    except Exception:
        return True

    assert False, "Check Cross Dependence is not working in real case"

def test_insert_database_with_same_name():
    global exampleJobCorrectOne
    jobInstanceOne = Jobs(**exampleJobCorrectOne)

    global exampleJobCorrectTwo
    jobInstanceTwo = Jobs(**exampleJobCorrectTwo)
    database = DatabaseConnection()
    database.insert(jobInstanceOne)
    try:
        database.insert(jobInstanceTwo)
    except Exception:
        return True
    assert False, "There is a same name in job, but don't has a error!"

def test_consult_job():
    global exampleJobCorrectOne
    jobInstanceOne = Jobs(**exampleJobCorrectOne)

    global exampleJobCorrecThree
    jobInstanceTwo = Jobs(**exampleJobCorrecThree)

    database = DatabaseConnection()
    database.insert(jobInstanceOne)
    database.insert(jobInstanceTwo)
    valoresJobConsultado = database.consult(jobInstanceOne.getAttributes()["name"])
    assert valoresJobConsultado == jobInstanceOne.getAttributes(), "Valor consultado não está sendo retornando como valor original"

def test_consult_job_without_exist():
    global exampleJobCorrectOne
    jobInstanceOne = Jobs(**exampleJobCorrectOne)

    database = DatabaseConnection()
    database.insert(jobInstanceOne)

    assert database.consult(jobName="Job don't exist") == False, "Não está retornando adequadamente quando não há o Job"

def test_edition_job_correct():

    global exampleJobCorrectOne
    jobInstanceOne = Jobs(**exampleJobCorrectOne)

    global exampleJobCorrectTwo
    jobInstanceTwo = Jobs(**exampleJobCorrectTwo)

    global exampleJobCorrecThree
    jobInstanceThree = Jobs(**exampleJobCorrecThree)

    database = DatabaseConnection()
    database.insert(jobInstanceOne)
    database.insert(jobInstanceThree)
    assert database.edition(jobInstanceTwo, jobName="First Job Teste"), "Update não foi realizado" 
    assert database.consult(jobInstanceTwo.getAttributes()['name']) == jobInstanceTwo.getAttributes(), "Não está inserindo corretamente"

def test_edition_job_incorrect():
    """
    Testa editando Job com nome que já existe
    """
    global exampleJobCorrectOne
    jobInstanceOne = Jobs(**exampleJobCorrectOne)

    global exampleJobCorrectTwo
    jobInstanceTwo = Jobs(**exampleJobCorrectTwo)

    global exampleJobCorrecThree
    jobInstanceThree = Jobs(**exampleJobCorrecThree)

    database = DatabaseConnection()
    database.insert(jobInstanceOne)
    database.insert(jobInstanceThree)
    nameJobThree = jobInstanceThree.getAttributes()['name']
    nameJobOne = jobInstanceOne.getAttributes()['name']
    'jobInstanceTwo tem o mesmo nome do jobInstanceOne'
    assert not database.edition(jobInstanceTwo, jobName=nameJobThree), "Há conflito de nomes"

def test_edition_job_with_cross_dependence():

    global exampleJobCorrectOne
    jobInstanceOne = Jobs(**exampleJobCorrectOne)

    global exampleJobCorrecThree
    jobInstanceThree = Jobs(**exampleJobCorrecThree)

    global exampleJobWithCrossDependence
    jobInstanceCross = Jobs(**exampleJobWithCrossDependence)

    database = DatabaseConnection()
    database.insert(jobInstanceOne)
    database.insert(jobInstanceThree)
    assert not database.edition(jobInstanceCross, jobName=jobInstanceThree.getAttributes()['name']), "Está havendo dependência cruzada na edição"

def test_exclusion_job():
    global exampleJobCorrectOne
    jobInstanceOne = Jobs(**exampleJobCorrectOne)

    global exampleJobCorrecThree
    jobInstanceThree = Jobs(**exampleJobCorrecThree)

    database = DatabaseConnection()
    database.insert(jobInstanceOne)
    database.insert(jobInstanceThree)

    assert database.consult(jobName=exampleJobCorrectOne['name']) != False, "Não consultou adequadamente"
    assert database.exclusion(jobName=exampleJobCorrectOne['name']), "Não deletou corretamente"
    assert database.consult(jobName=exampleJobCorrectOne['name']) == False, "Valor ainda existe no banco de dados"