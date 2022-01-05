"""
WSGI module.

It is for correct nginx/flask
"""


from app import app

if __name__ == '__main__':
    app.run()
