DROP TABLE IF EXISTS plant_pot;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS repository;


CREATE TABLE plant_pot (
    id INTEGER primary KEY AUTOINCREMENT,
    name TEXT,
    max_water_amount INTEGER,
    min_ph_level FLOAT,
    max_ph_level FLOAT
);

CREATE TABLE location(
    id INTEGER primary KEY AUTOINCREMENT,
    name TEXT,
    max_temperature INTEGER
);

CREATE TABLE repository(
    id INTEGER primary key AUTOINCREMENT,
    location_id INTEGER,
    plant_pot_id INTEGER,
    time TEXT,
    water_level INTEGER,
    ph_level FLOAT,
    FOREIGN KEY(location_id) REFERENCES location(id),
    FOREIGN KEY(plant_pot_id) REFERENCES plant_pot(id)
);