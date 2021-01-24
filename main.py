from flask import Flask, g

import account

app = Flask(__name__)
app.register_blueprint(account.app)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
