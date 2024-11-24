from flask_app import app
from flask_app.controllers import users, home, groups, messages, events, discussions


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5001)