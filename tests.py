import json
import os
import unittest

from todo.tasks import get_connection
from todo.tasks import drop_testing_database
from todo.tasks import make_tasks_list
from todo.todo import app


os.environ['TESTING'] = 'True'


class AppTests(unittest.TestCase):

    def setUp(self):
        self.connection = get_connection()
        schema = '''CREATE TABLE items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NUll,
        date TEXT NOT NULL,
        description TEXT,
        done BOOLEAN
        );'''
        self.connection.execute(schema)
        self.client = app.test_client()

    def tearDown(self):
        self.connection.close()
        drop_testing_database()

    def _add_items(self):
        # Add a couple of items
        sql = '''INSERT INTO "items" VALUES(
           1,
           'Buy groceries',
           '2017-03-15 11:51',
           'Milk, Cheese, Pizza, Fruit, Tylenol',
           0)'''
        self.connection.execute(sql)
        sql = '''INSERT INTO "items" VALUES(
           2,
           'Learn SQL',
           '2017-03-15 11:54',
           'Complete Khan Academy SQL tutorial.',
           0)'''
        self.connection.execute(sql)
        self.connection.commit()

    def test_make_tasks_list(self):
        # Add a couple of items
        self._add_items()
        # Get the items
        cursor = self.connection.execute('SELECT * FROM items ORDER BY id')
        items = cursor.fetchall()
        tasklist = make_tasks_list(items)
        # A task is created for each item
        self.assertEqual(len(tasklist), 2)
        # Check the attributes of the task for the first item
        first_task = tasklist[0]
        self.assertEqual(first_task['id'], 1)
        self.assertEqual(first_task['title'], 'Buy groceries')
        self.assertEqual(first_task['date'], '2017-03-15 11:51')
        self.assertEqual(
            first_task['description'],
            'Milk, Cheese, Pizza, Fruit, Tylenol'
        )
        self.assertEqual(first_task['done'], False)

    def test_get_tasks_endpoint(self):
        # Add a couple of items
        self._add_items()
        url = '/todo/api/v1.0/tasks'
        response = self.client.get(url)
        result = response.get_data(as_text=True)
        tasks = json.loads(result)['tasks']
        # A task is created for each item
        self.assertEqual(len(tasks), 2)
        # Check the attributes of the task for the first item
        first_task = sorted(tasks, key=lambda task: task['uri'])[0]
        self.assertEqual(
            first_task['uri'],
            'http://localhost/todo/api/v1.0/tasks/1'
        )
        self.assertEqual(first_task['title'], 'Buy groceries')
        self.assertEqual(
            first_task['description'],
            'Milk, Cheese, Pizza, Fruit, Tylenol'
        )
        self.assertEqual(first_task['date'], '2017-03-15 11:51')
        self.assertEqual(first_task['done'], False)

    def test_delete_task_endpoint(self):
        # Get the number of tasks in tasklist before delete
        self._add_items()
        url = '/todo/api/v1.0/tasks'
        response = self.client.get(url)
        result = response.get_data(as_text=True)
        tasks = json.loads(result)['tasks']
        num_tasks_before = len(tasks)

        # Delete item 2
        url = '/todo/api/v1.0/tasks/2'
        response = self.client.delete(url)

        # Get the number of tasks in tasklist after delete
        url = '/todo/api/v1.0/tasks'
        response = self.client.get(url)
        result = response.get_data(as_text=True)
        tasks = json.loads(result)['tasks']
        num_tasks_after = len(tasks)

        self.assertEqual(num_tasks_before-1, num_tasks_after)

    def test_update_task_endpoint(self):
        # Get tasks and mark one as done
        self._add_items()
        data = {}
        headers = {'content-type': 'application/json'}
        url = '/todo/api/v1.0/tasks'
        response = self.client.put(url, headers=headers, data=data)
        result = response.get_data(as_text=True)
        tasks = json.loads(result)['tasks']


if __name__ == '__main__':
    unittest.main()
