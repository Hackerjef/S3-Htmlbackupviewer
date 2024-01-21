from flask import Blueprint, current_app, redirect, session, url_for, g

from s3htmlviewer.decos import authed, with_user

Auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@Auth.route('/logout', methods=['POST', 'GET'])
@authed
def auth_discord_logout():
    current_app.discord.revoke()
    return redirect(url_for("root"))


@Auth.route('/discord')
def auth_discord():
    return current_app.discord.create_session(scope=["guilds", "identify"], prompt=False)


@Auth.route('/discord/callback')
def auth_discord_callback():
    try:
        current_app.discord.callback()
    except: # noqa
        return redirect(url_for("auth.auth_discord"))

    # Try to get all guilds
    if session.get("next_url", None):
        url = str(session["next_url"])
        del session["next_url"]
        return redirect(url)
    return redirect(url_for("root"))


@Auth.route('/@me')
@with_user
def auth_me():
    data = g.user.__dict__.copy()
    for k in list(data.keys()):
        if k.startswith('_'):
            del data[k]
    data['guilds'] = g.guilds
    return data
