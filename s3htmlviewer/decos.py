import os
from functools import wraps

from flask import current_app, abort, url_for, redirect, g
from oauthlib.oauth2 import InvalidClientError, TokenExpiredError


def authed(func):
    @wraps(func)
    def deco(*args, **kwargs):
        if not current_app.discord.authorized:
            abort(403)
        return func(*args, **kwargs)

    return deco


def has_permission(func):
    @wraps(func)
    def deco(*args, **kwargs):
        if not g.guilds.get('in_guild', False):
            abort(403)
            return
        return func(*args, **kwargs)
    return deco


def with_user(func):
    @wraps(func)
    def deco(*args, **kwargs):
        if current_app.discord.authorized:
            try:
                user = current_app.discord.fetch_user()
            except (InvalidClientError, TokenExpiredError) as e:
                return redirect(url_for("auth.auth_discord"))
        else:
            user = None

        if current_app.discord.authorized:
            _guilds = [str(g.id) for g in current_app.discord.fetch_guilds()]
            guilds = {
                'in_guild': os.environ['ALLOWED_GUILD_ID'] in _guilds,
                'guild_ids': _guilds,
            }
            del _guilds
        else:
            guilds = {}
        g.user = user
        g.guilds = guilds
        return func(*args, **kwargs)

    return deco
