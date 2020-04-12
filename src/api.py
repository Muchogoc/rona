import time

from flask import Blueprint, g, render_template, request
from flask_api.decorators import set_renderers
from flask_api.renderers import BrowsableAPIRenderer, JSONRenderer

from .estimator import estimator
from .helpers import XMLRenderer, open_log_file

bp = Blueprint("api", __name__, url_prefix="/api/v1")

API_PURPOSE = (
    "Helping society and leaders "
    "prepare for the real big problem of COVID-19, which is its "
    "impact on lives, health systems, supply chains, and the economy"
)


@bp.route("/on-covid-19", methods=("GET", "POST"))
@set_renderers(JSONRenderer, BrowsableAPIRenderer)
def default_covid_estimates():
    if request.method == "POST":
        estimates = estimator(request.data)
        return estimates

    return {"COVID-19 estimator": API_PURPOSE}


@bp.route("/on-covid-19/json", methods=("GET", "POST"))
@set_renderers(JSONRenderer, BrowsableAPIRenderer)
def json_covid_estimates():
    if request.method == "POST":
        estimates = estimator(request.data)
        return estimates

    return {"COVID-19 estimator": API_PURPOSE}


@bp.route("/on-covid-19/xml", methods=("GET", "POST"))
@set_renderers(XMLRenderer, BrowsableAPIRenderer)
def xml_covid_estimates():
    if request.method == "POST":
        estimates = estimator(request.data)
        return estimates

    return {"COVID-19 estimator": API_PURPOSE}


@bp.route("/logs")
def covid_estimates_logs():
    logs = open_log_file()
    return render_template("log.html", logs=logs)


@bp.before_request
def start_timer():
    g.start = time.time()


@bp.after_request
def log_request(response):
    if request.path == "/favicon.ico":
        return response
    elif request.path.endswith("logs"):
        return response

    now = time.time()
    duration = (now - g.start) * 1000
    ms = round(duration, 2)

    log = (
        f"{request.method}    {request.path}  {response.status_code}  {ms} ms"
    )
    with open("src/logs.txt", "a+") as f:
        f.write(log + "\n")

    return response
