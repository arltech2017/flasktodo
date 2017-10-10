import sqlite3
import os

TESTING_DB_PATH = 'todo/test_todo.db'


def get_connection():
    global src_path
    database_path = "{}/todo/todo.db".format(src_path)
    if os.environ.get('TESTING') == 'True':
        database_path = TESTING_DB_PATH
    return sqlite3.connect(database_path)


def drop_testing_database():
    os.remove(TESTING_DB_PATH)


def retrieve_dbdata():
    """
    Read and return all todo items from the database.
    """
    conn = get_connection()
    cur = conn.execute('SELECT * FROM items')
    items = cur.fetchall()
    conn.close()
    return items


def add_task_to_db(task):
    """
    Add a new task to the task database.
    """
    conn = get_connection()
    insertstmt = "INSERT INTO items (title, date, description, done) "
    insertstmt += "VALUES (?, ?, ?, ?)"
    title = task['title']
    date = task['date']
    desc = task['description']
    done = task['done']
    conn.execute(insertstmt, (title, date, desc, done))
    conn.commit()
    conn.close()
    return True


def remove_task_from_db(task_id):
    """
    Remove a task from the task database.
    """
    conn = get_connection()
    delstmt = "DELETE FROM items WHERE id=?"
    conn.execute(delstmt, (task_id,))
    conn.commit()
    conn.close()
    return True


def update_task_in_db(task):
    """
    Change a field value of a task in the task database.
    """
    conn = get_connection()
    updatestmt = "UPDATE items SET title=?, date=?, description=?, "
    updatestmt += "done = ? WHERE id=?"
    title = task['title']
    date = task['date']
    desc = task['description']
    done = task['done']
    task_id = task['id']
    conn.execute(updatestmt, (title, date, desc, done, task_id))
    conn.commit()
    conn.close()
    return True


def make_tasks_list(items=[]):
    """
    Convert a list of tuples containing task values into dictionaries with
    key-value pairs.
    """
    tasklist = []

    for item in items:
        task = {'id': item[0], 'title': item[1], 'date': item[2],
                'description': item[3], 'done': bool(item[4])}
        tasklist.append(task)

    return tasklist
