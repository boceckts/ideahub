from flask import render_template

from app import db, app


@app.errorhandler(403)
def not_found_error(error):
    return render_template('error.html', message='You are not allowed to access the resource', code=403), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', message='Resource not found', code=404), 404


@app.errorhandler(409)
def not_found_error(error):
    return render_template('error.html', message='The data you sent to the server is not valid', code=409), 409


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', message='Oops, something went wrong...', code=500), 500
