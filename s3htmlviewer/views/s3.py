import os

import flask
from flask import Blueprint, current_app, redirect, session, url_for, g, jsonify, request, abort
from minio import S3Error

from s3htmlviewer.decos import with_user, has_permission
from s3htmlviewer.s3util import get_files, get_file

S3 = Blueprint('S3', __name__, url_prefix='/api/s3')


@S3.route("/list")
@with_user
@has_permission
def listendpoint():
    parent = request.args.get('parent')
    allowed = request.args.get('allowed')

    if not allowed:
        allowed = ['folder']

    if not parent:
        parent = None
    return jsonify(list(get_files(parent=parent, allow=allowed))), 200


@S3.route("/file/<path:path>")
@with_user
@has_permission
def fileendpoint(path):
    if not path:
        abort(404, 'File not found')
    try:
        file = get_file(path)
    except S3Error:
        abort(404, 'Backend error')

    # stupid way to match contact type
    resp = flask.Response(file)
    resp.headers['Content-Type'] = file.headers.get('Content-Type')
    return resp
