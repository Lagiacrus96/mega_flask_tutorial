from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404 # Requires error code

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback() # Issues session rollback to prevent failed database session to interfere with database access
    return render_template('500.html'), 500 # Requires error code
