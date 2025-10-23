python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Write-Host "Run 'python app.py' after creating the database and loading init_db.sql"
