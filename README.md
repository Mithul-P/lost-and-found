# Lost and Found Management System (Flask + MySQL)

## Quick start (Windows / macOS / Linux)

1. Create a virtual environment and activate it:
   - Windows (PowerShell):
     ```
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - macOS / Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create the database and tables:
- Start MySQL and run `init_db.sql` (for example using MySQL Workbench or `mysql -u root -p < init_db.sql`).

4. Edit `.env` if your DB credentials differ.

5. Run the app:
```
python app.py
```

6. Open http://127.0.0.1:5000 in your browser.

This package includes sample data so the home page shows demo items.
