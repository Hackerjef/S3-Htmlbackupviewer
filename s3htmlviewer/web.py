import logging
import os
import signal
from flask import Flask, render_template, Response, g, request
from flask_discord import DiscordOAuth2Session

from werkzeug.middleware.proxy_fix import ProxyFix

from s3htmlviewer.decos import with_user
from s3htmlviewer.views import Auth, S3
from s3htmlviewer.s3util import get_files

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config.from_object(__name__)
app.secret_key = bytes(os.environ["SECRET_KEY"], 'utf-8')
app.config.update(
    SECRET_KEY=bytes(os.environ["SECRET_KEY"], 'utf-8'),
    MAX_CONTENT_LENGTH=(16 * 1024 * 1024),
)


def keyboardInterruptHandler(s, frame):
    os.kill(os.getpid(), signal.SIGTERM)


signal.signal(signal.SIGINT, keyboardInterruptHandler)

DiscordOAuth2Session(app, client_id=os.environ["CLIENT_ID"], client_secret=os.environ["CLIENT_SECRET"],
                     redirect_uri=os.environ["CLIENT_REDIRECT_URI"])

app.register_blueprint(Auth)
app.register_blueprint(S3)


@app.route("/")
@with_user
def root():
    return render_template('index.jinja',
                           user=g.user,
                           parent_backups=list(get_files(allow=['folder'])) if g.get('guilds', {}).get('in_guild', False) else None,
                           backup_files=None if not request.args.get("backup_sel") else list(
                               get_files(allow=['file'], parent=request.args.get('backup_sel'))) if g.get('guilds', {}).get('in_guild', False) else None)


@app.route("/robots.txt")
def robotstxt():
    r = Response(response="User-Agent: *\nDisallow: /\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r
