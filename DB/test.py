from DataBase import *

db = DataBase()

print(db)

# data = ['qw','qw','qw','qw']
# data1 = ['qw','wq','qw']

# db.insertDataOneInTable('user', data)
# db.insertDataOneInTable('music', data)
db.clearTable('user')
db.clearTable('music')