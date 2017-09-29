#!/usr/bin/env python3
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
from functools import wraps
from .tasks import retrieve_dbdata, make_tasks_list, add_task_to_db, \
        remove_task_from_db, update_task_in_db

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'cash':
        return 'pass'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response
    http://flask.pocoo.org/snippets/100/"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator


def defaultheaders(f):
    """If you want to set some more default headers,
    append them to this dict"""
    headers = {'Access-Control-Allow-Origin': '*'}

    @wraps(f)
    @add_response_headers({'Access-Control-Allow-Origin': '*'})
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'],
                                      _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
@defaultheaders
def get_tasks():
    tasks = make_tasks_list(retrieve_dbdata())
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@defaultheaders
def get_task(task_id):
    tasks = make_tasks_list(retrieve_dbdata())
    task = [task for task in tasks if task['id'] == task_id]
    if not task:
        abort(404)
    return jsonify({'task': make_public_task(task[0])})


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@defaultheaders
def add_task():
    task = {
        'title': request.form['user'],
        'description': request.form['description'],
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'done': False
    }
    add_task_to_db(task)
    return get_tasks()

def test():
    if not request.json or 'title' not in request.json:
        print("Error: " + request.json)
        abort(404)
    print("Hi")
    task = {
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'done': False
    }
    add_task_to_db(task)
    return get_tasks()


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@defaultheaders
def update_task(task_id):
    tasks = make_tasks_list(retrieve_dbdata())
    task = [task for task in tasks if task['id'] == task_id]
    if not task:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and \
       type(request.json['description']) != str:
        abort(400)
    if 'date' in request.json and type(request.json['date']) != str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) != bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description',
                                              task[0]['description'])
    task[0]['date'] = request.json.get('date', task[0]['date'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    update_task_in_db(task[0])
    return get_tasks(), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@defaultheaders
def delete_task(task_id):
    tasks = make_tasks_list(retrieve_dbdata())
    task = [task for task in tasks if task['id'] == task_id]
    if not task:
        abort(404)
    remove_task_from_db(task_id)
    return get_tasks(), 201


if __name__ == '__main__':
    app.run(debug=True)
