from flask import render_template
from . import user

@user.app_errorhandler(400)
def bad_request(e):
    return render_template('error/400.html'), 400

@user.app_errorhandler(403)
def forbidden(e):
    return render_template('error/403.html'), 403

@user.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@user.app_errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500

