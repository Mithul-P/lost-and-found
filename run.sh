#!/usr/bin/env bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Run 'python app.py' after creating the database and loading init_db.sql"
