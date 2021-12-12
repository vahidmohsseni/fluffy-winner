import random
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from Server.models import PlantPot, Location, Repository


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def select_all_plants():
    db = get_db()
    res = db.execute("SELECT * FROM plant_pot").fetchall()

    lis = None
    if res is not None:
        lis = []
        for p in res:
            lis.append(PlantPot(p[0], p[1], p[2], p[3], p[4]))

    return lis


def select_all_locations():
    db = get_db()
    res = db.execute("SELECT * FROM location").fetchall()

    lis = None
    if res is not None:
        lis = []
        for p in res:
            lis.append((Location(p[0], p[1], p[2])))

    return lis


def select_all_from_repo():
    db = get_db()
    res = db.execute("SELECT repository.*, location.name, plant_pot.name, plant_pot.min_ph_level, plant_pot.max_ph_level FROM repository LEFT JOIN location ON repository.location_id = location.id LEFT JOIN plant_pot ON repository.plant_pot_id = plant_pot.id").fetchall()
    lis = None
    if res is not None:
        lis = []
        for p in res:
            lis.append(Repository(p[0], p[3], p[4], p[5], p[6], p[7], p[8], p[9]))

    return lis


def get_location_temperature(lid: int):
    db = get_db()
    res = db.execute(f"SELECT max_temperature FROM location WHERE id = {lid}").fetchone()
    return res[0] #+ random.randint(1, 4)


def add_item_to_repo(loc_id, plant_id):
    db = get_db()
    db.execute(f"INSERT INTO repository (location_id, plant_pot_id) VALUES ({loc_id}, {plant_id})")
    db.commit()


def remove_item_from_repo(rid):
    db = get_db()
    db.execute(f"DELETE FROM repository where id = {rid}")
    db.commit()


def add_new_location(name, temp):
    db = get_db()
    db.execute(f"INSERT INTO location (name, max_temperature) VALUES ('{name}', {temp})")
    db.commit()

def add_new_type_plant(name, max_w, min_p, max_p):
    db = get_db()
    db.execute(f"INSERT INTO plant_pot (name, max_water_amount, min_ph_level, max_ph_level) VALUES ('{name}', {max_w}, {min_p}, {max_p})")
    db.commit()


def update_plant_and_temp(rid, moist_level, ph, lid, temp, time):
    db = get_db()
    db.execute(f"UPDATE repository SET water_level = {moist_level}, ph_level = {ph}, time = '{time}' WHERE id = {rid}")
    db.commit()
    db.execute(f"UPDATE location SET max_temperature = {temp} WHERE id = {lid}")
    db.commit()


def get_a_plant_from_repo(rid):
    db = get_db()
    res = db.execute(f"SELECT repository.*, plant_pot.min_ph_level, plant_pot.max_ph_level, plant_pot.max_water_amount "
                     f"FROM repository LEFT JOIN plant_pot ON repository.plant_pot_id = plant_pot.id "
                     f"WHERE repository.id = {rid}").fetchone()
    print(res[4], res[8])
    return Repository(res[0], res[3], res[4], res[5], None, None, res[6], res[7], res[8])


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_data():
    db = get_db()

    with current_app.open_resource('data.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    init_data()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
