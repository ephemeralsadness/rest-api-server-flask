"""
Application module.

It contains handle descriptions and works
with database manager
"""
import json
from flask import Flask, jsonify, request, send_file, Response

from db_manager import DBManager

app = Flask(__name__)
db_manager = DBManager()


@app.route('/user/', methods=['POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        successful_registration = db_manager.register_user(username, password)
        return jsonify({
            'success': successful_registration
        })
    return None


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
    elif request.method == 'PUT':
        task_done = json.loads(request.form['task_done'])
        db_manager.refresh_task(username, task_id, task_done)
    elif request.method == 'DELETE':
        db_manager.delete_task(username, task_id)

    return jsonify({
        'success': True
    })


@app.route('/files/', methods=['GET', 'POST'])
@app.route('/files/<string:filename>/', methods=['GET', 'DELETE'])
def file(filename=None):
    username = request.form['username']
    password = request.form['password']

    if not db_manager.login_user(username, password):
        return jsonify({
            'success': False
        })

    file_writer = db_manager.get_file_writer()

    if request.method == 'GET':
        if filename:
            filepath = file_writer.get(username, filename)
            if filepath is not None:
                return send_file(filepath)
        else:
            return jsonify({
                'success': True,
                'files': file_writer.files(username)
            })
    elif request.method == 'POST':
        if 'file' in request.files:
            file_writer.save(username, request.files['file'])
        return jsonify({
            'success': True
        })
    elif request.method == 'DELETE':
        file_writer.remove(username, filename)
        return jsonify({
            'success': True
        })

    return Response('{"success": false}',
                    status=400,
                    mimetype='application/json')


if __name__ == '__main__':
    app.run()
