import image_hosting


class User:
    class UserAlreadExistsException(Exception): 
        def __str__(self):
            return 'User with that username already exists!'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.table = 'users'

    def save(self):
        if image_hosting.get_object(self.table, **{'username': self.username}) == []:
            sql = "INSERT INTO users (username, password) VALUES (?, ?);"
            db = image_hosting.get_db()  # while inserting have to call db.commit (connection)
            cursor = image_hosting.get_cursor()
            cursor.execute(sql, (self.username, self.password))
            db.commit()  # connection commit
        else:
            return self.UserAlreadExistsException()

    def is_created(self):
        if image_hosting.get_object(self.table, **{'username': self.username}):
            return True
        return False