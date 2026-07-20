import unittest
from peewee import *

from app import TimelinePost
from playhouse.shortcuts import model_to_dict
import datetime


MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')


class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection... but good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(
            name='John Doe',
            email='john@example.com',
            content="Hello World, I'm John!",
            created_at=datetime.datetime(2026, 1, 1, 9, 0, 0),
        )
        assert first_post.id == 1

        second_post = TimelinePost.create(
            name="Jane Doe",
            email="jane@example.com",
            content="Hello World, I'm Jane!",
            created_at=datetime.datetime(2026, 1, 1, 10, 0, 0),
        )
        assert second_post.id == 2

        #  Get timeline posts and assert that they are correct
        posts = [model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())]
        self.assertEqual(first_post.id, 1)
        self.assertEqual(second_post.id, 2)


        posts = list(
            TimelinePost.select().order_by(
                TimelinePost.created_at.desc(), TimelinePost.id.desc()
            )
        )
        self.assertEqual([post.name for post in posts], ["Jane Doe", "John Doe"])

        
