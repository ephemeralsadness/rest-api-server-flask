import json

from db_manager import DBManager
from flask import Flask, jsonify, request

app = Flask(__name__)
db_manager = DBManager()


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'Hello': 'world!'
    })


@app.route('/user/', methods=['POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        successful_registration = db_manager.register_user(username, password)
        return jsonify({
            'success': successful_registration
        })


@app.route('/todo/', methods=['GET', 'POST'])
@app.route('/todo/<int:task_id>/', methods=['PUT', 'DELETE'])
def todo(task_id=None):
    username = request.form['username']
    password = request.form['password']

    if not db_manager.login_user(username, password):
        return jsonify({
            'success': False
        })

    if request.method == 'GET':
        task_list = db_manager.get_todo_list(username)
        return jsonify({
            'success': True,
            'todo_list': task_list
        })
    elif request.method == 'POST':
        task_name = request.form['task_name']
        db_manager.add_task(username, task_name)
        return jsonify({
            'success': True
        })
    elif request.method == 'PUT':
        task_done = json.loads(request.form['task_done'])
        db_manager.refresh_task(username, task_id, task_done)
        return jsonify({
            'success': True
        })
    elif request.method == 'DELETE':
        db_manager.delete_task(username, task_id)
        return jsonify({
            'success': True
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
