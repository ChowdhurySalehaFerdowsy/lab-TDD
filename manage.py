# manage.py

from flask.cli import FlaskGroup
from src import app, db #new-part 3

cli = FlaskGroup (app)

# new-part -3
@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__=='__main__':
    cli()
    