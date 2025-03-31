"""The WSGI (web application) interface."""

import os

import flask
import flask_bootstrap  # type: ignore[import-untyped]
import flask_sqlalchemy
import flask_wtf  # type: ignore[import-untyped]
import sqlalchemy.orm

from templatepython.config import get_config, get_storage


class _OrmBase(sqlalchemy.orm.DeclarativeBase):
    pass


db = flask_sqlalchemy.SQLAlchemy(model_class=_OrmBase)
csrf = flask_wtf.CSRFProtect()


def create_app() -> flask.Flask:
    """Create and configure the flask application."""
    cfg = get_config()

    # Those cannot be set when the app has started...
    if cfg.get("DEBUG"):
        os.environ["FLASK_DEBUG"] = "1"
    if cfg.get("TESTING"):
        os.environ["FLASK_TESTING"] = "1"

    app = flask.Flask(
        __name__, instance_path=get_storage().joinpath("instance").as_posix()
    )
    app.config.update(**get_config())

    db.init_app(app)
    flask_bootstrap.Bootstrap(app)
    csrf.init_app(app)

    @app.route("/")
    def index() -> str:
        return flask.render_template("index.html")

    return app
