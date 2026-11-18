"""Generic list / create / edit / delete routes for every resource in resources.py."""
import mysql.connector
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import database
from resources import RESOURCES
from validation import fk_options, form_value, validate

bp = Blueprint("crud", __name__)


def _get(key):
    if key not in RESOURCES:
        abort(404)
    return RESOURCES[key]


def _row_or_404(r, row_id):
    row = database.query(f"SELECT * FROM {r['table']} WHERE {r['pk']} = %s", (row_id,), one=True)
    if not row:
        abort(404)
    return row


def _render_form(key, r, values, errors, row_id=None):
    options = {f["name"]: fk_options(f["fk"]) for f in r["fields"] if f["kind"] == "fk"}
    return render_template("form.html", key=key, r=r, values=values, errors=errors, options=options, row_id=row_id)


@bp.route("/<key>/")
def list_(key):
    r = _get(key)
    return render_template("list.html", key=key, r=r, rows=database.query(r["list_sql"]))


@bp.route("/<key>/new", methods=["GET", "POST"])
def create(key):
    r = _get(key)
    if request.method == "POST":
        values, errors = validate(r, request.form)
        if not errors:
            cols = ", ".join(values)
            database.execute(f"INSERT INTO {r['table']} ({cols}) VALUES ({', '.join(['%s'] * len(values))})",
                             tuple(values.values()))
            flash(f"{r['singular']} added.", "success")
            return redirect(url_for("crud.list_", key=key))
        return _render_form(key, r, request.form, errors)
    return _render_form(key, r, {}, {})


@bp.route("/<key>/<int:row_id>/edit", methods=["GET", "POST"])
def edit(key, row_id):
    r = _get(key)
    row = _row_or_404(r, row_id)
    if request.method == "POST":
        values, errors = validate(r, request.form)
        if not errors:
            sets = ", ".join(f"{c} = %s" for c in values)
            database.execute(f"UPDATE {r['table']} SET {sets} WHERE {r['pk']} = %s", (*values.values(), row_id))
            flash(f"{r['singular']} updated.", "success")
            return redirect(url_for("crud.list_", key=key))
        return _render_form(key, r, request.form, errors, row_id)
    shown = {f["name"]: form_value(f, row[f["name"]]) for f in r["fields"]}
    return _render_form(key, r, shown, {}, row_id)


@bp.route("/<key>/<int:row_id>/delete", methods=["POST"])
def delete(key, row_id):
    r = _get(key)
    _row_or_404(r, row_id)
    try:
        database.execute(f"DELETE FROM {r['table']} WHERE {r['pk']} = %s", (row_id,))
        flash(f"{r['singular']} deleted.", "success")
    except mysql.connector.Error as exc:
        flash(f"Could not delete: {exc.msg}", "danger")
    return redirect(url_for("crud.list_", key=key))


@bp.route("/<key>/<int:row_id>")
def detail(key, row_id):
    r = _get(key)
    return render_template("detail.html", key=key, r=r, row=_row_or_404(r, row_id))
