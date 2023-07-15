import sqlite3

from object.User import User


class Db():

    def __init__(self):
        self.sqlite_connection = sqlite3.connect('sqlite_python.db')

    def add_new_user(self, user):
        select = 'select * from users where name = ?'
        cursor = self.sqlite_connection.cursor()
        cursor.execute(select, (user.name,))
        results = cursor.fetchall()
        cursor.close()
        if results.__len__() == 0:
            print('Новый пользователь')
            query = "INSERT INTO users(name, city, sex) VALUES(?,?,?)"
            cursor = self.sqlite_connection.cursor()
            cursor.execute(query, (user.name, user.city, user.sex,))
            self.sqlite_connection.commit()
        else:
            print('Такой пользователь уже есть в системе')

    def seach_user(self, user: User, id_user:int):
        query = "select * from history_serch where seach_user_id = ? and id_user = ?"
        cursor = self.sqlite_connection.cursor()
        if cursor.execute(query, (user.id, id_user)):
            return cursor.fetchall()

    def add_seach_user(self, user: User, id_user:int):
        result_seach_user = self.seach_user(user, id_user)
        if result_seach_user.__len__() == 0:
            query = "INSERT INTO history_serch (seach_user_id, id_user) VALUES(?, ?)"
            cursor = self.sqlite_connection.cursor()
            cursor.execute(query, (user.id, id_user))
            self.sqlite_connection.commit()
            return True
        else:
            return False

    def close(self):
        if (self.sqlite_connection):
            self.sqlite_connection.close()
            print("Соединение с SQLite закрыто")
