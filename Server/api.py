import json
import time
import os
import random

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, Response
)
from werkzeug.exceptions import abort

import requests

from Server.db import select_all_plants
from Server.db import select_all_locations
from Server.db import get_location_temperature
from Server.db import add_item_to_repo
from Server.db import select_all_from_repo
from Server.db import remove_item_from_repo
from Server.db import add_new_location
from Server.db import add_new_type_plant
from Server.db import update_plant_and_temp
from Server.db import get_a_plant_from_repo
from Server.db import get_data_for_init
from Server.db import get_history
from Server.helper import MyEncoder

bp = Blueprint('api', __name__)

PORT = str(int(os.environ.get('PORT', 5000)))


@bp.route("/")
def index():
    return render_template("index.html", history=get_history())


# keys: ["location_id", "plant_id", "moisture_level", "ph_level", "temperature"]
# returns: {"status": "ok", "needs_water": [true or false], "ph_stat": ["GOOD", "POOR", "EXCEED"]}
@bp.route("/sensor", methods=["POST", "GET"])
def read_sensor():
    if request.method == "POST":
        if all(k in request.form.keys() for k in ["location_id",
                                                  "plant_id", "moisture_level", "ph_level", "temperature"]):
            lid = request.form["location_id"]
            rid = request.form["plant_id"]
            water = request.form["moisture_level"]
            ph = request.form["ph_level"]
            temp = request.form["temperature"]
            ti = time.ctime(time.time())[4:]
            update_plant_and_temp(rid, water, ph, lid, temp, ti)
            plant = get_a_plant_from_repo(rid)

            if plant.ph_level != "GOOD":
                send_email(f"\n\npH level for plant {rid} is {plant.ph_level}")

            return jsonify({"status": "ok", "needs_water": plant.needs_water, "ph_stat": plant.ph_level})

    return "salam"


@bp.route("/admin", methods=['GET', 'POST'])
def admin_page():
    if request.method == "GET":
        return render_template("admin.html",
                               locations=select_all_locations(),
                               types=select_all_plants(),
                               repo=select_all_from_repo())


@bp.route("/add_plant_to_location", methods=["GET", "POST"])
def add_plant_to_location():
    if request.method == "GET":
        return render_template("addPlant.html", locations=select_all_locations(), plants=select_all_plants())

    elif request.method == "POST":
        if all(k in request.form.keys() for k in ("location_id", "plant_id")):
            add_item_to_repo(request.form["location_id"], request.form["plant_id"])
            return "Successful!"
        return "Invalid"

    return "Invalid Method"


@bp.route("/remove_pot", methods=["POST"])
def remove_pot_from_repo():
    if request.method == "POST":
        rid = request.args["id"]
        remove_item_from_repo(rid)
        return redirect("/admin")


@bp.route("/add_location", methods=["GET", "POST"])
def add_location():
    if request.method == "POST":
        name = request.form["name"]
        temp = request.form["max_temperature"]
        add_new_location(name, int(temp))
        return redirect("/admin")
    else:
        return render_template("addNewLoc.html")


@bp.route("/add_plant", methods=["GET", "POST"])
def add_new_type_of_plant():
    if request.method == "POST":
        name = request.form["name"]
        max_w = request.form["max_water_amount"]
        min_p = request.form["min_ph_level"]
        max_p = request.form["max_ph_level"]
        add_new_type_plant(name, max_w, min_p, max_p)
        return redirect("/admin")
    else:
        return render_template("addNewPlant.html")


@bp.route("/init_sim", methods=["GET"])
def initial_simulation():
    resp = {"num_locations": 0,
            "locations_data": []}
    data = get_data_for_init()
    if data:
        for i in data:
            resp["num_locations"] += 1
            resp["locations_data"].append(i)

    return jsonify(resp)


@bp.route("/loctmp", methods=["GET"])
def locations_tmp():
    if request.method == "GET":
        return str(get_location_temperature(request.args["id"]))


def send_email(message):
    i = random.randint(1, 20)
    if i <= 2:
        base_url = "http://127.0.0.1:" + PORT
        resp = requests.get(base_url + f"/mail?msg={message}")
        return resp
    return 0
