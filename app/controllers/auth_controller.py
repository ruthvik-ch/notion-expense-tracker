from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
import os
from dotenv import load_dotenv

load_dotenv()

auth_controller = Blueprint("auth_controller", __name__)

PASSWORD = os.getenv("PASSWORD", "")

# ---------- VIEW CONTROLLER ----------

@auth_controller.route("/login", methods=["GET"])
def login_page():
    """Render the login page"""
    if session.get("logged_in"):
        return redirect(url_for("expense_controller.home"))
    return render_template("login.html")


@auth_controller.route("/logout", methods=["GET"])
def logout():
    """Logout the user"""
    session.clear()
    return redirect(url_for("expense_controller.home"))


# ---------- API CONTROLLER ----------

@auth_controller.route("/api/login", methods=["POST"])
def authenticate():
    """Validate password and create session"""
    data = request.get_json()
    password = data.get("password", "") if data else ""

    if not password:
        return jsonify({"error": "Password is required"}), 400

    if password == PASSWORD:
        session["logged_in"] = True
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid password"}), 401


@auth_controller.route("/api/check-login", methods=["GET"])
def check_login():
    """Check if user is logged in"""
    logged_in = session.get("logged_in", False)
    return jsonify({"logged_in": logged_in}), 200
