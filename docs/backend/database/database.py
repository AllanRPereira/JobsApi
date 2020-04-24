import sqlalchemy as alchemy
import datetime
from docs.backend.tablemodels.tablemodels import tableBaseClass
from docs.backend.jobs.jobs import Jobs

class DatabaseConnection:
    
    def __init__(self):
        self.engineDatabase = alchemy.create_engine("sqlite:///:memory:", connect_args={"check_same_thread" : False})
        tableBaseClass.metadata.create_all(self.engineDatabase)
        self.jobTable, self.taskTable = tableBaseClass.metadata.tables['jobs_table'], tableBaseClass.metadata.tables['tasks_table']
        self.connection = self.engineDatabase.connect()

    def insert(self, jobInstance):
        if not self.checkCrossDependence(jobInstance):
            return (False, "There is cross dependence in this jobs!")

        attributesJob = jobInstance.getAttributes()
        attributesJobWithoutTasks = attributesJob.copy()
        attributesJobWithoutTasks.pop("tasks")
        attributesJobWithoutTasks['parentJob'] = jobInstance.getParentParse()

        insertJobQuery = self.jobTable.insert().values(**attributesJobWithoutTasks)
        idThisJob = self.connection.execute(insertJobQuery).inserted_primary_key[0]
        for attributesTask in attributesJob['tasks']:
            attributesTask['idJobForeignKey'] = idThisJob
            dateToDb = datetime.datetime(*[int(strDate) for strDate in attributesTask['createdAt'].split("-")])
            attributesTask['createdAt'] = dateToDb
            insertTasksQuery = self.taskTable.insert().values(**attributesTask)
            self.connection.execute(insertTasksQuery)
        
        return (True, "")

    def checkCrossDependence(self, jobInstance):
        attributesJob = jobInstance.getAttributes()
        nameJob = attributesJob['name']
        parentJob = attributesJob['parentJob']
        selectCondition = self.jobTable.c.parentJob
        whereCondition = self.jobTable.c.name == parentJob['name']
        selectParentJob = alchemy.select([selectCondition])
        results = self.connection.execute(selectParentJob).fetchone()
        if results:
            if nameJob == results[0].split("&")[0]:
                return False
        return True

    def edition(self, jobInstance, jobName=False, jobInstancePrimary=False):
        if not self.checkCrossDependence(jobInstance):
            return (False, "There is cross dependence in this jobs!")
        elif jobName:
            nameWhere = jobName
        elif jobInstancePrimary:
            nameWhere = jobInstancePrimary.getAttributes()["name"]
        else:
            return (False, "JobName is not passed")

        attributesJobToUpdate = jobInstance.getAttributes()
        attributesJobWithoutTasks = attributesJobToUpdate.copy()
        attributesJobWithoutTasks.pop("tasks")
        attributesJobWithoutTasks['parentJob'] = jobInstance.getParentParse()
        whereCondition = self.jobTable.c.name == nameWhere
        updateJobQuery = self.jobTable.update().where(whereCondition).values(**attributesJobWithoutTasks)
        try:
            self.connection.execute(updateJobQuery)
        except alchemy.exc.IntegrityError:
            return (False, "There is a job with this name")
        queryIdExecute = alchemy.select([self.jobTable.c.idJob]).where(self.jobTable.c.name == attributesJobWithoutTasks['name'])
        idThisJob = self.connection.execute(queryIdExecute).fetchone()[0]
        tasksNameQuery = alchemy.select([self.taskTable.c.name]).where(self.taskTable.c.idJobForeignKey == idThisJob)
        taskNameList = self.connection.execute(tasksNameQuery).fetchall()
        for attributesTask, namesTaskDb in zip(attributesJobToUpdate['tasks'], taskNameList):
            attributesTask['idJobForeignKey'] = idThisJob
            dateToDb = datetime.datetime(*[int(strDate) for strDate in attributesTask['createdAt'].split("-")])
            attributesTask['createdAt'] = dateToDb
            whereCondition = alchemy.and_(self.taskTable.c.idJobForeignKey == idThisJob, self.taskTable.c.name == namesTaskDb[0])
            updateTasksQuery = self.taskTable.update().where(whereCondition).values(**attributesTask)
            self.connection.execute(updateTasksQuery)

        return (True, "")

    def exclusion(self, jobName):
        idJobQuery = alchemy.select([self.jobTable.c.idJob]).where(self.jobTable.c.name == jobName)
        idThisJob = self.connection.execute(idJobQuery).fetchone()[0]
        whereCondition = self.jobTable.c.name == jobName
        deleteJobQuery = self.jobTable.delete().where(whereCondition)
        self.connection.execute(deleteJobQuery)

        whereCondition = self.taskTable.c.idJobForeignKey == idThisJob
        deleteTaskQuery = self.taskTable.delete().where(whereCondition)
        numberOfTasksDeleted = self.connection.execute(deleteTaskQuery).rowcount

        return (True, numberOfTasksDeleted)

    def consult(self, jobName):
        whereCondition = self.jobTable.c.name == jobName
        selectJobQuery = self.jobTable.select().where(whereCondition)
        selectJobValues = self.connection.execute(selectJobQuery).fetchone()
        if not selectJobValues:
            return (False, "This job doesn't exists")
        else:
            idJob, name, active, parentJob = selectJobValues
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
        JobDictionary["tasks"] = newTaskValues.copy()

        return (True, JobDictionary.copy())

