

class DBManager:

    def __init__(self):
        # username -> {password, list}
        self.users = {}

    def login_user(self, username, password):
        return username in self.users and self.users[username]['password'] == password

    def register_user(self, username, password):
        if username in self.users:
            return False

        self.users[username] = {}
        self.users[username]['password'] = password
        self.users[username]['todo_list'] = []
        return True

    def get_todo_list(self, username):
        return self.users[username]['todo_list']

    def add_task(self, username, task_name):
        task = {
            'name': task_name,
            'done': False
        }
        self.users[username]['todo_list'].append(task)

    def delete_task(self, username, task_id):
        current_user_list = self.users[username]['todo_list']
        assert (0 <= task_id < len(current_user_list))
        current_user_list.pop(task_id)

    def refresh_task(self, username, task_id, task_done):
        current_user_list = self.users[username]['todo_list']
        assert (0 <= task_id < len(current_user_list))
        current_user_list[task_id]['done'] = task_done
