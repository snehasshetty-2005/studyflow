"""Flask application factory and shared request configuration."""
from datetime import date
import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user

from config import Config
from .extensions import csrf, db, limiter, login_manager, migrate


def create_app(config_object=Config):
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_object(config_object)
    Config.validate(app)

    from . import models  # noqa: F401 - registers models with SQLAlchemy metadata

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    from .auth import auth_bp
    from .main import main_bp
    from .tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    @app.context_processor
    def inject_template_values():
        return {"today": date.today(), "app_user": current_user}

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(429)
    def too_many_requests(_error):
        return render_template("errors/429.html"), 429

    @app.errorhandler(500)
    def server_error(error):
        app.logger.error("Unhandled request error (%s); details suppressed.", type(error).__name__)
        return render_template("errors/500.html"), 500

    @app.before_request
    def redirect_authenticated_auth_pages():
        if current_user.is_authenticated and request.endpoint in {"auth.login", "auth.register"}:
            flash("You are already signed in.", "info")
            return redirect(url_for("main.dashboard"))

    return app
