import sqlite3
from sql_queries import QUERIES


class DBManager:

    def __init__(self):
        self.users = {}
        self.__connection = sqlite3.connect('users.db', check_same_thread=False)

        cursor = self.__connection.cursor()
        cursor.execute(QUERIES.CREATE_USERS_TABLE)
        cursor.execute(QUERIES.CREATE_TASKS_TABLE)
        self.__connection.commit()

    def __del__(self):
        self.__connection.close()

    def login_user(self, username, password):
        cursor = self.__connection.cursor()
        cursor.execute(QUERIES.GET_USER, (username,))
        rows = cursor.fetchall()
        self.__connection.commit()

        has_user = len(rows) != 0
        if not has_user:
            return

        real_password = rows[0][0]
        return password == real_password

    def register_user(self, username, password):
        cursor = self.__connection.cursor()
        cursor.execute(QUERIES.GET_USER, (username,))
        username_rows = cursor.fetchall()
        self.__connection.commit()
        if len(username_rows) > 0:
            return False

        cursor.execute(QUERIES.CREATE_USER, (username, password))
        self.__connection.commit()
        return True

    def get_todo_list(self, username):
        cursor = self.__connection.cursor()
        cursor.execute(QUERIES.GET_USER_TODOLIST, (username,))
        rows = cursor.fetchall()
        self.__connection.commit()

        def task_row_to_object(row):
            return {
                'task_id': row[0],
                'name': row[1],
                'done': row[2]
            }

        return list(map(task_row_to_object, rows))

    def add_task(self, username, task_name):
        cursor = self.__connection.cursor()
        cursor.execute(QUERIES.ADD_TASK, (username, task_name))
        self.__connection.commit()

    def delete_task(self, username, task_id):
        cursor = self.__connection.cursor()
        cursor.execute(QUERIES.DELETE_TASK, (task_id, username))
        self.__connection.commit()

    def refresh_task(self, username, task_id, task_done):
        cursor = self.__connection.cursor()
        cursor.execute(QUERIES.REFRESH_TASK, (task_done, task_id, username))
        self.__connection.commit()
