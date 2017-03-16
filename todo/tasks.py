import sqlite3


def get_tasks():
    """
      >>> result = get_tasks()
      >>> len(result)
      2
      >>> result[0]['id']
      1
      >>> result[1]['title']
      'Learn Python'
    """
    tasklist = [
        {
            'id': 1,
            'title': 'Buy groceries',
            'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
            'done': False
        },
        {
            'id': 2,
            'title': 'Learn Python',
            'description': 'Need to find a good Python tutorial on the web',
            'done': False
        }
    ]
    return tasklist


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    doctest.testfile('test_db_setup.txt', optionflags=doctest.ELLIPSIS)
