from gevent import monkey

monkey.patch_all()
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

import click
from logging.config import dictConfig
from werkzeug.serving import run_simple


@click.group()
def cli():
    dictConfig({
        'version': 1,
        'formatters': {'default': {'format': '[%(levelname)s] %(asctime)s - %(name)s:%(lineno)d - %(message)s'}},
        'handlers': {'wsgi': {'class': 'logging.StreamHandler', 'stream': 'ext://sys.stdout', 'formatter': 'default'}},
        'root': {'level': 'INFO', 'handlers': ['wsgi']}
    })


@cli.command()
@click.option('--debug/--no-debug', '-d', default=True)
def serve(debug):
    from s3htmlviewer.web import app

    if debug:
        app.debug = True
        return run_simple(os.environ.get("HOST", "0.0.0.0"), int(os.environ.get("PORT", "80")), app, use_debugger=True, use_reloader=True, use_evalex=True, threaded=True)
    else:
        return run_simple(os.environ.get("HOST", "0.0.0.0"), int(os.environ.get("PORT", "80")), app, threaded=True)


if __name__ == '__main__':
    cli()
