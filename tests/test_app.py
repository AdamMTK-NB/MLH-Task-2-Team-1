# tests/test_app.py

import unittest
import os

os.environ['TESTING'] = 'true'

from app import app, TimelinePost


class AppTestCase(unittest.TestCase):
    def setUp(self):
        TimelinePost.delete().execute()
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        for name in ["Adam Maatouk", "Gabriel Changamire", "Amar Kanakamedala"]:
            assert f'<p class="team-member-name">{name}</p>' in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "Hello World, I'm John!",
            },
        )
        assert response.status_code == 200
        assert response.is_json
        created_post = response.get_json()
        assert created_post["name"] == "John Doe"
        assert created_post["email"] == "john@example.com"
        assert created_post["content"] == "Hello World, I'm John!"

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        timeline_posts = response.get_json()["timeline_posts"]
        assert len(timeline_posts) == 1
        assert timeline_posts[0]["id"] == created_post["id"]
        assert timeline_posts[0]["name"] == "John Doe"

    def test_timelines(self):


        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": "Hello World, I'm John!"
            },
        )
        assert response.status_code == 200
        assert response.is_json
        created_post = response.get_json()
        assert created_post["name"] == "John Doe"
        assert created_post["email"] == "john@example.com"
        assert created_post["content"] == "Hello World, I'm John!"

        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Jane Doe",
                "email": "jane@example.com",
                "content": "Hello World, I'm Jane!"
            },
        )
        assert response.status_code == 200
        assert response.is_json
        created_post_2 = response.get_json()
        assert created_post_2["name"] == "Jane Doe"
        assert created_post_2["email"] == "jane@example.com"
        assert created_post_2["content"] == "Hello World, I'm Jane!"

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        timeline_posts = response.get_json()["timeline_posts"]

        assert len(timeline_posts) == 2

        assert timeline_posts[1]["id"] == created_post["id"]
        assert timeline_posts[1]["name"] == "John Doe"
        assert timeline_posts[0]["id"] == created_post_2["id"]
        assert timeline_posts[0]["name"] == "Jane Doe"
        

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            "/api/timeline_post",
            data={
                "email": "john@example.com",
                "content": "Hello world, I'm John!"
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": ""
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!"
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
