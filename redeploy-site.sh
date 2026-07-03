#!/bin/bash

PROJECT_DIR="$HOME/MLH-Task-2-Team-1"

tmux kill-server 2>/dev/null

cd "$PROJECT_DIR" || exit

git fetch
git reset --hard origin/main

python3 -m venv venv
source venv/bin/activate

python3 -m pip install -r requirements.txt

tmux new -d -s flask "cd $PROJECT_DIR && source venv/bin/activate && flask run --host=0.0.0.0 --port=5000"