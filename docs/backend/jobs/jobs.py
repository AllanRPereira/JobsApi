class Jobs:
    def __init__(self, name, active=False, parentJob=False, tasks=[], *args, **kwargs):

        #Check relative of himself throught name attribute
        if parentJob != False:
            if parentJob['name'] == name:
                raise Exception("ParentJob can't have same name of the principal job")

        self.name = name
        self.active = active
        self.parentJob = parentJob
        self.tasks = [Tasks(**task) for task in tasks]

    def getAttributes(self):
        attributes = {
            'name' : self.name,
            'active' : self.active,
            'parentJob' : self.parentJob,
            'tasks' : [task.getAttributes() for task in self.tasks]
        }
        return attributes
    
    def getParentParse(self):
        
        return "&".join([
            self.parentJob["name"],
            str(int(self.parentJob["active"]))
        ])
    
class Tasks:
    def __init__(self, name, weight, completed, createdAt, *args, **kwargs):
        self.name = name
        self.weight = weight
        self.completed = completed
        self.createdAt = createdAt
    
    def getAttributes(self):
        attributes = {
            'name' : self.name,
            'weight' : self.weight,
            'completed' : self.completed,
            'createdAt' : self.createdAt
        }
        return attributes