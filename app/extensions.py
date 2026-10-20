"""Extensions are created here and initialized by the application factory."""
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please sign in to view that page."
login_manager.login_message_category = "info"
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)
