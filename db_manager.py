from config import SALT, FILE_FOLDER
from hashlib import pbkdf2_hmac
import os
from os.path import join as pj
import sqlite3
from sql_queries import QUERIES
from werkzeug.utils import secure_filename


class FileWriter:
    def __init__(self, file_folder):
        # Absolute path to folder
        self.FILE_FOLDER = file_folder

    def save(self, username, file):
        filepath = pj(self.FILE_FOLDER, username, secure_filename(file.filename))
        file.save(filepath)

    def get(self, username, filename):
        filepath = pj(self.FILE_FOLDER, username, filename)
        if not os.path.exists(filepath):
            return None
        return filepath

    def files(self, username):
        folder_path = pj(self.FILE_FOLDER, username)
        if not os.path.isdir(folder_path):
            os.remove(folder_path)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        return os.listdir(folder_path)

    def remove(self, username, filename):
        filepath = pj(self.FILE_FOLDER, username, filename)
        if os.path.exists(filepath):
            os.remove(filepath)


class DBManager:

    def __init__(self):
        self.users = {}
        self.__connection = sqlite3.connect('users.db', check_same_thread=False)
        self.file_writer = FileWriter(FILE_FOLDER)

        cursor = self.__connection.cursor()
        cursor.execute(QUERIES.CREATE_USERS_TABLE)
        cursor.execute(QUERIES.CREATE_TASKS_TABLE)
        self.__connection.commit()

    def __del__(self):
        self.__connection.close()

    @staticmethod
    def __encrypt(password):
        key = pbkdf2_hmac('sha256', password.encode('utf-8'), SALT, 100000)
        return key

    def login_user(self, username, password):
        cursor = self.__connection.cursor()
        cursor.execute(QUERIES.GET_USER, (username,))
        rows = cursor.fetchall()
        self.__connection.commit()

        has_user = len(rows) != 0
        if not has_user:
            return

        real_password = rows[0][0]
        return self.__encrypt(password) == real_password

    def register_user(self, username, password):
        cursor = self.__connection.cursor()
        cursor.execute(QUERIES.GET_USER, (username,))
        username_rows = cursor.fetchall()
        self.__connection.commit()
        if len(username_rows) > 0:
            return False

        cursor.execute(QUERIES.CREATE_USER, (username, self.__encrypt(password)))
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

    def get_file_writer(self):
        return self.file_writer
