# MLH Fellowship Portfolio — Team 1

A Flask portfolio site built by **Adam Maatouk**, **Amar Kanakamedala**, and **Gabriel Changamire** for the Meta Production Engineering Fellowship (Week 1).

This repo extends the starter portfolio into a full team site with dynamic pages, Jinja templates, and content separated from application logic so each teammate can update their section without touching routes or wiring.

---

# Live Website

The portfolio site is hosted on Vercel and can be viewed here:

https://mlh-task-2-team-1-37cz.vercel.app

---

## Team

| Name | Role |
|------|------|
| Adam Maatouk | MLH Fellow · Software Engineer |
| Amar Kanakamedala | MLH Fellow · Software Engineer |
| Gabriel Changamire | MLH Fellow · Software Engineer |

---

## What We Built

All Week 1 portfolio and Flask tasks are complete. Highlights:

### Home (`/`)

- MLH Fellow profile header with team logo
- **Meet the Team** section with a photo, name, role, bio, and social links for each teammate
- Teammate content is driven by `app/about_us_data.py` and rendered with Jinja loops

### Work (`/work`)

- Work experience page with a section per teammate
- Each role shows title, organization, dates, location, summary, and optional reference links
- Data lives in `app/work_history_data.py`

### Hobbies (`/hobbies`)

- Dedicated hobbies page with a section per teammate
- Each hobby is shown as a card with an image and name
- Clicking a hobby opens an animated modal gallery with multiple related images (Unsplash)
- Data in `app/hobbies_data.py`; modal behaviour in `app/static/js/hobbies.js`

### Education (`/education`)

- Education history page with a section per teammate
- Each entry includes institution, degree, dates, location, highlights, and optional links
- Data lives in `app/education_data.py`

### Map (`/map`)

- Interactive 3D globe showing places each teammate has visited
- Pins, arcs, and a side panel use consistent accent colours per teammate
- Data lives in `app/places_data.py`; globe logic in `app/static/js/map.js`

### Navigation

- Shared layout in `app/templates/base.html`
- Dynamic nav bar built from `NAV_PAGES` in `app/__init__.py` — add a route and a nav entry to expose a new page
- Active page is highlighted in the nav

---

## Project Structure

```
app/
├── __init__.py           # Routes, logging, nav config, context processor
├── about_us_data.py      # Team bios, photos, roles, links (home page)
├── hobbies_data.py       # Hobbies and gallery images per teammate
├── work_history_data.py  # Work experience per teammate
├── education_data.py     # Education per teammate
├── places_data.py        # Map coordinates and place labels
├── templates/
│   ├── base.html         # Shared nav and page shell
│   ├── index.html        # Home / Meet the Team
│   ├── work.html
│   ├── hobbies.html
│   ├── education.html
│   └── map.html
└── static/
    ├── img/              # Team photos and site assets
    ├── js/               # hobbies.js, map.js
    └── styles/main.css
```

---

## Quick Start (Windows)

```powershell
python -m venv python3-virtualenv
.\python3-virtualenv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `example.env` to `.env`, then run:

```powershell
$env:FLASK_ENV = "development"
$env:FLASK_APP = "app"
flask run
```

Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

<details>
<summary>macOS / Linux commands</summary>

```bash
python -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt
cp example.env .env
export FLASK_ENV=development
export FLASK_APP=app
flask run
```

</details>

---

## Updating Content

| What to change | File |
|----------------|------|
| Bios, roles, GitHub/LinkedIn links | `app/about_us_data.py` |
| Work experience | `app/work_history_data.py` |
| Hobbies and gallery images | `app/hobbies_data.py` |
| Education | `app/education_data.py` |
| Map locations | `app/places_data.py` |
| Nav labels / new pages | `app/__init__.py` (`NAV_PAGES` + route) |
| Teammate photos | `app/static/img/` |

Templates use Jinja `{% for %}` loops over these data structures, so adding an entry to a list is usually enough — no template changes required.

---

## Clean Code Practices

- **Logging** — route handlers log page visits; 404/500 handlers log errors (no sensitive data)
- **Separation of concerns** — content in `*_data.py` modules, routes in `__init__.py`, markup in templates
- **DRY layout** — `base.html` shared across all pages; `url_for()` for static assets and links
- **Comments** — explain *why* (design decisions), not *what* the code obviously does

---

## Task Checklist

### GitHub Tasks
- [x] Create Issues for each task
- [x] Progress on each task in a new branch
- [x] Open a Pull Request when a task is finished to get feedback

### Portfolio Tasks
- [x] Add a photo of yourself to the website
- [x] Add an "About yourself" section to the website
- [x] Add your previous work experiences
- [x] Add your hobbies (including images)
- [x] Add your current/previous education
- [x] Add a map of all the cool locations/countries you visited

### Flask Tasks
- [x] Get your Flask app running locally
- [x] Add Jinja templates for multiple work experiences / education / hobbies
- [x] Create a new page to display hobbies
- [x] Add a menu bar that dynamically displays other pages in the app

---

---

# Original MLH Week 1 README

# Production Engineering - Week 1 - Portfolio Site

Welcome to the MLH Fellowship! During Week 1, you'll be using Flask to build a portfolio site. This site will be the foundation for activities we do in future weeks so spend time this week making it your own and reflect your personality!

## Tasks

Once you've got your portfolio downloaded and running using the instructions below, you should attempt to complete the following tasks.

For each of these tasks, you should create an [Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues) and work on them in a new [branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches). When the task has been completed, you should open a [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) and get another fellow in your pod to give you feedback before merging it in.

*Note: Make sure to include a link to the Issue you're progressing on inside of your Pull Request so your reviewer knows what you're progressing on!*

### GitHub Tasks
- [x] Create Issues for each task below
- [x] Progress on each task in a new branch
- [x] Open a Pull Request when a task is finished to get feedback

### Portfolio Tasks
- [x] Add a photo of yourself to the website
- [x] Add an "About youself" section to the website.
- [x] Add your previous work experiences
- [x] Add your hobbies (including images)
- [x] Add your current/previous education
- [x] Add a map of all the cool locations/countries you visited

### Flask Tasks
- [x] Get your Flask app running locally on your machine using the instructions below.
- [x] Add a template for adding multiple work experiences/education/hobbies using [Jinja](https://jinja.palletsprojects.com/en/3.0.x/api/#basics)
- [x] Create a new page to display hobbies.
- [x] Add a menu bar that dynamically displays other pages in the app


## Getting Started

You need to do all your progress here.

## Installation

Make sure you have python3 and pip installed

Create and activate virtual environment using virtualenv
```bash
$ python -m venv python3-virtualenv
$ source python3-virtualenv/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies!

```bash
pip install -r requirements.txt
```

## Usage

Create a .env file using the example.env template (make a copy using the variables inside of the template)

Start flask development server
```bash
$ export FLASK_ENV=development
$ flask run
```

You should get a response like this in the terminal:
```
❯ flask run
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

You'll now be able to access the website at `localhost:5000` or `127.0.0.1:5000` in the browser! 

*Note: The portfolio site will only work on your local machine while you have it running inside of your terminal. We'll go through how to host it in the cloud in the next few weeks!* 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
