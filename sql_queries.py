
class QUERIES:
    CREATE_USERS_TABLE = '''
        CREATE TABlE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        );
    '''

    CREATE_TASKS_TABLE = '''
        CREATE TABlE IF NOT EXISTS tasks(
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            task_name TEXT NOT NULL,
            is_done INTEGER NOT NULL
        );
    '''

    GET_USER = '''
        SELECT password
        FROM users
        WHERE username = ?
        LIMIT 1;
    '''

    CREATE_USER = '''
        INSERT INTO users
        (username, password)
        VALUES (?, ?);
    '''

    GET_USER_TODOLIST = '''
        SELECT task_id, task_name, is_done
        FROM tasks
        WHERE username = ?;
    '''

    ADD_TASK = '''
        INSERT INTO tasks
        (username, task_name, is_done)
        VALUES (?, ?, 0);
    '''

    DELETE_TASK = '''
        DELETE FROM tasks
        WHERE task_id = ? AND username = ?
    '''

    REFRESH_TASK = '''
        UPDATE tasks
        SET is_done = ?
        WHERE task_id = ? AND username = ?;
    '''