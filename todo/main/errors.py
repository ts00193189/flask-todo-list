from flask import render_template


def page_not_found(error):
    print(error)
    return render_template('404.html'), 404


def bad_request(error):
    print(error)
    return render_template('400.html'), 400
