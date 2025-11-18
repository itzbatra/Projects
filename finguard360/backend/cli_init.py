# Provides a simple CLI entry to init DB for local dev using Flask CLI
from app import create_app, db
app = create_app()

@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Initialized the database.')
