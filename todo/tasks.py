import sqlite3


def retrieve_dbdata():
    """
    Read and return all todo items from the database.
    """
    conn = sqlite3.connect('todo/todo.db')
    cur = conn.execute('SELECT * FROM items')
    items = cur.fetchall() 
    conn.close()
    return items


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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    doctest.testfile('test_db_setup.txt', optionflags=doctest.ELLIPSIS)
