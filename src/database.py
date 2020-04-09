import sqlalchemy as alchemy
import datetime
from JobsApi.src.tablemodels import tableBaseClass

class DatabaseConnection:
    
    def __init__(self):
        self.engineDatabase = alchemy.create_engine("sqlite:///:memory:")
        tableBaseClass.metadata.create_all(self.engineDatabase)
        self.jobTable, self.taskTable = tableBaseClass.metadata.tables['jobs_table'], tableBaseClass.metadata.tables['tasks_table']
        self.connection = self.engineDatabase.connect()

    def insert(self, jobInstance):
        if not self.checkCrossDependence(jobInstance):
            raise Exception("There is cross dependence in this jobs!")

        attributesJob = jobInstance.getAttributes()
        attributesJobWithoutTasks = attributesJob.copy()
        attributesJobWithoutTasks.pop("tasks")
        attributesJobWithoutTasks['parentJob'] = attributesJobWithoutTasks['parentJob']['name']

        insertJobQuery = self.jobTable.insert().values(**attributesJobWithoutTasks)
        idThisJob = self.connection.execute(insertJobQuery).inserted_primary_key[0]
        for attributesTask in attributesJob['tasks']:
            attributesTask['idJobForeignKey'] = idThisJob
            dateToDb = datetime.datetime(*[int(strDate) for strDate in attributesTask['createdAt'].split("-")])
            attributesTask['createdAt'] = dateToDb
            insertTasksQuery = self.taskTable.insert().values(**attributesTask)
            self.connection.execute(insertTasksQuery)
        
        return True
    
    def checkCrossDependence(self, jobInstance):
        attributesJob = jobInstance.getAttributes()
        nameJob = attributesJob['name']
        parentJob = attributesJob['parentJob']
        selectCondition = self.jobTable.c.parentJob
        whereCondition = self.jobTable.c.name == parentJob['name']
        selectParentJob = alchemy.select([selectCondition])
        results = self.connection.execute(selectParentJob).fetchone()
        if results:
            if nameJob == results[0]:
                return False
        return True

    def edition(self, jobInstance, taskInstance=None):
        pass
    
    def exclusion(self, jobName):
        pass

    def consult(self, jobName):
        pass


