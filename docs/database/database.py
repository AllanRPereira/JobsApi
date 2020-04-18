import sqlalchemy as alchemy
import datetime
from docs.tablemodels.tablemodels import tableBaseClass

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
        attributesJobWithoutTasks['parentJob'] = "&".join([
            attributesJob["parentJob"]["name"],
            str(int(attributesJob["parentJob"]["active"]))
        ])

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

    def edition(self, jobInstance):
        attributesJob = jobInstance.getAttributes()
        attributesJobWithoutTasks = attributesJob.copy()
        attributesJobWithoutTasks.pop("tasks")
        attributesJobWithoutTasks['parentJob'] = attributesJobWithoutTasks['parentJob']['name']
        whereCondition = self.jobTable.c.name == attributesJob['name']
        updateJobQuery = self.jobTable.update().where(whereCondition).values(**attributesJobWithoutTasks)
        idThisJob = self.connection.execute(updateJobQuery).inserted_primary_key[0]

        for attributesTask in attributesJob['tasks']:
            attributesTask['idJobForeignKey'] = idThisJob
            dateToDb = datetime.datetime(*[int(strDate) for strDate in attributesTask['createdAt'].split("-")])
            attributesTask['createdAt'] = dateToDb
            whereCondition = self.taskTable.c.idJobForeignKey == idThisJob
            updateTasksQuery = self.taskTable.update().where(whereCondition).values(**attributesTask)
            self.connection.execute(updateTasksQuery)
        
        return True

    def exclusion(self, jobName):
        whereCondition = self.jobTable.c.name == jobName
        deleteJobQuery = self.jobTable.delete().where(whereCondition)
        idThisJob = self.connection.execute(deleteJobQuery).lastrowid[0]

        whereCondition = self.taskTable.c.idJobForeignKey == idThisJob
        deleteTaskQuery = self.taskTable.delete().where(whereCondition)
        numberOfTasksDeleted = self.connection.execute(deleteTaskQuery).rowcount

        return numberOfTasksDeleted

    def consult(self, jobName):
        whereCondition = self.jobTable.c.name == jobName
        selectJobQuery = self.jobTable.select().where(whereCondition)
        idJob, name, active, parentJob = self.connection.execute(selectJobQuery).fetchone()
        parentJob = parentJob.split("&")
        parentJob = {
            "name" : parentJob[0],
            "active" : bool(int(parentJob[1]))
        }

        JobDictionary = {
            "name" : name,
            "active" : active,
            "parentJob" : parentJob
        }

        whereCondition = self.taskTable.c.idJobForeignKey == idJob
        takTab = self.taskTable
        columnsToSelect = [takTab.c.name, takTab.c.weight, takTab.c.completed, takTab.c.createdAt]
        selectTaskQuery = alchemy.select(columnsToSelect).where(whereCondition)
        taskValues = self.connection.execute(selectTaskQuery).fetchall()
        newTaskValues = []
        for task in taskValues:
            name, weight, completed, createdAt = task
            dateString = f"{createdAt.year:04d}-{createdAt.month:02d}-{createdAt.day:02d}"
            newTaskValues.append({
                "name" : name,
                "weight" : weight,
                "createdAt" : dateString,
                "completed" : completed
            })

        JobDictionary["tasks"] = newTaskValues

        return JobDictionary

