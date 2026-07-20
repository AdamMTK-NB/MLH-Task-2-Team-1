import logging
import os
import datetime

from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

# Hobby content lives in its own module so teammates can update images and names
# without touching route or template logic (Single Responsibility).
from .hobbies_data import TEAM_HOBBIES
from .work_history_data import TEAM_WORK_HISTORY
from .places_data import TEAM_PLACES
from .education_data import TEAM_EDUCATION
from .about_us_data import TEAM_ABOUT_US

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# New nav items only need an entry here once a matching route exists.
NAV_PAGES = [
    {"endpoint": "index", "label": "Home"},
    {"endpoint": "work", "label": "Work"},
    {"endpoint": "hobbies", "label": "Hobbies"},
    {"endpoint": "map_page", "label": "Map"},
    {"endpoint": "education", "label": "Education"},
    {"endpoint": "timeline", "label": "Timeline"},
]

app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306,
)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

# Tests rebind TimelinePost to an in-memory SQLite database.  Do not attempt
# to connect while importing the app when no MySQL database has been
# configured (for example, in a local test environment).
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase(
        'file:memory?mode=memory&cache=shared',
        uri=True
    )
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

TimelinePost.bind(mydb, bind_refs=False, bind_backrefs=False)
mydb.connect(reuse_if_open=True)
mydb.create_tables([TimelinePost], safe=True)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    # name = request.form['name']
    name = request.form.get("name", "").strip()
    if not name:
        return {"error": "Invalid name"}, 400
    email = request.form.get("email", "").strip()
    if not email or "@" not in email:
        return {"error": "Invalid email"}, 400
    content = request.form.get("content", "").strip()
    if not content:
        return {"error": "Invalid content"}, 400    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in 
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    post = TimelinePost.get_or_none(TimelinePost.id == post_id)

    if post is None:
        return {"error": "Timeline post not found"}, 404

    post.delete_instance()
    return {"message": "Timeline post deleted"}

@app.route('/timeline')
def timeline():
    logger.info("Serving timeline page")
    return render_template("timeline.html", title="Timeline")

@app.context_processor
def inject_globals():
    # Shared across all templates so the nav bar stays in sync automatically.
    return {
        "nav_pages": NAV_PAGES,
        "url": os.getenv("URL"),
    }


@app.route("/")
def index():
    logger.info("Serving index page")
    return render_template(
        "index.html",
        title="MLH Fellow",
        team_about=TEAM_ABOUT_US,
    )


@app.route("/work")
def work():
    logger.info("Serving work history page")
    return render_template("work.html", title="Work Experience", team_work=TEAM_WORK_HISTORY)


@app.route("/hobbies")
def hobbies():
    logger.info("Serving hobbies page")
    return render_template("hobbies.html", team_hobbies=TEAM_HOBBIES)


@app.route("/map")
def map_page():
    logger.info("Serving map page")
    return render_template("map.html", title="Around the World", team_places=TEAM_PLACES)


@app.route("/education")
def education():
    logger.info("Serving education page")
    return render_template("education.html", title="Education", team_education=TEAM_EDUCATION)


@app.errorhandler(404)
def page_not_found(error):
    logger.warning("Page not found: %s", error)
    return "Page not found", 404


@app.errorhandler(500)
def internal_server_error(error):
    logger.error("Internal server error: %s", error)
    return "Internal server error", 500
