# test_db.py
import os
import sys
import unittest
from peewee import *

# Ensure the project root (parent of this tests/ folder) is on sys.path,
# so `from app import ...` works whether you run this via
# `pytest`, `python -m unittest`, or `python tests/test_db.py` directly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')


class TestTimelinePost(unittest.TestCase):

    # Binding models to the test db is safe to do once for the whole class -- it doesn't represent state that a test could mutate, just wiring. Doing this per-test would be wasted work.
    @classmethod
    def setUpClass(cls):
        print('setupClass: bind models')
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

    # No tearDownClass needed here: peewee's Database class has no unbind()
    # method, and since setUpClass binds TimelinePost to test_db once for
    # the whole process, there's nothing to "restore" afterward. If another
    # test file also needs TimelinePost bound to a different database, that
    # file handles it with its own setUpClass -- it doesn't depend on this
    # one cleaning up.

    # Table creation + fixture data DOES represent mutable state, so it needs to happen per-test. Otherwise 1 test's changes (e.g. deleting a post) would leak into the next test and make results depend on execution order.
    def setUp(self):
        print('setUp per test: create tables')
        test_db.connect()
        test_db.create_tables(MODELS)

        # Common fixture posts every test can rely on existing.
        self.first_post = TimelinePost.create(
            name='John Doe',
            email='john@example.com',
            content="Hello world, I'm John!",
        )
        self.second_post = TimelinePost.create(
            name='Jane Doe',
            email='jane@example.com',
            content="Hello world, I'm Jane!",
        )

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_post_creation(self):
        # setUp already created these two posts -- just assert on them.
        print('test timeline POST')
        self.assertEqual(self.first_post.id, 1)
        self.assertEqual(self.first_post.name, 'John Doe')
        self.assertEqual(self.second_post.id, 2)
        self.assertEqual(self.second_post.name, 'Jane Doe')

    def test_get_timeline_posts(self):
        print('test timeline GET')
        posts = list(TimelinePost.select().order_by(TimelinePost.created_at.asc()))

        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0].name, 'John Doe')
        self.assertEqual(posts[0].email, 'john@example.com')
        self.assertEqual(posts[1].name, 'Jane Doe')
        self.assertEqual(posts[1].email, 'jane@example.com')

    def test_delete_timeline_post(self):
        print('test timeline DELETE')
        deleted_count = (
            TimelinePost.delete()
            .where(TimelinePost.id == self.first_post.id)
            .execute()
        )

        self.assertEqual(deleted_count, 1)
        remaining = list(TimelinePost.select())
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].name, 'Jane Doe')


# allows us to run test like normal python file in Terminal, i.e. "python test_db.py"
if __name__ == '__main__':
    unittest.main()