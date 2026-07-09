#!/bin/bash

PROJECT_DIR="$HOME/MLH-Task-2-Team-1"

cd "$PROJECT_DIR" || exit

git fetch
git reset --hard origin/main

python3 -m venv venv
source venv/bin/activate

python3 -m pip install -r requirements.txt

sudo systemctl restart myportfolio
sudo systemctl status myportfolio --no-pager
