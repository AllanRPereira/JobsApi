import sqlalchemy as sql

engine = sql.create_engine("sqlite:///:memory:")
connection = engine.connect()

userMeta = sql.MetaData()
tableUser = sql.Table(
    "user", userMeta,
    sql.Column("id", sql.Integer, primary_key=True),
    sql.Column("user", sql.String),
    sql.Column("color", sql.String),
    sql.Column("age", sql.ARRAY(sql.String))
)
userMeta.create_all(engine)
insertQ = tableUser.insert().values(user="Madara", color="Black", age=["ohh", "tata"])
idThisJob = connection.execute(insertQ).inserted_primary_key[0]
print(idThisJob)
insertQ = tableUser.insert().values(user="Madara", color="Blue", age=["dsds", "dd"])
idThisJob = connection.execute(insertQ).inserted_primary_key[0]
print(idThisJob)
insertQ = tableUser.insert().values(user="Madara", color="Yellow", age=["ohaah", "cc"])
idThisJob = connection.execute(insertQ).inserted_primary_key[0]
print(idThisJob)

selectQ = sql.select([tableUser.c.color, tableUser.c.age]).where(tableUser.c.user == "Madara")
selectValue = connection.execute(selectQ)
print(selectValue)
print(selectValue.fetchall())