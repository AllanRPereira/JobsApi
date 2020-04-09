import sqlalchemy as alchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

tableBaseClass = declarative_base()

class Jobs(tableBaseClass):
    __tablename__ = "jobs_table"
    __table_args__ = (alchemy.UniqueConstraint('name'),)

    idJob = alchemy.Column('idJob', alchemy.Integer, primary_key=True)
    name = alchemy.Column('name', alchemy.String)
    active = alchemy.Column('active', alchemy.Boolean)
    parentJob = alchemy.Column('parentJob', alchemy.String)

class Tasks(tableBaseClass):
    __tablename__ = "tasks_table"

    idTask = alchemy.Column('idTask', alchemy.Integer, primary_key=True)
    name = alchemy.Column('name', alchemy.String)
    weight = alchemy.Column('weight', alchemy.Integer)
    completed = alchemy.Column('completed', alchemy.Boolean)
    createdAt = alchemy.Column('createdAt', alchemy.DateTime)
    idJobKey = alchemy.Column('idJobForeignKey', alchemy.Integer, alchemy.ForeignKey('jobs_table.idJob'))
    jobRelation = relationship("Jobs")