from flask_app import app
# from app import create_app
from flask_app.controllers import users, home, groups, messages, events, discussions

# app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5001)