from database.DataBase import Database


def start():
    db = Database()

    print(db)

    # data = ['qw','qw','qw','qw']
    # data1 = ['qw','wq','qw']

    # db.insertDataOneInTable('user', data)
    # db.insertDataOneInTable('music', data)
    db.clearTable('user')
    db.clearTable('music')