"""Registration, login, and logout endpoints."""
from urllib.parse import urlparse

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from email_validator import EmailNotValidError, validate_email
from sqlalchemy import func

from ..extensions import db, limiter
from ..models import User
from . import auth_bp


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    errors = {}
    values = {"name": "", "email": ""}
    if request.method == "POST":
        values = {key: request.form.get(key, "").strip() for key in values}
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if not values["name"] or len(values["name"]) > 80:
            errors["name"] = "Enter a name up to 80 characters."
        email = values["email"].lower()
        try:
            email = validate_email(email, check_deliverability=False).normalized.lower()
        except EmailNotValidError:
            errors["email"] = "Enter a valid email address."
        if not errors.get("email") and db.session.scalar(db.select(User.id).where(func.lower(User.email) == email)):
            errors["email"] = "An account with this email already exists."
        if len(password) < 8 or len(password) > 128:
            errors["password"] = "Use a password between 8 and 128 characters."
        if password != confirm:
            errors["confirm_password"] = "The passwords do not match."
        if not errors:
            user = User(name=values["name"], email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Your account is ready. Welcome!", "success")
            return redirect(url_for("main.dashboard"))
    return render_template("auth/register.html", errors=errors, values=values)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():
    errors, email = {}, ""
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = db.session.scalar(db.select(User).where(func.lower(User.email) == email))
        if user is None or not user.check_password(request.form.get("password", "")):
            errors["form"] = "Email or password is incorrect."
        else:
            login_user(user, remember=False)
            target = request.args.get("next", "")
            if target.startswith("/") and not target.startswith("//") and "\\" not in target and urlparse(target).netloc == "":
                return redirect(target)
            flash("You are signed in.", "success")
            return redirect(url_for("main.dashboard"))
    return render_template("auth/login.html", errors=errors, email=email)


@auth_bp.post("/logout")
def logout():
    logout_user()
    flash("You have been signed out.", "success")
    return redirect(url_for("auth.login"))
