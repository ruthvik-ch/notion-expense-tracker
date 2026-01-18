from flask import Flask
from app.controllers.expense_controller import expense_controller
from app.controllers.auth_controller import auth_controller

def create_app():
    app = Flask(__name__)
    app.secret_key = "your-secret-key-change-in-production"
    app.register_blueprint(expense_controller)
    app.register_blueprint(auth_controller)
    return app

app = create_app()

if __name__ == "__main__":
    create_app().run(debug=True)
