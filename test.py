from src.jobs import Jobs, Tasks
from src.database import DatabaseConnection

def test_create_a_task():
    task_property = {
        'name' : 'Task open Browser Test',
        'weight' : 8,
        'completed' : True,
        'createdAt' : '2020-04-08'
    }
    taskInstance = Tasks(**task_property)
    assert taskInstance.getAttributes() == task_property, "Task não foi criada corretamente!"

def test_create_job():
    job_property = {
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
    jobInstance = Jobs(**job_property)
    assert jobInstance.getAttributes() == job_property, "Job não foi criado corretamente!"

def test_create_job_with_name_equal_parent():
    job_property = {
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
    try:
        Jobs(**job_property)
        assert "Don't possible create job with the same name' parent"
    except:
        pass
        
def test_cross_dependency_without_error():
    job_property = {
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
    jobInstance = Jobs(**job_property)

    database = DatabaseConnection()
    assert database.checkCrossDependence(jobInstance) == True, "Check Cross Dependence is not working"

def test_insert_database_with_cross_dependecy():
    job_property = {
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
    jobInstanceOne = Jobs(**job_property)

    job_property = {
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
    jobInstanceTwo = Jobs(**job_property)
    database = DatabaseConnection()
    database.insert(jobInstanceOne)
    try:
        database.insert(jobInstanceTwo)
        assert False, "Check Cross Dependence is not working in real case"
    except:
        return True

def test_insert_database_with_same_name():
    job_property = {
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
    jobInstanceOne = Jobs(**job_property)

    job_property = {
        'name' : 'First Job Teste',
        'active' : True,
        'parentJob' : {
            'name' : 'Three Job Teste',
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
    jobInstanceTwo = Jobs(**job_property)
    database = DatabaseConnection()
    database.insert(jobInstanceOne)
    try:
        database.insert(jobInstanceTwo)
        assert False, "There is a same name in job, but don't has a error!"
    except:
        return True
    
def test_consult_job():
    job_property = {
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
    jobInstanceOne = Jobs(**job_property)

    job_property = {
        'name' : 'Four Job Teste',
        'active' : True,
        'parentJob' : {
            'name' : 'Three Job Teste',
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
    jobInstanceTwo = Jobs(**job_property)

    database = DatabaseConnection()
    database.insert(jobInstanceOne)
    database.insert(jobInstanceTwo)
    valoresJobConsultado = database.consult(jobInstanceOne.getAttributes()["name"])
    assert valoresJobConsultado == jobInstanceOne.getAttributes(), "Valor consultado não está sendo retornando como valor original"

