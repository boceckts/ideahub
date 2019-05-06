from flask import render_template

from app import db, app


@app.errorhandler(403)
def not_found_error(error):
    return render_template('error.html', title=403, message='You are not allowed to access the resource', code=403), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', title=404, message='Resource not found', code=404), 404


@app.errorhandler(405)
def not_found_error(error):
    return render_template('error.html', title=405, message='Method not allowed', code=405), 405


@app.errorhandler(409)
def not_found_error(error):
    return render_template('error.html', title=409, message='The data you sent to the server is not valid',
                           code=409), 409


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', title=500, message='Oops, something went wrong...', code=500), 500
