from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.user_bp import user_bp
from blueprints.prop_bp import prop_bp

registerable_bp = [
    cli_bp,
    auth_bp,
    user_bp,
    prop_bp
]